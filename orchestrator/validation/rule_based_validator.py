"""
Rule-Based Validator for applying predefined rules to validate outputs.
"""

import logging
import asyncio
from typing import Dict, Any, List, Optional, Callable

logger = logging.getLogger(__name__)

class RuleBasedValidator:
    """
    Applies predefined rules to validate agent outputs.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Rule-Based Validator.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.rules = {}
        self._register_default_rules()
        logger.info("RuleBasedValidator initialized with %d rules", len(self.rules))
    
    def _register_default_rules(self):
        """Register default validation rules."""
        # Register data extraction rules
        self.register_rule("DataExtractionAgent", "extract_data", self._validate_extraction_result)
        
        # Register statistical analysis rules
        self.register_rule("StatisticalAnalysisAgent", "analyze_data", self._validate_analysis_result)
        
        # Register visualization rules
        self.register_rule("VisualizationAgent", "create_visualizations", self._validate_visualization_result)
    
    def register_rule(self, agent_name: str, task_name: str, rule_func: Callable):
        """
        Register a validation rule for a specific agent and task.
        
        Args:
            agent_name: Name of the agent
            task_name: Name of the task
            rule_func: Validation function that returns (is_valid, score, message)
        """
        key = f"{agent_name}:{task_name}"
        self.rules[key] = rule_func
        logger.info("Registered rule for %s", key)
    
    async def validate(
        self, 
        agent_name: str, 
        task_name: str, 
        task_input: Dict[str, Any], 
        task_output: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate a task output using registered rules.
        
        Args:
            agent_name: Name of the agent that produced the output
            task_name: Name of the task that was executed
            task_input: Input data for the task
            task_output: Output data from the task
            
        Returns:
            Validation result with is_valid flag, confidence score, and message
        """
        key = f"{agent_name}:{task_name}"
        rule_func = self.rules.get(key)
        
        if not rule_func:
            logger.warning("No rule found for %s", key)
            return {
                "is_valid": True,  # Default to valid if no rule exists
                "confidence": 50.0,  # Neutral confidence
                "message": f"No validation rule defined for {key}"
            }
        
        logger.info("Validating %s using rule-based validator", key)

        # Apply the rule
        is_valid, confidence, message = await rule_func(task_input, task_output)
        
        logger.info("Validation result for %s: valid=%s, confidence=%f, message=%s", 
                   key, is_valid, confidence, message)
        
        return {
            "is_valid": is_valid,
            "confidence": confidence,
            "message": message
        }
    
    async def _validate_extraction_result(
        self, 
        task_input: Dict[str, Any], 
        task_output: Dict[str, Any]
    ) -> tuple:
        """
        Validate data extraction results.
        
        Args:
            task_input: Input data for the task
            task_output: Output data from the task
            
        Returns:
            Tuple of (is_valid, confidence_score, message)
        """
        # Check if data is present
        if "data" not in task_output:
            return False, 0.0, "Missing 'data' field in extraction result"
        
        data = task_output.get("data", [])
        
        # Check if data is empty
        if not data:
            return False, 30.0, "Extracted data is empty"
        
        # Check if metadata is present
        if "metadata" not in task_output:
            return True, 70.0, "Data present but missing metadata"
        
        # Check metadata fields
        metadata = task_output.get("metadata", {})
        required_fields = ["source", "record_count", "extraction_timestamp"]
        missing_fields = [field for field in required_fields if field not in metadata]
        
        if missing_fields:
            return True, 80.0, f"Metadata missing fields: {', '.join(missing_fields)}"
        
        # All checks passed
        return True, 95.0, "Extraction result is valid"
    
    async def _validate_analysis_result(
        self, 
        task_input: Dict[str, Any], 
        task_output: Dict[str, Any]
    ) -> tuple:
        """
        Validate statistical analysis results.
        
        Args:
            task_input: Input data for the task
            task_output: Output data from the task
            
        Returns:
            Tuple of (is_valid, confidence_score, message)
        """
        # Check if analysis_results is present
        if "analysis_results" not in task_output:
            return False, 0.0, "Missing 'analysis_results' field in analysis result"
        
        analysis_results = task_output.get("analysis_results", {})
        
        # Check if analysis_results is empty
        if not analysis_results:
            return False, 30.0, "Analysis results are empty"
        
        # Check if metadata is present
        if "metadata" not in task_output:
            return True, 70.0, "Analysis results present but missing metadata"
        
        # Check metadata fields
        metadata = task_output.get("metadata", {})
        required_fields = ["analysis_timestamp", "analysis_methods"]
        missing_fields = [field for field in required_fields if field not in metadata]
        
        if missing_fields:
            return True, 80.0, f"Metadata missing fields: {', '.join(missing_fields)}"
        
        # All checks passed
        return True, 95.0, "Analysis result is valid"
    
    async def _validate_visualization_result(
        self, 
        task_input: Dict[str, Any], 
        task_output: Dict[str, Any]
    ) -> tuple:
        """
        Validate visualization results.
        
        Args:
            task_input: Input data for the task
            task_output: Output data from the task
            
        Returns:
            Tuple of (is_valid, confidence_score, message)
        """
        # Check if visualizations is present
        if "visualizations" not in task_output:
            return False, 0.0, "Missing 'visualizations' field in visualization result"
        
        visualizations = task_output.get("visualizations", [])
        
        # Check if visualizations is empty
        if not visualizations:
            return False, 30.0, "No visualizations generated"
        
        # Check required fields in each visualization
        required_fields = ["id", "title", "type", "data"]
        invalid_visualizations = []
        
        for i, viz in enumerate(visualizations):
            missing_fields = [field for field in required_fields if field not in viz]
            if missing_fields:
                invalid_visualizations.append(f"Visualization {i+1} missing fields: {', '.join(missing_fields)}")
        
        if invalid_visualizations:
            return True, 60.0, f"Some visualizations are invalid: {'; '.join(invalid_visualizations)}"
        
        # Check if metadata is present
        if "metadata" not in task_output:
            return True, 80.0, "Visualizations present but missing metadata"
        
        # All checks passed
        return True, 95.0, "Visualization result is valid"