"""
Main Orchestrator module that coordinates the entire system.
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional, Union

from orchestrator.agents.base_agent import Agent
from orchestrator.agents.data_extraction_agent import DataExtractionAgent
from orchestrator.agents.statistical_analysis_agent import StatisticalAnalysisAgent
from orchestrator.agents.visualization_agent import VisualizationAgent
from orchestrator.validation.confidence_evaluator import ConfidenceEvaluator
from orchestrator.hitl.hitl_manager import HITLManager
from orchestrator.state.workflow_state_manager import WorkflowStateManager
from orchestrator.state.context_store import ContextStore
from orchestrator.state.history_manager import HistoryManager
from orchestrator.utils.logging_tool import setup_logging

# Set up logging
logger = logging.getLogger(__name__)
setup_logging()

class Orchestrator:
    """
    Master controller that coordinates the workflow and manages agent interactions.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Orchestrator with configuration settings.
        
        Args:
            config: Configuration dictionary for the orchestrator
        """
        self.config = config or {}
        
        # Initialize confidence threshold
        self.confidence_threshold = self.config.get("confidence_threshold", 85)
        
        # Initialize state management components
        self.context_store = ContextStore()
        self.history_manager = HistoryManager()
        self.workflow_state_manager = WorkflowStateManager(self.context_store)
        
        # Initialize validation components
        self.confidence_evaluator = ConfidenceEvaluator(self.confidence_threshold)
        
        # Initialize HITL components
        self.hitl_manager = HITLManager(self.context_store, self.history_manager)
        
        # Initialize agents
        self.agents = {
            "data_extraction": DataExtractionAgent(),
            "statistical_analysis": StatisticalAnalysisAgent(),
            "visualization": VisualizationAgent()
        }
        
        logger.info("Orchestrator initialized with %d agents", len(self.agents))
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a user request through the entire workflow.
        
        Args:
            request: The user request to process
            
        Returns:
            The processed result
        """
        logger.info("Processing request: %s", request.get("request_id", "unknown"))
        
        # Initialize workflow state
        workflow_id = self.workflow_state_manager.create_workflow(request)
        self.context_store.set(f"workflow:{workflow_id}:request", request)
        
        try:
            # Step 1: Extract data
            extraction_result = await self._execute_agent_task(
                "data_extraction", 
                "extract_data", 
                request
            )
            
            # Step 2: Analyze data
            analysis_result = await self._execute_agent_task(
                "statistical_analysis", 
                "analyze_data", 
                extraction_result
            )
            
            # Step 3: Generate visualizations
            visualization_result = await self._execute_agent_task(
                "visualization", 
                "create_visualizations", 
                analysis_result
            )
            
            # Combine results
            final_result = {
                "request_id": request.get("request_id"),
                "extraction_result": extraction_result,
                "analysis_result": analysis_result,
                "visualization_result": visualization_result,
                "workflow_id": workflow_id,
                "status": "completed"
            }
            
            # Update workflow state
            self.workflow_state_manager.complete_workflow(workflow_id, final_result)
            
            logger.info("Request %s processed successfully", request.get("request_id", "unknown"))
            return final_result
            
        except Exception as e:
            logger.error("Error processing request: %s", str(e), exc_info=True)
            self.workflow_state_manager.fail_workflow(workflow_id, str(e))
            raise
    
    async def _execute_agent_task(
        self, 
        agent_name: str, 
        task_name: str, 
        task_input: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a task on an agent with validation and potential HITL intervention.
        
        Args:
            agent_name: Name of the agent to execute the task
            task_name: Name of the task to execute
            task_input: Input data for the task
            
        Returns:
            The result of the task execution
        """
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent {agent_name} not found")
        
        logger.info("Executing task %s on agent %s", task_name, agent_name)
        
        # Execute the task
        result = await agent.execute_task(task_name, task_input)
        
        # Evaluate confidence
        confidence_score = await self.confidence_evaluator.evaluate(
            agent_name, task_name, task_input, result
        )
        
        logger.info(
            "Task %s on agent %s completed with confidence score: %f", 
            task_name, agent_name, confidence_score
        )
        
        # Check if HITL is needed
        if confidence_score < self.confidence_threshold:
            logger.info(
                "Confidence score %f below threshold %f, triggering HITL", 
                confidence_score, self.confidence_threshold
            )
            
            # Trigger HITL process
            result = await self.hitl_manager.process(
                agent_name, task_name, task_input, result, confidence_score
            )
            
            # Re-evaluate confidence after HITL
            confidence_score = await self.confidence_evaluator.evaluate(
                agent_name, task_name, task_input, result, is_hitl_result=True
            )
            
            logger.info(
                "After HITL, task %s on agent %s has confidence score: %f", 
                task_name, agent_name, confidence_score
            )
        
        # Add confidence score to result
        result["confidence_score"] = confidence_score
        
        # Record in history
        self.history_manager.add_entry({
            "agent": agent_name,
            "task": task_name,
            "confidence_score": confidence_score,
            "hitl_triggered": confidence_score < self.confidence_threshold,
            "timestamp": self.history_manager.get_timestamp()
        })
        
        return result