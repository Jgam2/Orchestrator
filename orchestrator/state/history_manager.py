"""
History Manager for tracking interaction history.
"""

import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class HistoryManager:
    """
    Tracks interaction history.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the History Manager.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.history = []
        self.max_history_size = self.config.get("max_history_size", 1000)
        logger.info("HistoryManager initialized with max size: %d", self.max_history_size)
    
    def add_entry(self, entry: Dict[str, Any]) -> None:
        """
        Add an entry to the history.
        
        Args:
            entry: History entry to add
        """
        # Ensure the entry has a timestamp
        if "timestamp" not in entry:
            entry["timestamp"] = self.get_timestamp()
        
        # Add the entry
        self.history.append(entry)
        
        # Trim history if needed
        if len(self.history) > self.max_history_size:
            self.history = self.history[-self.max_history_size:]
            logger.info("History trimmed to max size")
        
        logger.debug("Added history entry: %s", entry.get("type", "unknown"))
    
    def get_entries(
        self, 
        entry_type: Optional[str] = None, 
        limit: Optional[int] = None, 
        reverse: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get history entries, optionally filtered by type.
        
        Args:
            entry_type: Optional entry type filter
            limit: Optional limit on number of entries
            reverse: Whether to return entries in reverse order (newest first)
            
        Returns:
            List of matching history entries
        """
        # Filter by type if specified
        if entry_type:

            entries = [e for e in self.history if e.get("type") == entry_type]
        else:
            entries = self.history.copy()
        
        # Reverse if requested
        if reverse:
            entries = entries[::-1]
        
        # Apply limit if specified
        if limit is not None:
            entries = entries[:limit]
        
        return entries
    
    def clear_history(self) -> None:
        """Clear the entire history."""
        self.history = []
        logger.info("History cleared")
    
    def get_history_size(self) -> int:
        """
        Get the current size of the history.
        
        Returns:
            Number of entries in the history
        """
        return len(self.history)
    
    def get_timestamp(self) -> str:
        """
        Get the current timestamp as a string.
        
        Returns:
            Current timestamp string
        """
        from datetime import datetime
        return datetime.now().isoformat()