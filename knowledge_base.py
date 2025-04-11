import numpy as np
import logging
from medical_knowledge.headache_data import HEADACHE_KNOWLEDGE

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MedicalKnowledgeBase:
    """
    A simple medical knowledge base focusing on headaches
    
    This class provides storage and retrieval mechanisms for medical knowledge,
    with both vector-based and keyword-based search capabilities.
    """
    
    def __init__(self):
        """Initialize the knowledge base with predefined headache information"""
        self.knowledge_entries = HEADACHE_KNOWLEDGE
        # Initialize empty vectors - will be populated on first use
        self.vectors = None
        
    def _calculate_similarity(self, query_vector, entry_vector):
        """
        Calculate cosine similarity between two vectors
        
        Args:
            query_vector: Query embedding
            entry_vector: Entry embedding
            
        Returns:
            Similarity score (0-1)
        """
        # Normalize vectors
        query_norm = query_vector / np.linalg.norm(query_vector)
        entry_norm = entry_vector / np.linalg.norm(entry_vector)
        
        # Calculate cosine similarity
        return np.dot(query_norm, entry_norm)
    
    def _get_entry_vectors(self):
        """
        Get or create entry vectors
        
        Returns:
            List of entry vectors
        """
        if self.vectors is None:
            # Initialize with random vectors as placeholders
            # In a real implementation, these would be actual embeddings
            self.vectors = [np.random.randn(1536) for _ in self.knowledge_entries]
        
        return self.vectors
    
    def search_by_vector(self, query_vector, top_k=3):
        """
        Search the knowledge base using vector similarity
        
        Args:
            query_vector: Embedding of the query
            top_k: Number of top results to return
            
        Returns:
            List of relevant knowledge entries
        """
        try:
            entry_vectors = self._get_entry_vectors()
            
            # Calculate similarities
            similarities = [self._calculate_similarity(query_vector, entry_vector) 
                           for entry_vector in entry_vectors]
            
            # Get indices of top k entries
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            # Return top entries
            return [self.knowledge_entries[i] for i in top_indices]
            
        except Exception as e:
            logger.error(f"Error in search_by_vector: {str(e)}")
            # Fallback to keyword search
            if isinstance(query_vector, list) and len(query_vector) > 0:
                # Convert embedding to keywords by just using the symptoms text
                return self.search_by_keywords(["headache", "pain"], top_k)
            return self.knowledge_entries[:min(top_k, len(self.knowledge_entries))]
    
    def search_by_keywords(self, keywords, top_k=3):
        """
        Search the knowledge base using keyword matching
        
        Args:
            keywords: List of keywords to match
            top_k: Number of top results to return
            
        Returns:
            List of relevant knowledge entries
        """
        try:
            # Simple keyword matching - count keyword occurrences
            matches = []
            
            for entry in self.knowledge_entries:
                entry_lower = entry.lower()
                score = sum(1 for keyword in keywords if keyword in entry_lower)
                matches.append((entry, score))
            
            # Sort by score
            matches.sort(key=lambda x: x[1], reverse=True)
            
            # Return top entries
            return [entry for entry, _ in matches[:top_k]]
            
        except Exception as e:
            logger.error(f"Error in search_by_keywords: {str(e)}")
            return self.knowledge_entries[:min(top_k, len(self.knowledge_entries))]
