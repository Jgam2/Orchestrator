"""
Statistical Analysis Agent for analyzing data and generating insights.
"""

import logging
import asyncio
import random
from typing import Dict, Any, List, Optional
from collections import defaultdict

from orchestrator.agents.base_agent import Agent

logger = logging.getLogger(__name__)

class StatisticalAnalysisAgent(Agent):
    """
    Agent specialized in performing statistical analysis on data.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Statistical Analysis Agent.
        
        Args:
            config: Configuration dictionary for the agent
        """
        super().__init__("StatisticalAnalysisAgent", config)
    
    def _get_supported_tasks(self) -> List[str]:
        """
        Get the list of tasks supported by this agent.
        
        Returns:
            List of task names
        """
        return ["analyze_data", "detect_anomalies", "generate_insights", "cluster_topics"]
    
    async def analyze_data(self, extraction_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the extracted data to generate statistical insights.
        
        Args:
            extraction_result: Result from the data extraction agent
            
        Returns:
            Analysis results
        """
        data = extraction_result.get("data", [])
        logger.info("Analyzing data with %d records", len(data))
        
        # Simulate analysis
        await asyncio.sleep(2)  # Simulate processing time
        
        # Determine the type of data and perform appropriate analysis
        if any("feedback" in item for item in data if isinstance(item, dict)):
            analysis_results = await self._analyze_feedback_data(data)
        elif any("product_id" in item for item in data if isinstance(item, dict)):
            analysis_results = await self._analyze_sales_data(data)
        else:
            analysis_results = await self._analyze_generic_data(data)
        
        return {
            "analysis_results": analysis_results,
            "metadata": {
                "source_metadata": extraction_result.get("metadata", {}),
                "analysis_timestamp": self._get_timestamp(),
                "analysis_methods": ["descriptive_statistics", "trend_analysis", "pattern_recognition"]
            }
        }
    
    async def detect_anomalies(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect anomalies in the data.
        
        Args:
            data: Data to analyze for anomalies
            
        Returns:
            Detected anomalies
        """
        logger.info("Detecting anomalies in data")
        
        # Simulate anomaly detection
        await asyncio.sleep(1.5)
        
        # In a real implementation, this would use statistical methods to detect anomalies
        # For demonstration, we'll randomly flag some items as anomalies
        items = data.get("data", [])
        anomalies = []
        
        for item in items:
            if random.random() < 0.2:  # 20% chance of being flagged as anomaly
                anomalies.append({
                    "item": item,
                    "anomaly_score": random.uniform(0.7, 0.95),
                    "reason": random.choice([
                        "Outlier value detected",
                        "Unusual pattern",
                        "Statistical deviation",
                        "Inconsistent with historical data"
                    ])
                })
        
        return {
            "anomalies": anomalies,
            "anomaly_count": len(anomalies),
            "total_items": len(items),
            "anomaly_percentage": len(anomalies) / len(items) if items else 0
        }
    
    async def generate_insights(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate business insights from analysis results.
        
        Args:
            analysis_results: Results of data analysis
            
        Returns:
            Generated insights
        """
        logger.info("Generating insights from analysis results")
        
        # Simulate insight generation
        await asyncio.sleep(1.8)
        
        # In a real implementation, this would use ML models to generate insights
        results = analysis_results.get("analysis_results", {})
        
        # Generate insights based on the type of analysis
        if "sentiment_distribution" in results:
            insights = self._generate_feedback_insights(results)
        elif "sales_by_region" in results:
            insights = self._generate_sales_insights(results)
        else:
            insights = self._generate_generic_insights(results)
        
        return {
            "insights": insights,
            "confidence_scores": {
                insight["title"]: random.uniform(0.75, 0.98) for insight in insights
            },
            "generation_timestamp": self._get_timestamp()
        }
    
    async def cluster_topics(self, text_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cluster text data into topics.
        
        Args:
            text_data: Text data to cluster
            
        Returns:
            Topic clusters
        """
        logger.info("Clustering text data into topics")
        
        # Simulate topic clustering
        await asyncio.sleep(2.2)
        
        # In a real implementation, this would use NLP techniques like LDA or BERTopic
        items = text_data.get("data", [])
        
        # Extract text fields
        texts = []
        for item in items:
            if isinstance(item, dict) and "feedback" in item:
                texts.append(item["feedback"])
        
        # Generate sample topics
        sample_topics = [
            {"name": "Product Quality", "keywords": ["quality", "product", "good", "great", "excellent", "poor"]},
            {"name": "Customer Service", "keywords": ["service", "customer", "support", "help", "responsive"]},
            {"name": "Pricing", "keywords": ["price", "expensive", "cheap", "cost", "worth"]},
            {"name": "Delivery", "keywords": ["delivery", "shipping", "late", "fast", "quick", "delay"]},
            {"name": "User Experience", "keywords": ["website", "app", "navigate", "easy", "difficult", "interface"]}
        ]
        
        # Assign documents to topics (in a real system, this would be done using NLP)
        topic_assignments = []
        for i, text in enumerate(texts):
            # Simple keyword matching for demonstration
            scores = []
            for topic in sample_topics:
                score = sum(1 for keyword in topic["keywords"] if keyword.lower() in text.lower())
                scores.append((topic["name"], score))
            
            # Assign to highest scoring topic
            assigned_topic = max(scores, key=lambda x: x[1])[0] if scores else "Uncategorized"
            
            topic_assignments.append({
                "document_id": i,
                "text": text,
                "assigned_topic": assigned_topic,
                "confidence": random.uniform(0.7, 0.95)
            })
        
        return {
            "topics": sample_topics,
            "assignments": topic_assignments,
            "topic_distribution": {
                topic["name"]: sum(1 for a in topic_assignments if a["assigned_topic"] == topic["name"])
                for topic in sample_topics
            }
        }
    
    async def _analyze_feedback_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze customer feedback data.
        
        Args:
            data: Customer feedback data
            
        Returns:
            Analysis results
        """
        # Calculate sentiment distribution
        ratings = [item.get("rating", 0) for item in data]
        sentiment_distribution = {
            "positive": sum(1 for r in ratings if r >= 4) / len(ratings) if ratings else 0,
            "neutral": sum(1 for r in ratings if r == 3) / len(ratings) if ratings else 0,
            "negative": sum(1 for r in ratings if r <= 2) / len(ratings) if ratings else 0
        }
        
        # Calculate average rating
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        
        # Group by date
        from collections import defaultdict
        date_groups = defaultdict(list)
        for item in data:
            date = item.get("date", "unknown")
            date_groups[date].append(item)
        
        # Calculate trend over time
        trend_data = {
            date: sum(item.get("rating", 0) for item in items) / len(items) if items else 0
            for date, items in date_groups.items()
        }
        
        return {
            "sentiment_distribution": sentiment_distribution,
            "average_rating": avg_rating,
            "rating_trend": trend_data,
            "sample_size": len(data)
        }
    
    async def _analyze_sales_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze sales data.
        
        Args:
            data: Sales data
            
        Returns:
            Analysis results
        """
        # Calculate total sales
        total_sales = sum(item.get("quantity", 0) * item.get("price", 0) for item in data)
        
        # Group by product
        from collections import defaultdict
        product_groups = defaultdict(list)
        for item in data:
            product_id = item.get("product_id", "unknown")
            product_groups[product_id].append(item)
        
        # Calculate sales by product
        sales_by_product = {
            product_id: sum(item.get("quantity", 0) * item.get("price", 0) for item in items)
            for product_id, items in product_groups.items()
        }
        
        # Group by region
        region_groups = defaultdict(list)
        for item in data:
            region = item.get("region", "unknown")
            region_groups[region].append(item)
        
        # Calculate sales by region
        sales_by_region = {
            region: sum(item.get("quantity", 0) * item.get("price", 0) for item in items)
            for region, items in region_groups.items()
        }
        
        # Group by date
        date_groups = defaultdict(list)
        for item in data:
            date = item.get("date", "unknown")
            date_groups[date].append(item)
        
        # Calculate trend over time
        trend_data = {
            date: sum(item.get("quantity", 0) * item.get("price", 0) for item in items)
            for date, items in date_groups.items()
        }
        
        return {
            "total_sales": total_sales,
            "sales_by_product": sales_by_product,
            "sales_by_region": sales_by_region,
            "sales_trend": trend_data,
            "sample_size": len(data)
        }
    
    async def _analyze_generic_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze generic data.
        
        Args:
            data: Generic data
            
        Returns:
            Analysis results
        """
        # Extract numeric values
        values = []
        for item in data:
            if isinstance(item, dict) and "value" in item:
                values.append(item["value"])
        
        # Calculate basic statistics
        avg_value = sum(values) / len(values) if values else 0
        min_value = min(values) if values else 0
        max_value = max(values) if values else 0
        
        # Group by category if available
        category_groups = defaultdict(list)
        for item in data:
            if isinstance(item, dict) and "category" in item:
                category = item["category"]
                category_groups[category].append(item)
        
        # Calculate statistics by category
        category_stats = {
            category: {
                "count": len(items),
                "avg_value": sum(item.get("value", 0) for item in items) / len(items) if items else 0,
                "min_value": min(item.get("value", 0) for item in items) if items else 0,
                "max_value": max(item.get("value", 0) for item in items) if items else 0
            }
            for category, items in category_groups.items()
        }
        
        return {
            "average_value": avg_value,
            "min_value": min_value,
            "max_value": max_value,
            "value_range": max_value - min_value if values else 0,
            "category_statistics": category_stats,
            "sample_size": len(data)
        }
    
    def _generate_feedback_insights(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate insights from feedback analysis.
        
        Args:
            results: Feedback analysis results
            
        Returns:
            List of insights
        """
        sentiment_dist = results.get("sentiment_distribution", {})
        avg_rating = results.get("average_rating", 0)
        
        insights = [
            {
                "title": "Overall Customer Satisfaction",
                "description": f"The overall customer satisfaction rating is {avg_rating:.2f}/5.0.",
                "importance": "high"
            }
        ]
        
        # Add insight about sentiment distribution
        positive = sentiment_dist.get("positive", 0) * 100
        negative = sentiment_dist.get("negative", 0) * 100
        
        if positive > 70:
            insights.append({
                "title": "Strong Positive Sentiment",
                "description": f"Customer feedback is predominantly positive ({positive:.1f}%), indicating strong product satisfaction.",
                "importance": "high"
            })
        elif negative > 30:
            insights.append({
                "title": "Concerning Negative Sentiment",
                "description": f"A significant portion of feedback ({negative:.1f}%) is negative, suggesting areas for improvement.",
                "importance": "high"
            })
        
        # Add trend insight if available
        trend_data = results.get("rating_trend", {})
        if trend_data:
            dates = sorted(trend_data.keys())
            if len(dates) >= 2:
                first_rating = trend_data[dates[0]]
                last_rating = trend_data[dates[-1]]
                change = last_rating - first_rating
                
                if abs(change) >= 0.5:
                    direction = "improved" if change > 0 else "declined"
                    insights.append({
                        "title": "Sentiment Trend",
                        "description": f"Customer satisfaction has {direction} by {abs(change):.2f} points over the analyzed period.",
                        "importance": "medium"
                    })
        
        return insights
    
    def _generate_sales_insights(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate insights from sales analysis.
        
        Args:
            results: Sales analysis results
            
        Returns:
            List of insights
        """
        total_sales = results.get("total_sales", 0)
        sales_by_product = results.get("sales_by_product", {})
        sales_by_region = results.get("sales_by_region", {})
        
        insights = [
            {
                "title": "Total Sales Performance",
                "description": f"Total sales for the period amount to ${total_sales:.2f}.",
                "importance": "high"
            }
        ]
        
        # Add insight about top product
        if sales_by_product:
            top_product = max(sales_by_product.items(), key=lambda x: x[1])
            product_contribution = (top_product[1] / total_sales) * 100 if total_sales else 0
            
            insights.append({
                "title": "Top Performing Product",
                "description": f"Product {top_product[0]} is the top performer, contributing ${top_product[1]:.2f} ({product_contribution:.1f}%) to total sales.",
                "importance": "high"
            })
        
        # Add insight about regional performance
        if sales_by_region:
            top_region = max(sales_by_region.items(), key=lambda x: x[1])
            bottom_region = min(sales_by_region.items(), key=lambda x: x[1])
            
            insights.append({
                "title": "Regional Performance Variance",
                "description": f"The {top_region[0]} region leads with ${top_region[1]:.2f} in sales, while the {bottom_region[0]} region has the lowest at ${bottom_region[1]:.2f}.",
                "importance": "medium"
            })
        
        # Add trend insight if available
        trend_data = results.get("sales_trend", {})
        if trend_data:
            dates = sorted(trend_data.keys())
            if len(dates) >= 2:
                first_sales = trend_data[dates[0]]
                last_sales = trend_data[dates[-1]]
                change_pct = ((last_sales - first_sales) / first_sales) * 100 if first_sales else 0
                
                if abs(change_pct) >= 5:
                    direction = "increased" if change_pct > 0 else "decreased"
                    insights.append({
                        "title": "Sales Trend",
                        "description": f"Sales have {direction} by {abs(change_pct):.1f}% from {dates[0]} to {dates[-1]}.",
                        "importance": "high"
                    })
        
        return insights
    
    def _generate_generic_insights(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate insights from generic data analysis.
        
        Args:
            results: Generic analysis results
            
        Returns:
            List of insights
        """
        avg_value = results.get("average_value", 0)
        value_range = results.get("value_range", 0)
        category_stats = results.get("category_statistics", {})
        
        insights = [
            {
                "title": "Data Overview",
                "description": f"The average value across all data points is {avg_value:.2f}, with a range of {value_range:.2f}.",
                "importance": "medium"
            }
        ]
        
        # Add insight about categories if available
        if category_stats:
            categories = list(category_stats.keys())
            if len(categories) >= 2:
                category_avgs = [(cat, stats["avg_value"]) for cat, stats in category_stats.items()]
                top_category = max(category_avgs, key=lambda x: x[1])
                bottom_category = min(category_avgs, key=lambda x: x[1])
                
                insights.append({
                    "title": "Category Comparison",
                    "description": f"Category {top_category[0]} has the highest average value at {top_category[1]:.2f}, while category {bottom_category[0]} has the lowest at {bottom_category[1]:.2f}.",
                    "importance": "medium"
                })
        
        return insights
    
    def _get_timestamp(self) -> str:
        """
        Get the current timestamp as a string.
        
        Returns:
            Current timestamp string
        """
        from datetime import datetime
        return datetime.now().isoformat()