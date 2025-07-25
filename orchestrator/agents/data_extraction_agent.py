"""
Data Extraction Agent for retrieving and preprocessing data.
"""

import logging
import asyncio
from typing import Dict, Any, List, Optional

from orchestrator.agents.base_agent import Agent

logger = logging.getLogger(__name__)

class DataExtractionAgent(Agent):
    """
    Agent specialized in retrieving and preprocessing data from various sources.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Data Extraction Agent.
        
        Args:
            config: Configuration dictionary for the agent
        """
        super().__init__("DataExtractionAgent", config)
    
    def _get_supported_tasks(self) -> List[str]:
        """
        Get the list of tasks supported by this agent.
        
        Returns:
            List of task names
        """
        return ["extract_data", "validate_data_source", "preprocess_data"]
    
    async def extract_data(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract data from the specified source.
        
        Args:
            request: Request containing data source information
            
        Returns:
            Extracted data
        """
        logger.info("Extracting data from source: %s", request.get("data_source", "unknown"))
        
        # Simulate data extraction
        await asyncio.sleep(1)  # Simulate processing time
        
        # In a real implementation, this would connect to databases, APIs, etc.
        data_source = request.get("data_source", "sample_data")
        
        # Generate sample data based on the request
        if "customer feedback" in data_source.lower():
            data = self._generate_sample_feedback_data()
        elif "sales" in data_source.lower():
            data = self._generate_sample_sales_data()
        else:
            data = self._generate_generic_sample_data()
        
        return {
            "data": data,
            "metadata": {
                "source": data_source,
                "record_count": len(data),
                "extraction_timestamp": self._get_timestamp()
            }
        }
    
    async def validate_data_source(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that the data source exists and is accessible.
        
        Args:
            request: Request containing data source information
            
        Returns:
            Validation result
        """
        data_source = request.get("data_source", "")
        logger.info("Validating data source: %s", data_source)
        
        # Simulate validation
        await asyncio.sleep(0.5)
        
        # In a real implementation, this would check if the data source is accessible
        is_valid = len(data_source) > 0
        
        return {
            "is_valid": is_valid,
            "message": "Data source is valid and accessible" if is_valid else "Invalid data source"
        }
    
    async def preprocess_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Preprocess the extracted data.
        
        Args:
            data: Extracted data to preprocess
            
        Returns:
            Preprocessed data
        """
        logger.info("Preprocessing data with %d records", len(data.get("data", [])))
        
        # Simulate preprocessing
        await asyncio.sleep(1.5)
        
        # In a real implementation, this would clean, normalize, and transform the data
        processed_data = data.get("data", [])
        
        return {
            "data": processed_data,
            "metadata": {
                **data.get("metadata", {}),
                "preprocessing_applied": ["cleaning", "normalization", "transformation"],
                "preprocessing_timestamp": self._get_timestamp()
            }
        }
    
    def _generate_sample_feedback_data(self) -> List[Dict[str, Any]]:
        """
        Generate sample customer feedback data.
        
        Returns:
            List of sample feedback records
        """
        return [
            {"id": 1, "customer_id": 101, "rating": 4, "feedback": "Great product, very satisfied!", "date": "2023-01-15"},
            {"id": 2, "customer_id": 102, "rating": 2, "feedback": "Product quality could be better", "date": "2023-01-18"},
            {"id": 3, "customer_id": 103, "rating": 5, "feedback": "Excellent service and product", "date": "2023-01-20"},
            {"id": 4, "customer_id": 104, "rating": 3, "feedback": "Average product, nothing special", "date": "2023-01-25"},
            {"id": 5, "customer_id": 105, "rating": 1, "feedback": "Very disappointed with quality", "date": "2023-02-02"},
            {"id": 6, "customer_id": 106, "rating": 4, "feedback": "Good product but expensive", "date": "2023-02-05"},
            {"id": 7, "customer_id": 107, "rating": 5, "feedback": "Best purchase I've made this year!", "date": "2023-02-10"},
            {"id": 8, "customer_id": 108, "rating": 2, "feedback": "Delivery was late and product damaged", "date": "2023-02-15"},
            {"id": 9, "customer_id": 109, "rating": 4, "feedback": "Very good customer service", "date": "2023-02-20"},
            {"id": 10, "customer_id": 110, "rating": 3, "feedback": "Product is okay but website is hard to navigate", "date": "2023-02-25"}
        ]
    
    def _generate_sample_sales_data(self) -> List[Dict[str, Any]]:
        """
        Generate sample sales data.
        
        Returns:
            List of sample sales records
        """
        return [
            {"id": 1, "product_id": "P001", "quantity": 5, "price": 29.99, "date": "2023-01-05", "region": "North"},
            {"id": 2, "product_id": "P002", "quantity": 2, "price": 49.99, "date": "2023-01-10", "region": "South"},
            {"id": 3, "product_id": "P001", "quantity": 3, "price": 29.99, "date": "2023-01-15", "region": "East"},
            {"id": 4, "product_id": "P003", "quantity": 1, "price": 99.99, "date": "2023-01-20", "region": "West"},
            {"id": 5, "product_id": "P002", "quantity": 4, "price": 49.99, "date": "2023-01-25", "region": "North"},
            {"id": 6, "product_id": "P004", "quantity": 2, "price": 19.99, "date": "2023-02-01", "region": "South"},
            {"id": 7, "product_id": "P001", "quantity": 6, "price": 29.99, "date": "2023-02-05", "region": "East"},
            {"id": 8, "product_id": "P003", "quantity": 2, "price": 99.99, "date": "2023-02-10", "region": "West"},
            {"id": 9, "product_id": "P002", "quantity": 3, "price": 49.99, "date": "2023-02-15", "region": "North"},
            {"id": 10, "product_id": "P004", "quantity": 5, "price": 19.99, "date": "2023-02-20", "region": "South"}
        ]
    
    def _generate_generic_sample_data(self) -> List[Dict[str, Any]]:
        """
        Generate generic sample data.
        
        Returns:
            List of generic sample records
        """
        return [
            {"id": i, "value": i * 10, "category": ["A", "B", "C"][i % 3], "timestamp": f"2023-01-{i+1:02d}"}
            for i in range(10)
        ]
    
    def _get_timestamp(self) -> str:
        """
        Get the current timestamp as a string.
        
        Returns:
            Current timestamp string
        """
        from datetime import datetime
        return datetime.now().isoformat()