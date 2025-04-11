import os
import logging
import json
from flask import Flask, render_template, request, jsonify
from headache_rag import HeadacheRAG
from knowledge_base import MedicalKnowledgeBase

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Initialize the knowledge base and RAG system
knowledge_base = MedicalKnowledgeBase()
headache_rag = HeadacheRAG(knowledge_base)

@app.route("/")
def index():
    """Render the main page"""
    return render_template("index.html")

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
        
        return jsonify({
            "diagnosis": diagnosis,
            "recommendations": recommendations
        })
    
    except Exception as e:
        logger.error(f"Error in analyze_symptoms: {str(e)}")
        
        # Use fallback analysis with the symptoms we extracted
        fallback_diagnosis, fallback_recommendations = headache_rag.fallback_analysis(symptoms_text)
        
        # Check if it's a quota error
        error_message = str(e)
        if "quota" in error_message.lower() or "429" in error_message:
            error_message = "OpenAI API quota exceeded. Using fallback analysis system."
        else:
            error_message = "An error occurred during analysis. Using fallback method."
            
        # Return a 200 status with fallback data instead of 500
        # This makes it easier for the frontend to handle
        return jsonify({
            "error": error_message,
            "diagnosis": fallback_diagnosis,
            "recommendations": fallback_recommendations,
            "using_fallback": True
        }), 200

@app.route("/health")
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
