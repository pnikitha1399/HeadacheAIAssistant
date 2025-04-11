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
    try:
        # Get data from request
        data = request.json
        symptoms = data.get("symptoms", "")
        
        if not symptoms:
            return jsonify({"error": "No symptoms provided"}), 400
        
        # Process with RAG system
        diagnosis, recommendations = headache_rag.analyze_headache(symptoms)
        
        return jsonify({
            "diagnosis": diagnosis,
            "recommendations": recommendations
        })
    
    except Exception as e:
        logger.error(f"Error in analyze_symptoms: {str(e)}")
        return jsonify({"error": "An error occurred during analysis. Using fallback method.", 
                        "fallback_response": headache_rag.fallback_analysis(symptoms)}), 500

@app.route("/health")
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
