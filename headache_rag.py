import os
import logging
import json
from openai import OpenAI
import numpy as np
from knowledge_base import MedicalKnowledgeBase

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class HeadacheRAG:
    """
    Headache Retrieval Augmented Generation system
    Uses OpenAI API for LLM capabilities and a medical knowledge base for RAG
    """
    
    def __init__(self, knowledge_base):
        """
        Initialize the HeadacheRAG system
        
        Args:
            knowledge_base: A MedicalKnowledgeBase instance
        """
        self.knowledge_base = knowledge_base
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.openai_client = OpenAI(api_key=self.openai_api_key) if self.openai_api_key else None
        
        # Define system prompt
        self.system_prompt = """
        You are a headache diagnosis assistant. Your task is to analyze the user's symptoms 
        and provide a possible diagnosis and recommendations. Remember:
        
        1. You are NOT a doctor and should always include a disclaimer that the user should 
           consult a healthcare professional.
        2. Focus on providing informative, evidence-based responses.
        3. Be clear about the limitations of your diagnosis.
        4. Provide practical recommendations that might help alleviate symptoms.
        5. Format your response as JSON with 'diagnosis' and 'recommendations' fields.
        6. If the symptoms indicate a potentially severe condition (stroke, meningitis, etc.), 
           strongly advise seeking immediate medical attention.
        
        Use the provided context information to formulate your response.
        """
    
    def _embed_text(self, text):
        """
        Embed the text using OpenAI's API (fallback to simple keyword matching if unavailable)
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector or keywords
        """
        try:
            if self.openai_client:
                response = self.openai_client.embeddings.create(
                    model="text-embedding-ada-002",
                    input=text
                )
                return response.data[0].embedding
            else:
                # Simple fallback - extract keywords
                return text.lower().split()
        except Exception as e:
            logger.error(f"Error embedding text: {str(e)}")
            # Fallback to simple keyword extraction
            return text.lower().split()
    
    def _retrieve_relevant_context(self, query_embedding, top_k=3):
        """
        Retrieve the most relevant information from knowledge base
        
        Args:
            query_embedding: Embedding of the query
            top_k: Number of top results to retrieve
            
        Returns:
            Relevant context as a string
        """
        if isinstance(query_embedding, list) and all(isinstance(x, float) for x in query_embedding):
            # Vector embedding - use vector similarity
            results = self.knowledge_base.search_by_vector(query_embedding, top_k)
        else:
            # Keyword list - use keyword matching
            results = self.knowledge_base.search_by_keywords(query_embedding, top_k)
            
        return "\n\n".join(results)
    
    def _generate_response(self, symptoms, context):
        """
        Generate a response using OpenAI's API
        
        Args:
            symptoms: User's symptoms
            context: Retrieved medical knowledge context
            
        Returns:
            Generated diagnosis and recommendations
        """
        try:
            if not self.openai_client:
                raise ValueError("OpenAI API key not available")
                
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Symptoms: {symptoms}\n\nContext: {context}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.5,
                max_tokens=1000
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get("diagnosis"), result.get("recommendations")
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise
    
    def analyze_headache(self, symptoms):
        """
        Analyze headache symptoms using RAG
        
        Args:
            symptoms: User's description of headache symptoms
            
        Returns:
            Diagnosis and recommendations
        """
        try:
            # Embed the symptoms
            query_embedding = self._embed_text(symptoms)
            
            # Retrieve relevant context
            context = self._retrieve_relevant_context(query_embedding)
            
            # Generate response
            diagnosis, recommendations = self._generate_response(symptoms, context)
            
            return diagnosis, recommendations
            
        except Exception as e:
            logger.error(f"Error in analyze_headache: {str(e)}")
            # Use fallback method and include the error
            return self.fallback_analysis(symptoms)
    
    def fallback_analysis(self, symptoms):
        """
        Fallback method for when the API fails
        
        Args:
            symptoms: User's description of headache symptoms
            
        Returns:
            Tuple of (diagnosis, recommendations)
        """
        # Simple keyword-based analysis
        keywords = symptoms.lower()
        diagnosis = "Based on the limited analysis available due to system constraints, "
        recommendations = ["Please consult a healthcare professional for accurate diagnosis."]
        
        # Very basic pattern matching
        if "migraine" in keywords or "aura" in keywords or "one side" in keywords:
            diagnosis += "your symptoms suggest a possible migraine."
            recommendations.extend([
                "Rest in a quiet, dark room",
                "Apply cold or warm compress",
                "Stay hydrated",
                "Over-the-counter pain medication may help (follow package instructions)"
            ])
        elif "cluster" in keywords or "eye pain" in keywords or "one eye" in keywords:
            diagnosis += "your symptoms have some similarities with cluster headaches."
            recommendations.extend([
                "Consult a doctor immediately as cluster headaches often need prescription medication",
                "Oxygen therapy might help (requires medical supervision)",
                "Avoid alcohol during headache periods"
            ])
        elif "tension" in keywords or "stress" in keywords or "tight" in keywords or "pressure" in keywords:
            diagnosis += "your symptoms are consistent with tension headaches."
            recommendations.extend([
                "Stress management techniques like meditation",
                "Gentle neck and shoulder stretches",
                "Regular breaks from screen time",
                "Over-the-counter pain relievers if needed"
            ])
        elif "sudden" in keywords and ("severe" in keywords or "worst" in keywords):
            diagnosis += "your symptoms could indicate a serious condition requiring IMMEDIATE medical attention."
            recommendations = [
                "SEEK EMERGENCY CARE IMMEDIATELY",
                "Call emergency services or go to the nearest emergency room",
                "Do not drive yourself if experiencing severe symptoms"
            ]
        else:
            diagnosis += "I cannot determine a specific type of headache from the information provided."
            recommendations.extend([
                "Track your symptoms and potential triggers",
                "Stay hydrated and get adequate sleep",
                "Consider over-the-counter pain relief if appropriate"
            ])
        
        # Always include this disclaimer
        recommendations.append("IMPORTANT: This is not a medical diagnosis. Always consult healthcare professionals for proper evaluation.")
        
        return diagnosis, recommendations
