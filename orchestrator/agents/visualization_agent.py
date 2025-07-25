"""
Visualization Agent for creating visual representations of data and analysis.
"""

import logging
import asyncio
import base64
import io
from typing import Dict, Any, List, Optional

from orchestrator.agents.base_agent import Agent

logger = logging.getLogger(__name__)

class VisualizationAgent(Agent):
    """
    Agent specialized in creating visualizations from data and analysis results.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Visualization Agent.
        
        Args:
            config: Configuration dictionary for the agent
        """
        super().__init__("VisualizationAgent", config)
    
    def _get_supported_tasks(self) -> List[str]:
        """
        Get the list of tasks supported by this agent.
        
        Returns:
            List of task names
        """
        return ["create_visualizations", "generate_dashboard", "export_report"]
    
    async def create_visualizations(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create visualizations based on analysis results.
        
        Args:
            analysis_result: Results from the statistical analysis agent
            
        Returns:
            Generated visualizations
        """
        results = analysis_result.get("analysis_results", {})
        logger.info("Creating visualizations for analysis results")
        
        # Simulate visualization creation
        await asyncio.sleep(1.5)  # Simulate processing time
        
        # Determine the type of data and create appropriate visualizations
        if "sentiment_distribution" in results:
            visualizations = await self._create_feedback_visualizations(results)
        elif "sales_by_region" in results:
            visualizations = await self._create_sales_visualizations(results)
        else:
            visualizations = await self._create_generic_visualizations(results)
        
        return {
            "visualizations": visualizations,
            "metadata": {
                "source_metadata": analysis_result.get("metadata", {}),
                "visualization_timestamp": self._get_timestamp(),
                "visualization_types": [viz["type"] for viz in visualizations]
            }
        }
    
    async def generate_dashboard(self, visualization_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate an interactive dashboard from visualizations.
        
        Args:
            visualization_result: Results from the visualization creation
            
        Returns:
            Dashboard configuration
        """
        visualizations = visualization_result.get("visualizations", [])
        logger.info("Generating dashboard with %d visualizations", len(visualizations))
        
        # Simulate dashboard generation
        await asyncio.sleep(2)
        
        # In a real implementation, this would create an interactive dashboard layout
        dashboard_layout = {
            "title": "Data Analysis Dashboard",
            "layout": "grid",
            "panels": []
        }
        
        # Add panels for each visualization
        for i, viz in enumerate(visualizations):
            panel = {
                "id": f"panel-{i+1}",
                "title": viz.get("title", f"Visualization {i+1}"),
                "type": viz.get("type", "chart"),
                "visualization_id": viz.get("id"),
                "position": {
                    "x": (i % 2) * 6,  # 2 columns
                    "y": (i // 2) * 6,  # Row based on index
                    "w": 6,
                    "h": 6
                }
            }
            dashboard_layout["panels"].append(panel)
        
        return {
            "dashboard": dashboard_layout,
            "visualizations": visualizations,
            "metadata": {
                "source_metadata": visualization_result.get("metadata", {}),
                "dashboard_timestamp": self._get_timestamp(),
                "panel_count": len(dashboard_layout["panels"])
            }
        }
    
    async def export_report(self, dashboard_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Export a report from the dashboard and visualizations.
        
        Args:
            dashboard_result: Results from the dashboard generation
            
        Returns:
            Exported report
        """
        dashboard = dashboard_result.get("dashboard", {})
        visualizations = dashboard_result.get("visualizations", [])
        logger.info("Exporting report from dashboard")
        
        # Simulate report generation
        await asyncio.sleep(1.8)
        
        # In a real implementation, this would generate a PDF or other report format
        report = {
            "title": "Data Analysis Report",
            "sections": [
                {
                    "title": "Executive Summary",
                    "content": "This report presents the analysis of the provided data."
                }
            ]
        }
        
        # Add sections for each visualization
        for i, viz in enumerate(visualizations):
            section = {
                "title": viz.get("title", f"Visualization {i+1}"),
                "content": viz.get("description", ""),
                "visualization_id": viz.get("id")
            }
            report["sections"].append(section)
        
        return {
            "report": report,
            "format": "json",  # In a real system, this might be "pdf", "html", etc.
            "metadata": {
                "source_metadata": dashboard_result.get("metadata", {}),
                "export_timestamp": self._get_timestamp(),
                "section_count": len(report["sections"])
            }
        }
    
    async def _create_feedback_visualizations(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Create visualizations for feedback data.
        
        Args:
            results: Feedback analysis results
            
        Returns:
            List of visualization configurations
        """
        visualizations = []
        
        # Sentiment distribution pie chart
        if "sentiment_distribution" in results:
            sentiment_dist = results["sentiment_distribution"]
            visualizations.append({
                "id": "viz-sentiment-dist",
                "title": "Sentiment Distribution",
                "type": "pie_chart",
                "description": "Distribution of customer sentiment based on feedback ratings.",
                "data": {
                    "labels": ["Positive", "Neutral", "Negative"],
                    "values": [
                        sentiment_dist.get("positive", 0) * 100,
                        sentiment_dist.get("neutral", 0) * 100,
                        sentiment_dist.get("negative", 0) * 100
                    ],
                    "colors": ["#90EE90", "#FFCC00", "#FF6666"]
                }
            })
        
        # Rating trend line chart
        if "rating_trend" in results:
            trend_data = results["rating_trend"]
            dates = sorted(trend_data.keys())
            values = [trend_data[date] for date in dates]
            
            visualizations.append({
                "id": "viz-rating-trend",
                "title": "Rating Trend Over Time",
                "type": "line_chart",
                "description": "Trend of average customer ratings over time.",
                "data": {
                    "x": dates,
                    "y": values,
                    "x_label": "Date",
                    "y_label": "Average Rating"
                }
            })
        
        return visualizations
    
    async def _create_sales_visualizations(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Create visualizations for sales data.
        
        Args:
            results: Sales analysis results
            
        Returns:
            List of visualization configurations
        """
        visualizations = []
        
        # Sales by product bar chart
        if "sales_by_product" in results:
            sales_by_product = results["sales_by_product"]
            products = list(sales_by_product.keys())
            values = [sales_by_product[product] for product in products]
            
            visualizations.append({
                "id": "viz-sales-by-product",
                "title": "Sales by Product",
                "type": "bar_chart",
                "description": "Comparison of sales performance across different products.",
                "data": {
                    "x": products,
                    "y": values,
                    "x_label": "Product",
                    "y_label": "Sales ($)"
                }
            })
        
        # Sales by region map
        if "sales_by_region" in results:
            sales_by_region = results["sales_by_region"]
            
            visualizations.append({
                "id": "viz-sales-by-region",
                "title": "Sales by Region",
                "type": "map",
                "description": "Geographical distribution of sales across regions.",
                "data": {
                    "regions": list(sales_by_region.keys()),
                    "values": list(sales_by_region.values()),
                    "color_scale": "Blues"
                }
            })
        
        # Sales trend line chart
        if "sales_trend" in results:
            trend_data = results["sales_trend"]
            dates = sorted(trend_data.keys())
            values = [trend_data[date] for date in dates]
            
            visualizations.append({
                "id": "viz-sales-trend",
                "title": "Sales Trend Over Time",
                "type": "line_chart",
                "description": "Trend of sales performance over time.",
                "data": {
                    "x": dates,
                    "y": values,
                    "x_label": "Date",
                    "y_label": "Sales ($)"
                }
            })
        
        return visualizations
    
    async def _create_generic_visualizations(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Create visualizations for generic data.
        
        Args:
            results: Generic analysis results
            
        Returns:
            List of visualization configurations
        """
        visualizations = []
        
        # Basic statistics bar chart
        visualizations.append({
            "id": "viz-basic-stats",
            "title": "Basic Statistics",
            "type": "bar_chart",
            "description": "Overview of basic statistical measures.",
            "data": {
                "x": ["Average", "Minimum", "Maximum", "Range"],
                "y": [
                    results.get("average_value", 0),
                    results.get("min_value", 0),
                    results.get("max_value", 0),
                    results.get("value_range", 0)
                ],
                "x_label": "Measure",
                "y_label": "Value"
            }
        })
        
        # Category comparison if available
        category_stats = results.get("category_statistics", {})
        if category_stats:
            categories = list(category_stats.keys())
            avg_values = [stats.get("avg_value", 0) for stats in category_stats.values()]
            
            visualizations.append({
                "id": "viz-category-comparison",
                "title": "Category Comparison",
                "type": "bar_chart",
                "description": "Comparison of average values across different categories.",
                "data": {
                    "x": categories,
                    "y": avg_values,
                    "x_label": "Category",
                    "y_label": "Average Value"
                }
            })
        
        return visualizations
    
    def _get_timestamp(self) -> str:
        """
        Get the current timestamp as a string.
        
        Returns:
            Current timestamp string
        """
        from datetime import datetime
        return datetime.now().isoformat()