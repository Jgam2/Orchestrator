"""
Tests for the Validation components.
"""

import unittest
import asyncio
from typing import Dict, Any

from orchestrator.validation.confidence_evaluator import ConfidenceEvaluator
from orchestrator.validation.rule_based_validator import RuleBasedValidator
from orchestrator.validation.embedding_validator import EmbeddingValidator
from orchestrator.validation.llm_validator import LLMValidator
from orchestrator.validation.validation_cache import ValidationCache

class TestConfidenceEvaluator(unittest.TestCase):
    """Test cases for the Confidence Evaluator."""
    
    def setUp(self):
        """Set up test environment."""
        self.evaluator = ConfidenceEvaluator(confidence_threshold=85.0)
    
    def test_initialization(self):
        """Test that the evaluator initializes correctly."""
        self.assertIsNotNone(self.evaluator)
        self.assertEqual(self.evaluator.confidence_threshold, 85.0)
    
    def test_evaluate(self):
        """Test evaluating confidence."""
        # Create test data
        agent_name = "TestAgent"
        task_name = "test_task"
        task_input = {"test": "input"}
        task_output = {"result": "output"}
        
        # Evaluate confidence
        confidence_score = asyncio.run(self.evaluator.evaluate(
            agent_name, task_name, task_input, task_output
        ))
        
        # Check the result
        self.assertIsNotNone(confidence_score)
        self.assertGreaterEqual(confidence_score, 0.0)
        self.assertLessEqual(confidence_score, 100.0)

class TestRuleBasedValidator(unittest.TestCase):
    """Test cases for the Rule-Based Validator."""
    
    def setUp(self):
        """Set up test environment."""
        self.validator = RuleBasedValidator()
    
    def test_initialization(self):
        """Test that the validator initializes correctly."""
        self.assertIsNotNone(self.validator)
        self.assertTrue(len(self.validator.rules) > 0)
    
    def test_validate(self):
        """Test validation."""
        # Create test data for data extraction
        agent_name = "DataExtractionAgent"
        task_name = "extract_data"
        task_input = {"data_source": "test"}
        task_output = {
            "data": [{"id": 1, "value": "test"}],
            "metadata": {"source": "test", "record_count": 1, "extraction_timestamp": "2023-01-01T00:00:00"}
        }
        
        # Validate
        result = asyncio.run(self.validator.validate(
            agent_name, task_name, task_input, task_output
        ))
        
        # Check the result
        self.assertIsNotNone(result)
        self.assertIn("is_valid", result)
        self.assertIn("confidence", result)
        self.assertIn("message", result)
        self.assertTrue(result["is_valid"])

class TestValidationCache(unittest.TestCase):
    """Test cases for the Validation Cache."""
    
    def setUp(self):
        """Set up test environment."""
        self.cache = ValidationCache()
    
    def test_initialization(self):
        """Test that the cache initializes correctly."""
        self.assertIsNotNone(self.cache)
        self.assertEqual(len(self.cache.cache), 0)
    
    def test_store_and_get(self):
        """Test storing and retrieving from cache."""
        # Create test data
        agent_name = "TestAgent"
        task_name = "test_task"
        task_input = {"test": "input"}
        task_output = {"result": "output"}
        validation_result = {"is_valid": True, "confidence": 95.0}
        
        # Store in cache
        self.cache.store(agent_name, task_name, task_input, task_output, validation_result)
        
        # Retrieve from cache
        cached_result = self.cache.get(agent_name, task_name, task_input, task_output)
        
        # Check the result
        self.assertIsNotNone(cached_result)
        self.assertEqual(cached_result, validation_result)

if __name__ == "__main__":
    unittest.main()