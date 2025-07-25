"""
HITL Manager for coordinating human-in-the-loop interactions.
"""

import logging
import asyncio
from typing import Dict, Any, Optional, Callable

from orchestrator.state.context_store import ContextStore
from orchestrator.state.history_manager import HistoryManager

logger = logging.getLogger(__name__)

class HITLManager:
    """
    Manages human-in-the-loop interactions when confidence is low.
    """
    
    def __init__(
        self, 
        context_store: ContextStore, 
        history_manager: HistoryManager,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the HITL Manager.
        
        Args:
            context_store: Context store for maintaining conversation state
            history_manager: History manager for tracking interactions
            config: Configuration dictionary
        """
        self.context_store = context_store
        self.history_manager = history_manager
        self.config = config or {}
        self.interaction_handlers = {}
        self._register_default_handlers()
        logger.info("HITLManager initialized")
    
    def _register_default_handlers(self):
        """Register default interaction handlers."""
        # Register handlers for different agent types
        self.register_handler("DataExtractionAgent", self._handle_data_extraction_hitl)
        self.register_handler("StatisticalAnalysisAgent", self._handle_analysis_hitl)
        self.register_handler("VisualizationAgent", self._handle_visualization_hitl)
    
    def register_handler(self, agent_name: str, handler_func: Callable):
        """
        Register a HITL handler for a specific agent.
        
        Args:
            agent_name: Name of the agent
            handler_func: Handler function for HITL interactions
        """
        self.interaction_handlers[agent_name] = handler_func
        logger.info("Registered HITL handler for %s", agent_name)
    
    async def process(
        self, 
        agent_name: str, 
        task_name: str, 
        task_input: Dict[str, Any], 
        task_output: Dict[str, Any], 
        confidence_score: float
    ) -> Dict[str, Any]:
        """
        Process a HITL request.
        
        Args:
            agent_name: Name of the agent that produced the output
            task_name: Name of the task that was executed
            task_input: Input data for the task
            task_output: Output data from the task
            confidence_score: Confidence score from the evaluator
            
        Returns:
            Updated task output after human intervention
        """
        logger.info("Processing HITL request for %s.%s with confidence %f", 
                   agent_name, task_name, confidence_score)
        
        # Record the HITL request
        self.history_manager.add_entry({
            "type": "hitl_request",
            "agent": agent_name,
            "task": task_name,
            "confidence_score": confidence_score,
            "timestamp": self.history_manager.get_timestamp()
        })
        
        # Get the appropriate handler
        handler = self.interaction_handlers.get(agent_name)
        if not handler:
            logger.warning("No HITL handler for %s, using default handler", agent_name)
            handler = self._default_hitl_handler
        
        # Process the HITL request
        updated_output = await handler(task_name, task_input, task_output, confidence_score)
        
        # Record the HITL response
        self.history_manager.add_entry({
            "type": "hitl_response",
            "agent": agent_name,
            "task": task_name,
            "timestamp": self.history_manager.get_timestamp()
        })
        
        logger.info("HITL processing completed for %s.%s", agent_name, task_name)
        return updated_output
    
    async def _default_hitl_handler(
        self, 
        task_name: str, 
        task_input: Dict[str, Any], 
        task_output: Dict[str, Any], 
        confidence_score: float
    ) -> Dict[str, Any]:
        """
        Default HITL handler when no specific handler is registered.
        
        Args:
            task_name: Name of the task that was executed
            task_input: Input data for the task
            task_output: Output data from the task
            confidence_score: Confidence score from the evaluator
            
        Returns:
            Updated task output after human intervention
        """
        logger.info("Using default HITL handler for task %s", task_name)
        
        # In a real implementation, this would interact with a human
        # For demonstration, we'll simulate a human response
        
        # Simulate human review time
        await asyncio.sleep(2.0)
        
        # Simulate human verification (just return the original output with a flag)
        updated_output = task_output.copy()
        updated_output["hitl_verified"] = True
        updated_output["hitl_timestamp"] = self.history_manager.get_timestamp()
        
        return updated_output
    
    async def _handle_data_extraction_hitl(
        self, 
        task_name: str, 
        task_input: Dict[str, Any], 
        task_output: Dict[str, Any], 
        confidence_score: float
    ) -> Dict[str, Any]:
        """
        Handle HITL for data extraction tasks.
        
        Args:
            task_name: Name of the task that was executed
            task_input: Input data for the task
            task_output: Output data from the task
            confidence_score: Confidence score from the evaluator
            
        Returns:
            Updated task output after human intervention
        """
        logger.info("Handling data extraction HITL for task %s", task_name)
        
        # In a real implementation, this would:
        # 1. Present the extracted data to a human
        # 2. Allow them to correct or verify it
        # 3. Return the corrected data
        
        # For demonstration, we'll simulate human corrections
        
        # Simulate human review time
        await asyncio.sleep(1.5)
        
        # Create a copy of the output to modify
        updated_output = task_output.copy()
        
        # Simulate human corrections
        if "data" in updated_output:
            data = updated_output["data"]
            
            # If data is a list, simulate corrections to the first few items
            if isinstance(data, list) and data:
                # Simulate adding a missing field or correcting a value
                for i in range(min(3, len(data))):
                    if isinstance(data[i], dict):
                        # Add a "human_verified" flag
                        data[i]["human_verified"] = True
                        
                        # If it's customer feedback, maybe correct a rating
                        if "rating" in data[i] and data[i]["rating"] == 1:
                            # Simulate correcting a mistakenly low rating
                            data[i]["rating"] = 2
                            data[i]["feedback"] += " [Rating corrected by human]"
        
        # Add HITL metadata
        if "metadata" not in updated_output:
            updated_output["metadata"] = {}
        
        updated_output["metadata"]["hitl_applied"] = True
        updated_output["metadata"]["hitl_timestamp"] = self.history_manager.get_timestamp()
        updated_output["metadata"]["hitl_confidence_before"] = confidence_score
        
        return updated_output
    
    async def _handle_analysis_hitl(
        self, 
        task_name: str, 
        task_input: Dict[str, Any], 
        task_output: Dict[str, Any], 
        confidence_score: float
    ) -> Dict[str, Any]:
        """
        Handle HITL for statistical analysis tasks.
        
        Args:
            task_name: Name of the task that was executed
            task_input: Input data for the task
            task_output: Output data from the task
            confidence_score: Confidence score from the evaluator
            
        Returns:
            Updated task output after human intervention
        """
        logger.info("Handling statistical analysis HITL for task %s", task_name)
        
        # In a real implementation, this would:
        # 1. Present the analysis results to a human expert
        # 2. Allow them to correct or verify the analysis
        # 3. Return the corrected analysis
        
        # For demonstration, we'll simulate human corrections
        
        # Simulate human review time
        await asyncio.sleep(2.0)
        
        # Create a copy of the output to modify
        updated_output = task_output.copy()
        
        # Simulate human corrections to analysis results
        if "analysis_results" in updated_output:
            analysis_results = updated_output["analysis_results"]
            
            # Add human insights or corrections
            if "sentiment_distribution" in analysis_results:
                # Simulate a small correction to sentiment distribution
                # For example, reclassifying some neutral sentiments as positive or negative
                sentiment_dist = analysis_results["sentiment_distribution"]
                
                # Simulate a human expert slightly adjusting the sentiment distribution
                positive_adjustment = 0.05
                sentiment_dist["positive"] = min(1.0, sentiment_dist.get("positive", 0) + positive_adjustment)
                sentiment_dist["neutral"] = max(0.0, sentiment_dist.get("neutral", 0) - positive_adjustment)
                
                # Add a note about the adjustment
                analysis_results["human_notes"] = "Adjusted sentiment distribution based on contextual understanding of customer language."
            
            elif "sales_by_region" in analysis_results:
                # Simulate a human expert adding context to regional sales data
                analysis_results["human_notes"] = "Verified regional sales data. Note that the East region had a promotional event during this period."
                
                # Maybe add a new insight that the algorithm missed
                if "sales_insights" not in analysis_results:
                    analysis_results["sales_insights"] = []
                
                analysis_results["sales_insights"].append({
                    "type": "human_insight",
                    "description": "The sales spike in the East region correlates with the Q2 promotional campaign."
                })
        
        # Add HITL metadata
        if "metadata" not in updated_output:
            updated_output["metadata"] = {}
        
        updated_output["metadata"]["hitl_applied"] = True
        updated_output["metadata"]["hitl_timestamp"] = self.history_manager.get_timestamp()
        updated_output["metadata"]["hitl_confidence_before"] = confidence_score
        updated_output["metadata"]["hitl_notes"] = "Human expert reviewed and adjusted analysis."
        
        return updated_output
    
    async def _handle_visualization_hitl(
        self, 
        task_name: str, 
        task_input: Dict[str, Any], 
        task_output: Dict[str, Any], 
        confidence_score: float
    ) -> Dict[str, Any]:
        """
        Handle HITL for visualization tasks.
        
        Args:
            task_name: Name of the task that was executed
            task_input: Input data for the task
            task_output: Output data from the task
            confidence_score: Confidence score from the evaluator
            
        Returns:
            Updated task output after human intervention
        """
        logger.info("Handling visualization HITL for task %s", task_name)
        
        # In a real implementation, this would:
        # 1. Present the visualizations to a human
        # 2. Allow them to adjust visualization parameters or add annotations
        # 3. Return the improved visualizations
        
        # For demonstration, we'll simulate human improvements
        
        # Simulate human review time
        await asyncio.sleep(1.8)
        
        # Create a copy of the output to modify
        updated_output = task_output.copy()
        
        # Simulate human improvements to visualizations
        if "visualizations" in updated_output:
            visualizations = updated_output["visualizations"]
            
            # Iterate through visualizations and make improvements
            for viz in visualizations:
                # Improve the title to be more descriptive
                if "title" in viz:
                    viz["title"] = f"{viz['title']} - Human Enhanced"
                
                # Add annotations or insights
                if "annotations" not in viz:
                    viz["annotations"] = []
                
                viz["annotations"].append({
                    "type": "human_annotation",
                    "text": "Key insight highlighted by human reviewer",
                    "position": {"x": 0.5, "y": 0.5}  # In a real system, this would be more specific
                })
                
                # Improve the description
                if "description" in viz:
                    viz["description"] += " This visualization has been reviewed and enhanced by a human expert."
        
        # Add HITL metadata
        if "metadata" not in updated_output:
            updated_output["metadata"] = {}
        
        updated_output["metadata"]["hitl_applied"] = True
        updated_output["metadata"]["hitl_timestamp"] = self.history_manager.get_timestamp()
        updated_output["metadata"]["hitl_confidence_before"] = confidence_score
        updated_output["metadata"]["hitl_improvements"] = [
            "Enhanced visualization titles",
            "Added expert annotations",
            "Improved descriptions"
        ]
        
        return updated_output