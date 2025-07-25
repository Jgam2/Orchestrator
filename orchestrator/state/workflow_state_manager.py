"""
Workflow State Manager for managing workflow state and transitions.
"""

import logging
import uuid
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class WorkflowStateManager:
    """
    Manages workflow state and transitions.
    """
    
    def __init__(self, context_store, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Workflow State Manager.
        
        Args:
            context_store: Context store for maintaining workflow state
            config: Configuration dictionary
        """
        self.context_store = context_store
        self.config = config or {}
        self.workflows = {}
        logger.info("WorkflowStateManager initialized")
    
    def create_workflow(self, request: Dict[str, Any]) -> str:
        """
        Create a new workflow.
        
        Args:
            request: Initial request that triggered the workflow
            
        Returns:
            Workflow ID
        """
        # Generate a unique workflow ID
        workflow_id = str(uuid.uuid4())
        
        # Create workflow state
        workflow = {
            "id": workflow_id,
            "status": "created",
            "request": request,
            "steps": [],
            "created_at": self._get_timestamp(),
            "updated_at": self._get_timestamp()
        }
        
        # Store the workflow
        self.workflows[workflow_id] = workflow
        
        # Store in context
        self.context_store.set(f"workflow:{workflow_id}", workflow)
        
        logger.info("Created workflow %s", workflow_id)
        return workflow_id
    
    def update_workflow(self, workflow_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a workflow.
        
        Args:
            workflow_id: ID of the workflow to update
            updates: Updates to apply
            
        Returns:
            Updated workflow
        """
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        # Get the current workflow
        workflow = self.workflows[workflow_id]
        
        # Apply updates
        for key, value in updates.items():
            if key != "id":  # Don't allow changing the ID
                workflow[key] = value
        
        # Update timestamp
        workflow["updated_at"] = self._get_timestamp()
        
        # Store the updated workflow
        self.workflows[workflow_id] = workflow
        
        # Update in context
        self.context_store.set(f"workflow:{workflow_id}", workflow)
        
        logger.info("Updated workflow %s", workflow_id)
        return workflow
    
    def add_workflow_step(
        self, 
        workflow_id: str, 
        step_type: str, 
        step_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Add a step to a workflow.
        
        Args:
            workflow_id: ID of the workflow
            step_type: Type of step
            step_data: Step data
            
        Returns:
            Updated workflow
        """
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        # Get the current workflow
        workflow = self.workflows[workflow_id]
        
        # Create the step
        step = {
            "type": step_type,
            "data": step_data,
            "timestamp": self._get_timestamp()
        }
        
        # Add the step
        workflow["steps"].append(step)
        
        # Update timestamp
        workflow["updated_at"] = self._get_timestamp()
        
        # Store the updated workflow
        self.workflows[workflow_id] = workflow
        
        # Update in context
        self.context_store.set(f"workflow:{workflow_id}", workflow)
        
        logger.info("Added %s step to workflow %s", step_type, workflow_id)
        return workflow
    
    def complete_workflow(self, workflow_id: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mark a workflow as completed.
        
        Args:
            workflow_id: ID of the workflow
            result: Final result of the workflow
            
        Returns:
            Updated workflow
        """
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        # Get the current workflow
        workflow = self.workflows[workflow_id]
        
        # Update status and add result
        workflow["status"] = "completed"
        workflow["result"] = result
        workflow["completed_at"] = self._get_timestamp()
        workflow["updated_at"] = self._get_timestamp()
        
        # Store the updated workflow
        self.workflows[workflow_id] = workflow
        
        # Update in context
        self.context_store.set(f"workflow:{workflow_id}", workflow)
        
        logger.info("Completed workflow %s", workflow_id)
        return workflow
    
    def fail_workflow(self, workflow_id: str, error: str) -> Dict[str, Any]:
        """
        Mark a workflow as failed.
        
        Args:
            workflow_id: ID of the workflow
            error: Error message
            
        Returns:
            Updated workflow
        """
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        # Get the current workflow
        workflow = self.workflows[workflow_id]
        
        # Update status and add error
        workflow["status"] = "failed"
        workflow["error"] = error
        workflow["failed_at"] = self._get_timestamp()
        workflow["updated_at"] = self._get_timestamp()
        
        # Store the updated workflow
        self.workflows[workflow_id] = workflow
        
        # Update in context
        self.context_store.set(f"workflow:{workflow_id}", workflow)
        
        logger.info("Failed workflow %s: %s", workflow_id, error)
        return workflow
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a workflow by ID.
        
        Args:
            workflow_id: ID of the workflow
            
        Returns:
            Workflow or None if not found
        """
        return self.workflows.get(workflow_id)
    
    def list_workflows(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List workflows, optionally filtered by status.
        
        Args:
            status: Optional status filter
            
        Returns:
            List of workflows
        """
        if status:
            return [w for w in self.workflows.values() if w.get("status") == status]
        else:
            return list(self.workflows.values())
    
    def _get_timestamp(self) -> str:
        """
        Get the current timestamp as a string.
        
        Returns:
            Current timestamp string
        """
        from datetime import datetime
        return datetime.now().isoformat()