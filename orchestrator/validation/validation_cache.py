"""
Validation Cache for storing and retrieving validation results.
"""

import logging
import json
import hashlib
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

class ValidationCache:
    """
    Caches validation results to avoid redundant processing.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Validation Cache.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.cache = {}
        self.max_cache_size = self.config.get("max_cache_size", 1000)
        logger.info("ValidationCache initialized with max size: %d", self.max_cache_size)
    
    def get(
        self, 
        agent_name: str, 
        task_name: str, 
        task_input: Dict[str, Any], 
        task_output: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Get cached validation result if available.
        
        Args:
            agent_name: Name of the agent
            task_name: Name of the task
            task_input: Input data for the task
            task_output: Output data from the task
            
        Returns:
            Cached validation result or None if not found
        """
        cache_key = self._generate_cache_key(agent_name, task_name, task_input, task_output)
        
        if cache_key in self.cache:
            logger.info("Cache hit for %s.%s", agent_name, task_name)
            return self.cache[cache_key]
        
        logger.info("Cache miss for %s.%s", agent_name, task_name)
        return None
    
    def store(
        self, 
        agent_name: str, 
        task_name: str, 
        task_input: Dict[str, Any], 
        task_output: Dict[str, Any], 
        validation_result: Dict[str, Any]
    ) -> None:
        """
        Store validation result in cache.
        
        Args:
            agent_name: Name of the agent
            task_name: Name of the task
            task_input: Input data for the task
            task_output: Output data from the task
            validation_result: Validation result to cache
        """
        cache_key = self._generate_cache_key(agent_name, task_name, task_input, task_output)
        
        # Check if we need to evict entries
        if len(self.cache) >= self.max_cache_size:
            # Simple LRU: just remove a random entry
            # In a real implementation, this would use a proper LRU strategy
            import random
            keys = list(self.cache.keys())
            key_to_remove = random.choice(keys)
            del self.cache[key_to_remove]
            logger.info("Cache full, evicted an entry")
        
        # Store the result
        self.cache[cache_key] = validation_result
        logger.info("Stored validation result in cache for %s.%s", agent_name, task_name)
    
    def clear(self) -> None:
        """Clear the entire cache."""
        self.cache = {}
        logger.info("Validation cache cleared")
    
    def _generate_cache_key(
        self, 
        agent_name: str, 
        task_name: str, 
        task_input: Dict[str, Any], 
        task_output: Dict[str, Any]
    ) -> str:
        """
        Generate a cache key for the given parameters.
        
        Args:
            agent_name: Name of the agent
            task_name: Name of the task
            task_input: Input data for the task
            task_output: Output data from the task
            
        Returns:
            Cache key string
        """
        # Create a string representation of the parameters
        key_parts = [
            f"agent={agent_name}",
            f"task={task_name}",
            f"input={json.dumps(task_input, sort_keys=True)}",
            f"output={json.dumps(task_output, sort_keys=True)}"
        ]
        key_string = "|".join(key_parts)
        
        # Hash the string to create a fixed-length key
        return hashlib.md5(key_string.encode()).hexdigest()