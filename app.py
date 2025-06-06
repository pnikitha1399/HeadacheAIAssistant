import os
import logging
import json
from flask import Flask, render_template, request, jsonify
from headache_rag import HeadacheRAG
from knowledge_base import MedicalKnowledgeBase
from models import db, HeadacheRecord

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,  # Detect stale connections
    "pool_recycle": 300,    # Recycle connections after 5 minutes
    "pool_timeout": 30,     # Connection timeout of 30 seconds
    "pool_size": 10         # Maximum number of connections
}
db.init_app(app)

# Create database tables immediately
with app.app_context():
    try:
        db.create_all()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")

# Initialize the knowledge base and RAG system
knowledge_base = MedicalKnowledgeBase()
headache_rag = HeadacheRAG(knowledge_base)

@app.route("/")
def index():
    """Render the main page"""
    return render_template("index.html")

@app.route("/history")
def history_page():
    """Render the history page"""
    return render_template("history.html")

@app.route("/analyze", methods=["POST"])
def analyze_symptoms():
    """Analyze the headache symptoms using RAG and LLM"""
    symptoms_text = ""
    
    try:
        # Get data from request
        data = request.json
        symptoms_text = data.get("symptoms", "")
        
        if not symptoms_text:
            return jsonify({"error": "No symptoms provided"}), 400
        
        # Process with RAG system
        diagnosis, recommendations = headache_rag.analyze_headache(symptoms_text)
        
        # Save the analysis to the database
        record_id = None
        try:
            record = HeadacheRecord(
                symptoms=symptoms_text,
                diagnosis=diagnosis,
                recommendations=json.dumps(recommendations),
                used_fallback=False
            )
            db.session.add(record)
            db.session.commit()
            record_id = record.id
        except Exception as db_error:
            logger.error(f"Error saving primary analysis to database: {str(db_error)}")
            # Make sure to rollback the session
            try:
                db.session.rollback()
            except:
                pass
        
        return jsonify({
            "diagnosis": diagnosis,
            "recommendations": recommendations,
            "record_id": record_id
        })
    
    except Exception as e:
        logger.error(f"Error in analyze_symptoms: {str(e)}")
        
        # Use fallback analysis with the symptoms we extracted
        fallback_diagnosis, fallback_recommendations = headache_rag.fallback_analysis(symptoms_text)
        
        # Check if it's a quota error
        error_message = str(e)
        is_quota_error = "quota" in error_message.lower() or "429" in error_message
        
        if is_quota_error:
            error_message = "OpenAI API quota exceeded. Using fallback analysis system."
        else:
            error_message = "An error occurred during analysis. Using fallback method."
        
        # Save the fallback analysis to the database
        try:
            # Create a new session for this operation to prevent transaction issues
            with app.app_context():
                # Make sure we have a clean session
                db.session.remove()
                
                record = HeadacheRecord(
                    symptoms=symptoms_text,
                    diagnosis=fallback_diagnosis,
                    recommendations=json.dumps(fallback_recommendations),
                    used_fallback=True
                )
                db.session.add(record)
                db.session.commit()
                record_id = record.id
        except Exception as db_error:
            logger.error(f"Error saving to database: {str(db_error)}")
            # Make sure to rollback the session to avoid future errors
            try:
                db.session.rollback()
            except:
                pass
            record_id = None
            
        # Return a 200 status with fallback data instead of 500
        # This makes it easier for the frontend to handle
        return jsonify({
            "error": error_message,
            "diagnosis": fallback_diagnosis,
            "recommendations": fallback_recommendations,
            "using_fallback": True,
            "record_id": record_id
        }), 200

@app.route("/api/history", methods=["GET"])
def get_headache_history():
    """API endpoint to get the history of headache records as JSON"""
    try:
        # Create a fresh session context to avoid any transaction issues
        with app.app_context():
            # Get all records ordered by most recent first
            records = HeadacheRecord.query.order_by(HeadacheRecord.created_at.desc()).all()
            
            # Format the records for JSON response
            history = []
            for record in records:
                # Handle potential JSON parsing errors
                try:
                    recommendations = json.loads(record.recommendations)
                except:
                    recommendations = ["Error loading recommendations"]
                
                history.append({
                    "id": record.id,
                    "symptoms": record.symptoms,
                    "diagnosis": record.diagnosis,
                    "recommendations": recommendations,
                    "created_at": record.created_at.isoformat(),
                    "used_fallback": record.used_fallback
                })
            
            return jsonify({"history": history})
    
    except Exception as e:
        logger.error(f"Error getting history: {str(e)}")
        # Make sure to close the session
        try:
            db.session.rollback()
        except:
            pass
        return jsonify({"error": "Failed to retrieve headache history"}), 500

@app.route("/health")
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
