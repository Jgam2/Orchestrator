"""
User Interaction Tool for handling the interface between the system and human users.
"""

import logging
import asyncio
from typing import Dict, Any, Optional, Callable, List

logger = logging.getLogger(__name__)

class UserInteractionTool:
    """
    Handles user interface interactions for HITL processes.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the User Interaction Tool.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.interaction_callbacks = {}
        logger.info("UserInteractionTool initialized")
    
    def register_callback(self, interaction_type: str, callback: Callable):
        """
        Register a callback for a specific interaction type.
        
        Args:
            interaction_type: Type of interaction
            callback: Callback function to handle the interaction
        """
        self.interaction_callbacks[interaction_type] = callback
        logger.info("Registered callback for interaction type: %s", interaction_type)
    
    async def present_question(
        self, 
        question: str, 
        options: Optional[List[str]] = None, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Present a question to the user and get their response.
        
        Args:
            question: Question to present
            options: Optional list of response options
            context: Optional context information
            
        Returns:
            User response
        """
        logger.info("Presenting question to user: %s", question)
        
        # In a real implementation, this would:
        # 1. Display the question in a UI
        # 2. Wait for the user to respond
        # 3. Return the user's response
        
        # For demonstration, we'll simulate a user response
        
        # Simulate user thinking time
        await asyncio.sleep(2.0)
        
        # Generate a simulated response
        if options:
            # If options are provided, simulate selecting one
            import random
            selected_option = random.choice(options)
            response = {
                "type": "option_selection",
                "selected_option": selected_option,
                "confidence": "high"
            }
        else:
            # Simulate a free-text response
            response = {
                "type": "free_text",
                "text": f"Simulated response to: {question}",
                "confidence": "medium"
            }
        
        logger.info("Received user response: %s", response)
        return response
    
    async def present_verification(
        self, 
        statement: str, 
        data: Any, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Present a verification request to the user.
        
        Args:
            statement: Statement to verify
            data: Data to verify
            context: Optional context information
            
        Returns:
            Verification result
        """
        logger.info("Presenting verification request to user: %s", statement)
        
        # In a real implementation, this would:
        # 1. Display the statement and data in a UI
        # 2. Ask the user to verify it
        # 3. Return the verification result
        
        # For demonstration, we'll simulate a verification result
        
        # Simulate user verification time
        await asyncio.sleep(1.5)
        
        # Generate a simulated verification result
        import random
        is_verified = random.random() < 0.8  # 80% chance of verification
        
        response = {
            "is_verified": is_verified,
            "corrections": {} if is_verified else {"general": "Simulated correction"},
            "confidence": "high" if is_verified else "medium"
        }
        
        logger.info("Received verification result: %s", "verified" if is_verified else "not verified")
        return response
    
    async def present_data_for_review(
        self, 
        data: Any, 
        instructions: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Present data for human review and editing.
        
        Args:
            data: Data to review
            instructions: Instructions for the reviewer
            context: Optional context information
            
        Returns:
            Reviewed and potentially edited data
        """
        logger.info("Presenting data for review: %s", instructions)
        
        # In a real implementation, this would:
        # 1. Display the data in an editable UI
        # 2. Show the instructions
        # 3. Allow the user to make changes
        # 4. Return the edited data
        
        # For demonstration, we'll simulate a review result
        
        # Simulate user review time
        await asyncio.sleep(3.0)
        
        # Make a copy of the data to simulate edits
        import copy
        edited_data = copy.deepcopy(data)
        
        # Simulate some edits based on the data type
        if isinstance(edited_data, dict):
            # Add a review note
            edited_data["human_review_note"] = "Reviewed and approved with minor edits"
            
            # Simulate fixing a value if it exists
            if "status" in edited_data:
                edited_data["status"] = "verified"
        elif isinstance(edited_data, list) and edited_data:
            # Add a review note to the first item if it's a dict
            if isinstance(edited_data[0], dict):
                edited_data[0]["human_review_note"] = "Reviewed and approved"
        
        response = {
            "edited_data": edited_data,
            "changes_made": True,
            "review_notes": "Simulated review with minor edits"
        }
        
        logger.info("Received reviewed data with edits")
        return response
    
    async def notify_user(
        self, 
        message: str, 
        level: str = "info", 
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Send a notification to the user.
        
        Args:
            message: Notification message
            level: Notification level (info, warning, error)
            context: Optional context information
        """
        logger.info("Sending %s notification to user: %s", level, message)
        
        # In a real implementation, this would send a notification through the UI
        # For demonstration, we'll just log it
        
        # Simulate notification display time
        await asyncio.sleep(0.5)
        
        # Log based on level
        if level == "warning":
            logger.warning("User notification (warning): %s", message)
        elif level == "error":
            logger.error("User notification (error): %s", message)
        else:
            logger.info("User notification (info): %s", message)