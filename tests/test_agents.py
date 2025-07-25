"""
Tests for the Agent components.
"""
import sys
import os
# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import asyncio
from typing import Dict, Any

from orchestrator.agents.base_agent import Agent
from orchestrator.agents.data_extraction_agent import DataExtractionAgent
from orchestrator.agents.statistical_analysis_agent import StatisticalAnalysisAgent
from orchestrator.agents.visualization_agent import VisualizationAgent

class TestDataExtractionAgent(unittest.TestCase):
    """Test cases for the Data Extraction Agent."""
    
    def setUp(self):
        """Set up test environment."""
        self.agent = DataExtractionAgent()
    
    def test_initialization(self):
        """Test that the agent initializes correctly."""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.name, "DataExtractionAgent")
        self.assertIn("extract_data", self.agent.supported_tasks)
    
    def test_extract_data(self):
        """Test extracting data."""
        # Create a test request
        request = {
            "data_source": "customer_feedback"
        }
        
        # Extract data
        result = asyncio.run(self.agent.extract_data(request))
        
        # Check the result
        self.assertIsNotNone(result)
        self.assertIn("data", result)
        self.assertIn("metadata", result)
        self.assertTrue(len(result["data"]) > 0)
        self.assertEqual(result["metadata"]["source"], "customer_feedback")

class TestStatisticalAnalysisAgent(unittest.TestCase):
    """Test cases for the Statistical Analysis Agent."""
    
    def setUp(self):
        """Set up test environment."""
        self.agent = StatisticalAnalysisAgent()
    
    def test_initialization(self):
        """Test that the agent initializes correctly."""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.name, "StatisticalAnalysisAgent")
        self.assertIn("analyze_data", self.agent.supported_tasks)
    
    def test_analyze_data(self):
        """Test analyzing data."""
        # Create test extraction result
        extraction_result = {
            "data": [
                {"id": 1, "customer_id": 101, "rating": 4, "feedback": "Great product!", "date": "2023-01-15"},
                {"id": 2, "customer_id": 102, "rating": 2, "feedback": "Not satisfied", "date": "2023-01-18"}
            ],
            "metadata": {
                "source": "customer_feedback",
                "record_count": 2
            }
        }
        
        # Analyze data
        result = asyncio.run(self.agent.analyze_data(extraction_result))
        
        # Check the result
        self.assertIsNotNone(result)
        self.assertIn("analysis_results", result)
        self.assertIn("metadata", result)
        self.assertIn("sentiment_distribution", result["analysis_results"])

class TestVisualizationAgent(unittest.TestCase):
    """Test cases for the Visualization Agent."""
    
    def setUp(self):
        """Set up test environment."""
        self.agent = VisualizationAgent()
    
    def test_initialization(self):
        """Test that the agent initializes correctly."""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.name, "VisualizationAgent")
        self.assertIn("create_visualizations", self.agent.supported_tasks)
    
    def test_create_visualizations(self):
        """Test creating visualizations."""
        # Create test analysis result
        analysis_result = {
            "analysis_results": {
                "sentiment_distribution": {
                    "positive": 0.65,
                    "neutral": 0.20,
                    "negative": 0.15
                },
                "average_rating": 3.8
            },
            "metadata": {
                "source_metadata": {
                    "source": "customer_feedback"
                }
            }
        }
        
        # Create visualizations
        result = asyncio.run(self.agent.create_visualizations(analysis_result))
        
        # Check the result
        self.assertIsNotNone(result)
        self.assertIn("visualizations", result)
        self.assertIn("metadata", result)
        self.assertTrue(len(result["visualizations"]) > 0)

if __name__ == "__main__":
    unittest.main()