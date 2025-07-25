"""
Model Selector for selecting appropriate models based on task.
"""

import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class ModelSelector:
    """
    Selects appropriate models based on task requirements.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Model Selector.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.models = self._load_models()
        logger.info("ModelSelector initialized with %d models", len(self.models))
    
    def _load_models(self) -> Dict[str, Dict[str, Any]]:
        """
        Load available models from configuration.
        
        Returns:
            Dictionary of models
        """
        # In a real implementation, this would load model configurations from a file or database
        # For demonstration, we'll use a hardcoded set of models
        
        return {
            "gpt-4": {
                "type": "llm",
                "provider": "openai",
                "capabilities": ["text_generation", "reasoning", "code_generation"],
                "cost_per_token": 0.01,
                "max_tokens": 8192,
                "performance": 0.95
            },
            "gpt-3.5-turbo": {
                "type": "llm",
                "provider": "openai",
                "capabilities": ["text_generation", "reasoning", "code_generation"],
                "cost_per_token": 0.002,
                "max_tokens": 4096,
                "performance": 0.85
            },
            "text-embedding-ada-002": {
                "type": "embedding",
                "provider": "openai",
                "capabilities": ["embeddings"],
                "cost_per_token": 0.0001,
                "max_tokens": 8191,
                "performance": 0.9
            },
            "local-bert": {
                "type": "embedding",
                "provider": "local",
                "capabilities": ["embeddings"],
                "cost_per_token": 0.0,
                "max_tokens": 512,
                "performance": 0.8
            },
            "local-rules": {
                "type": "rule_engine",
                "provider": "local",
                "capabilities": ["validation", "classification"],
                "cost_per_token": 0.0,
                "performance": 0.75
            }
        }
    
    def select_model(
        self, 
        task_type: str, 
        required_capabilities: List[str], 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Select the most appropriate model for a task.
        
        Args:
            task_type: Type of task
            required_capabilities: List of required capabilities
            context: Optional context information
            
        Returns:
            Selected model configuration
            
        Raises:
            ValueError: If no suitable model is found
        """
        logger.info("Selecting model for task type %s with capabilities %s", 
                   task_type, required_capabilities)
        
        # Filter models by required capabilities
        suitable_models = []
        for model_id, model in self.models.items():
            # Check if model has all required capabilities
            if all(cap in model["capabilities"] for cap in required_capabilities):
                suitable_models.append((model_id, model))
        
        if not suitable_models:
            error_msg = f"No suitable model found for task type {task_type} with capabilities {required_capabilities}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Apply selection strategy based on task type and context
        if context and context.get("optimize_for") == "cost":
            # Select the cheapest model
            selected = min(suitable_models, key=lambda x: x[1].get("cost_per_token", float("inf")))
            logger.info("Selected cheapest model: %s", selected[0])
        elif context and context.get("optimize_for") == "performance":
            # Select the highest performing model
            selected = max(suitable_models, key=lambda x: x[1].get("performance", 0))
            logger.info("Selected highest performing model: %s", selected[0])
        else:
            # Default: balance cost and performance
            # Use a simple scoring function
            def score_model(model_tuple):
                model_id, model = model_tuple
                cost = model.get("cost_per_token", 0.01)  # Default to high cost if not specified
                performance = model.get("performance", 0.5)  # Default to medium performance
                
                # Avoid division by zero
                if cost == 0:
                    cost = 0.0001
                
                # Score = performance / cost (higher is better)
                return performance / cost
            
            selected = max(suitable_models, key=score_model)
            logger.info("Selected balanced model: %s", selected[0])
        
        # Return the selected model with its ID
        result = selected[1].copy()
        result["id"] = selected[0]
        
        return result
    
    def get_model(self, model_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific model by ID.
        
        Args:
            model_id: ID of the model
            
        Returns:
            Model configuration or None if not found
        """
        if model_id in self.models:
            result = self.models[model_id].copy()
            result["id"] = model_id
            return result
        return None
    
    def list_models(
        self, 
        model_type: Optional[str] = None, 
        provider: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List available models, optionally filtered by type or provider.
        
        Args:
            model_type: Optional model type filter
            provider: Optional provider filter
            
        Returns:
            List of matching models
        """
        result = []
        
        for model_id, model in self.models.items():
            # Apply filters
            if model_type and model.get("type") != model_type:
                continue
            if provider and model.get("provider") != provider:
                continue
            
            # Add model to result
            model_copy = model.copy()
            model_copy["id"] = model_id
            result.append(model_copy)
        
        return result