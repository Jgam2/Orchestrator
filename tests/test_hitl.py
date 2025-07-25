"""
Tests for the HITL components.
"""

import unittest
import asyncio
from typing import Dict, Any

from orchestrator.hitl.hitl_manager import HITLManager
from orchestrator.hitl.user_interaction_tool import UserInteractionTool
from orchestrator.hitl.feedback_processor import FeedbackProcessor
from orchestrator.state.context_store import ContextStore
from orchestrator.state.history_manager import HistoryManager

class TestHITLManager(unittest.TestCase):
    """Test cases for the HITL Manager."""
    
    def setUp(self):
        """Set up test environment."""
        self.context_store = ContextStore()
        self.history_manager = HistoryManager()
        self.hitl_manager = HITLManager(self.context_store, self.history_manager)
    
    def test_initialization(self):
        """Test that the HITL manager initializes correctly."""
        self.assertIsNotNone(self.hitl_manager)
        self.assertEqual(self.hitl_manager.context_store, self.context_store)
        self.assertEqual(self.hitl_manager.history_manager, self.history_manager)
    
    def test_process(self):
        """Test processing a HITL request."""
        # Create test data
        agent_name = "TestAgent"
        task_name = "test_task"
        task_input = {"test": "input"}
        task_output = {"result": "output"}
        confidence_score = 70.0
        
        # Process HITL request
        updated_output = asyncio.run(self.hitl_manager.process(
            agent_name, task_name, task_input, task_output, confidence_score
        ))
        
        # Check the result
        self.assertIsNotNone(updated_output)
        self.assertIn("hitl_verified", updated_output)
        self.assertTrue(updated_output["hitl_verified"])

class TestUserInteractionTool(unittest.TestCase):
    """Test cases for the User Interaction Tool."""
    
    def setUp(self):
        """Set up test environment."""
        self.interaction_tool = UserInteractionTool()
    
    def test_initialization(self):
        """Test that the interaction tool initializes correctly."""
        self.assertIsNotNone(self.interaction_tool)


    def test_present_question(self):
        """Test presenting a question to the user."""
        # Create test data
        question = "Is this data correct?"
        options = ["Yes", "No", "Unsure"]
        
        # Present question
        response = asyncio.run(self.interaction_tool.present_question(
            question, options
        ))
        
        # Check the result
        self.assertIsNotNone(response)
        self.assertIn("type", response)
        self.assertIn("selected_option", response)
        self.assertIn(response["selected_option"], options)

class TestFeedbackProcessor(unittest.TestCase):
    """Test cases for the Feedback Processor."""
    
    def setUp(self):
        """Set up test environment."""
        self.feedback_processor = FeedbackProcessor()
    
    def test_initialization(self):
        """Test that the feedback processor initializes correctly."""
        self.assertIsNotNone(self.feedback_processor)
    
    def test_process_feedback(self):
        """Test processing feedback."""
        # Create test data
        feedback = {
            "type": "correction",
            "corrections": {"field1": "corrected_value"}
        }
        original_data = {
            "field1": "original_value",
            "field2": "unchanged_value"
        }
        
        # Process feedback
        updated_data = asyncio.run(self.feedback_processor.process_feedback(
            feedback, original_data
        ))
        
        # Check the result
        self.assertIsNotNone(updated_data)
        self.assertEqual(updated_data["field1"], "corrected_value")
        self.assertEqual(updated_data["field2"], "unchanged_value")
        self.assertIn("metadata", updated_data)
        self.assertTrue(updated_data["metadata"]["feedback_processed"])

if __name__ == "__main__":
    unittest.main()