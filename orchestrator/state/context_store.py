"""
Context Store for maintaining conversation context.
"""

import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class ContextStore:
    """
    Maintains conversation context across interactions.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Context Store.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.store = {}
        self.max_context_size = self.config.get("max_context_size", 1000)
        logger.info("ContextStore initialized with max size: %d", self.max_context_size)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the context store.
        
        Args:
            key: Context key
            value: Value to store
        """
        # Check if we need to evict entries
        if len(self.store) >= self.max_context_size and key not in self.store:
            # Simple LRU: just remove a random entry
            # In a real implementation, this would use a proper LRU strategy
            import random
            keys = list(self.store.keys())
            key_to_remove = random.choice(keys)
            del self.store[key_to_remove]
            logger.info("Context store full, evicted an entry")
        
        # Store the value
        self.store[key] = value
        logger.debug("Set context %s", key)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the context store.
        
        Args:
            key: Context key
            default: Default value if key not found
            
        Returns:
            Stored value or default
        """
        value = self.store.get(key, default)
        logger.debug("Get context %s: %s", key, "found" if value is not default else "not found")
        return value
    
    def delete(self, key: str) -> None:
        """
        Delete a value from the context store.
        
        Args:
            key: Context key
        """
        if key in self.store:
            del self.store[key]
            logger.debug("Deleted context %s", key)
    
    def clear(self) -> None:
        """Clear the entire context store."""
        self.store = {}
        logger.info("Context store cleared")
    
    def get_keys(self, prefix: Optional[str] = None) -> List[str]:
        """
        Get all keys in the context store, optionally filtered by prefix.
        
        Args:
            prefix: Optional key prefix filter
            
        Returns:
            List of matching keys
        """
        if prefix:
            return [k for k in self.store.keys() if k.startswith(prefix)]
        else:
            return list(self.store.keys())
    
    def get_context_size(self) -> int:
        """
        Get the current size of the context store.
        
        Returns:
            Number of entries in the context store
        """
        return len(self.store)