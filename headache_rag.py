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
        # Simple keyword-based analysis with improved pattern matching
        keywords = symptoms.lower()
        diagnosis = "Based on the pattern matching analysis of your symptoms, "
        recommendations = ["Please consult a healthcare professional for proper diagnosis."]
        
        # Break all words into single words and check for individual term matches
        # This improves detection when users don't use exact phrases
        keywords_list = keywords.split()
        
        # More comprehensive pattern matching with broader detection
        migraine_keywords = ["migraine", "aura", "one", "side", "throbbing", "pulsing", "nausea", 
                           "vomit", "light", "sensitive", "sensitivity", "sound", "visual", 
                           "blind", "spot", "half", "head", "worse", "pounding", "pound"]
        tension_keywords = ["tension", "stress", "tight", "pressure", "band", "squeezing", 
                          "both", "sides", "constant", "dull", "neck", "shoulders", "front", "back"]
        cluster_keywords = ["cluster", "eye", "pain", "severe", "burning", 
                          "piercing", "one", "side", "runny", "nose", "teary", "night", "sharp"]
        sinus_keywords = ["sinus", "face", "pain", "congestion", "stuffy", "mucus", 
                         "cheeks", "forehead", "bending", "worse", "lying", "nose"]
        emergency_keywords = ["sudden", "severe", "worst", "thunderclap", "stiff", "neck", 
                            "fever", "confusion", "speech", "weakness", "numb", "seizure", "vision", "loss", "vomiting"]
        
        # Count keyword matches for each type (word by word)
        migraine_count = sum(1 for word in migraine_keywords if word in keywords_list)
        tension_count = sum(1 for word in tension_keywords if word in keywords_list)
        cluster_count = sum(1 for word in cluster_keywords if word in keywords_list)
        sinus_count = sum(1 for word in sinus_keywords if word in keywords_list)
        emergency_count = sum(1 for word in emergency_keywords if word in keywords_list)
        
        # Add specific phrase checks that are important for diagnosis
        if "one side" in keywords or ("one" in keywords_list and "side" in keywords_list):
            migraine_count += 2  # This is a strong indicator of migraine
            
        if "both sides" in keywords or ("both" in keywords_list and "sides" in keywords_list):
            tension_count += 2  # This is a strong indicator of tension headache
            
        if "light sensitive" in keywords or "sensitivity to light" in keywords or "worse with light" in keywords:
            migraine_count += 2  # Another strong migraine indicator
        
        # Check for possible emergency conditions first
        if emergency_count >= 2 and any(word in keywords_list for word in ["worst", "sudden", "severe"]):
            diagnosis = "Your symptoms suggest a potentially serious condition that requires IMMEDIATE medical attention."
            recommendations = [
                "⚠️ SEEK EMERGENCY CARE IMMEDIATELY",
                "Call emergency services or go to the nearest emergency room",
                "Do not drive yourself if experiencing severe symptoms",
                "IMPORTANT: This is not a medical diagnosis. Please seek professional medical help immediately."
            ]
            return diagnosis, recommendations
        
        # Determine most likely headache type based on keyword count
        headache_types = [
            (migraine_count, "migraine", [
                "Rest in a quiet, dark room",
                "Apply cold or warm compress to the forehead or neck",
                "Stay well hydrated",
                "Over-the-counter pain medications such as ibuprofen may help (follow package instructions)",
                "Track potential triggers like certain foods, stress, or hormonal changes"
            ]),
            (tension_count, "tension headache", [
                "Practice stress management techniques like deep breathing or meditation",
                "Take regular breaks from screen time and work",
                "Apply gentle stretching to neck and shoulder muscles",
                "Consider over-the-counter pain relievers if appropriate",
                "Maintain good posture, especially when working at a desk"
            ]),
            (cluster_count, "cluster headache", [
                "Consult a doctor promptly as cluster headaches often require prescription medication",
                "Oxygen therapy might help (requires medical supervision)",
                "Avoid alcohol consumption during headache periods",
                "Keep a regular sleep schedule",
                "Avoid smoking and tobacco products"
            ]),
            (sinus_count, "sinus headache", [
                "Use a saline nasal spray to clear congestion",
                "Apply warm compresses to painful sinus areas",
                "Stay hydrated to thin mucus secretions",
                "Consider over-the-counter decongestants (follow package instructions)",
                "Use a humidifier, especially when sleeping"
            ])
        ]
        
        # Find the headache type with the most keyword matches
        headache_types.sort(reverse=True)
        max_count, headache_type, headache_recommendations = headache_types[0]
        
        # If we have a reasonable match (at least 2 keyword matches)
        if max_count >= 2:
            diagnosis += f"your symptoms are consistent with a {headache_type}."
            recommendations.extend(headache_recommendations)
        else:
            diagnosis += "I cannot determine a specific type of headache from the information provided."
            recommendations.extend([
                "Keep a headache diary to track symptoms, duration, and potential triggers",
                "Ensure you're staying hydrated and getting adequate sleep",
                "Consider over-the-counter pain relief if appropriate",
                "Pay attention to potential environmental triggers like bright lights, strong smells, or certain foods"
            ])
        
        # Always include this disclaimer
        recommendations.append("IMPORTANT: This is not a medical diagnosis. Always consult healthcare professionals for proper evaluation.")
        
        return diagnosis, recommendations
