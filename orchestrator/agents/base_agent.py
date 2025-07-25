"""
Base agent class that all specialized agents inherit from.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class Agent(ABC):
    """
    Abstract base class for all agents in the system.
    """
    
    def __init__(self, name: str = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the agent.
        
        Args:
            name: Name of the agent
            config: Configuration dictionary for the agent
        """
        self.name = name or self.__class__.__name__
        self.config = config or {}
        self.supported_tasks = self._get_supported_tasks()
        logger.info("Agent %s initialized with %d supported tasks", self.name, len(self.supported_tasks))
    
    @abstractmethod
    def _get_supported_tasks(self) -> List[str]:
        """
        Get the list of tasks supported by this agent.
        
        Returns:
            List of task names
        """
        pass
    
    async def execute_task(self, task_name: str, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task with the given input.
        
        Args:
            task_name: Name of the task to execute
            task_input: Input data for the task
            
        Returns:
            The result of the task execution
            
        Raises:
            ValueError: If the task is not supported by this agent
        """
        if task_name not in self.supported_tasks:
            raise ValueError(f"Task {task_name} not supported by agent {self.name}")
        
        logger.info("Agent %s executing task %s", self.name, task_name)
        
        # Get the task method
        task_method = getattr(self, task_name)
        
        # Execute the task
        result = await task_method(task_input)
        
        logger.info("Agent %s completed task %s", self.name, task_name)
        return result