"""
Tests for the Orchestrator.
"""

import unittest
import asyncio
from typing import Dict, Any
import sys
import os
# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from orchestrator.main import Orchestrator

class TestOrchestrator(unittest.TestCase):
    """Test cases for the Orchestrator."""
    
    def setUp(self):
        """Set up test environment."""
        self.orchestrator = Orchestrator()
    
    def test_initialization(self):
        """Test that the orchestrator initializes correctly."""
        self.assertIsNotNone(self.orchestrator)
        self.assertIsNotNone(self.orchestrator.agents)
        self.assertIsNotNone(self.orchestrator.confidence_evaluator)
        self.assertIsNotNone(self.orchestrator.hitl_manager)
    
    def test_process_request(self):
        """Test processing a request."""
        # Create a test request
        request = {
            "request_id": "test-123",
            "data_source": "test_data",
            "analysis_type": "sentiment"
        }
        
        # Process the request
        result = asyncio.run(self.orchestrator.process_request(request))
        
        # Check the result
        self.assertIsNotNone(result)
        self.assertEqual(result["request_id"], "test-123")
        self.assertIn("extraction_result", result)
        self.assertIn("analysis_result", result)
        self.assertIn("visualization_result", result)
        self.assertEqual(result["status"], "completed")

if __name__ == "__main__":
    unittest.main()