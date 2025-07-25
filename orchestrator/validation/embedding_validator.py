"""
Embedding Validator for using vector embeddings to validate outputs.
"""

import logging
import asyncio
import random
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger(__name__)

class EmbeddingValidator:
    """
    Uses vector embeddings for semantic validation of agent outputs.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Embedding Validator.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.embedding_cache = {}
        logger.info("EmbeddingValidator initialized")
    
    async def validate(
        self, 
        agent_name: str, 
        task_name: str, 
        task_input: Dict[str, Any], 
        task_output: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate a task output using semantic similarity to known good patterns.
        
        Args:
            agent_name: Name of the agent that produced the output
            task_name: Name of the task that was executed
            task_input: Input data for the task
            task_output: Output data from the task
            
        Returns:
            Validation result with similarity score and confidence
        """
        logger.info("Validating %s.%s using embedding validator", agent_name, task_name)
        
        # In a real implementation, this would:
        # 1. Convert the task output to a vector embedding
        # 2. Compare it to known good patterns in a vector database
        # 3. Return similarity scores and confidence
        
        # For demonstration, we'll simulate this process
        await asyncio.sleep(0.5)  # Simulate embedding computation
        
        # Get embeddings for the output
        output_embedding = await self._get_embedding(task_output)
        
        # Get reference embeddings for this agent and task
        reference_embeddings = await self._get_reference_embeddings(agent_name, task_name)
        
        # Calculate similarity scores
        similarities = []
        for ref_name, ref_embedding in reference_embeddings:
            similarity = self._calculate_similarity(output_embedding, ref_embedding)
            similarities.append((ref_name, similarity))
        
        # Find the best match
        best_match = max(similarities, key=lambda x: x[1]) if similarities else ("none", 0.0)
        
        # Calculate confidence based on similarity
        confidence = best_match[1] * 100.0
        
        logger.info("Best match: %s with similarity %f", best_match[0], best_match[1])
        
        return {
            "similarity_score": best_match[1],
            "confidence": confidence,
            "best_match": best_match[0],
            "all_similarities": similarities
        }
    
    async def _get_embedding(self, data: Dict[str, Any]) -> List[float]:
        """
        Get vector embedding for data.
        
        Args:
            data: Data to embed
            
        Returns:
            Vector embedding
        """
        # In a real implementation, this would use a model to generate embeddings
        # For demonstration, we'll generate a random vector
        
        # Use a hash of the data as a cache key
        import hashlib
        import json
        
        data_str = json.dumps(data, sort_keys=True)
        cache_key = hashlib.md5(data_str.encode()).hexdigest()
        
        # Check if we have a cached embedding
        if cache_key in self.embedding_cache:
            return self.embedding_cache[cache_key]
        
        # Generate a random embedding (in a real system, this would use a model)
        embedding_dim = 128
        embedding = [random.uniform(-1.0, 1.0) for _ in range(embedding_dim)]
        
        # Normalize the embedding
        magnitude = sum(x**2 for x in embedding) ** 0.5
        if magnitude > 0:
            embedding = [x / magnitude for x in embedding]
        
        # Cache the embedding
        self.embedding_cache[cache_key] = embedding
        
        return embedding
    
    async def _get_reference_embeddings(
        self, 
        agent_name: str, 
        task_name: str
    ) -> List[Tuple[str, List[float]]]:
        """
        Get reference embeddings for a specific agent and task.
        
        Args:
            agent_name: Name of the agent
            task_name: Name of the task
            
        Returns:
            List of (name, embedding) tuples
        """
        # In a real implementation, this would retrieve embeddings from a database
        # For demonstration, we'll generate random embeddings
        
        # Generate a few reference embeddings
        references = []
        
        for i in range(3):
            name = f"{agent_name}_{task_name}_reference_{i+1}"
            embedding_dim = 128
            embedding = [random.uniform(-1.0, 1.0) for _ in range(embedding_dim)]
            
            # Normalize the embedding
            magnitude = sum(x**2 for x in embedding) ** 0.5
            if magnitude > 0:
                embedding = [x / magnitude for x in embedding]
            
            references.append((name, embedding))
        
        return references
    
    def _calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calculate cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding
            embedding2: Second embedding
            
        Returns:
            Cosine similarity (-1 to 1)
        """
        # Check if embeddings have the same dimension
        if len(embedding1) != len(embedding2):
            logger.warning("Embeddings have different dimensions: %d vs %d", 
                          len(embedding1), len(embedding2))
            return 0.0
        
        # Calculate dot product
        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
        
        # Calculate magnitudes
        magnitude1 = sum(x**2 for x in embedding1) ** 0.5
        magnitude2 = sum(x**2 for x in embedding2) ** 0.5
        
        # Calculate cosine similarity
        if magnitude1 > 0 and magnitude2 > 0:
            similarity = dot_product / (magnitude1 * magnitude2)
        else:
            similarity = 0.0
        
        # Ensure similarity is within bounds
        similarity = max(-1.0, min(1.0, similarity))
        
        return similarity