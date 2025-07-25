import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
import time
from PIL import Image
import io
import base64
import random

# Set page configuration
st.set_page_config(
    page_title="Human-in-the-Loop Intelligent Orchestration System",
    page_icon="🔄",
    layout="wide"
)

# Title and introduction
st.title("Human-in-the-Loop Intelligent Orchestration System")
st.markdown("""
This interactive demo showcases our consolidated Orchestrator approach for multi-agent systems with 
human-in-the-loop capabilities, validation, and confidence scoring.
""")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Architecture Overview",
    "Interactive Workflow",
    "Confidence Scoring Demo",
    "HITL Integration",
    "Agent Swarm Visualization",
    "Performance Metrics"
])

# Architecture Overview page
if page == "Architecture Overview":
    st.header("System Architecture")
    
    st.write("""
    This interactive demo showcases our consolidated Orchestrator approach for multi-agent systems with 
    human-in-the-loop capabilities, validation, and confidence scoring.
    """)
    
    # Create a more structured visualization with clear layers
    st.markdown("""
    <style>
    .layer-box {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 15px;
    }
    .layer-title {
        font-weight: bold;
        margin-bottom: 10px;
    }
    .agent-box {
        background-color: #dae8fc;
        border-radius: 5px;
        padding: 8px;
        margin: 5px;
        display: inline-block;
        text-align: center;
        width: 180px;
    }
    .tool-box {
        background-color: #d5e8d4;
        border-radius: 5px;
        padding: 8px;
        margin: 5px;
        display: inline-block;
        text-align: center;
        width: 180px;
    }
    .validation-box {
        background-color: #fff2cc;
        border-radius: 5px;
        padding: 8px;
        margin: 5px;
        display: inline-block;
        text-align: center;
        width: 180px;
    }
    .hitl-box {
        background-color: #f8cecc;
        border-radius: 5px;
        padding: 8px;
        margin: 5px;
        display: inline-block;
        text-align: center;
        width: 180px;
    }
    .user-box {
        background-color: #ffffff;
        border: 2px solid #f8cecc;
        border-radius: 5px;
        padding: 8px;
        margin: 5px;
        display: inline-block;
        text-align: center;
        width: 180px;
    }
    .arrow-down {
        text-align: center;
        font-size: 24px;
        margin: 5px 0;
    }
    </style>
    
    <!-- User Layer -->
    <div style="text-align: center; margin-bottom: 20px;">
        <div class="user-box">👩‍💼 User</div>
        <div class="arrow-down">↕️</div>
    </div>
    
    <!-- Orchestrator Layer -->
    <div class="layer-box">
        <div class="layer-title">Orchestration Layer</div>
        <div style="text-align: center;">
            <div class="agent-box">🧠 Orchestrator<br>(Master Controller)</div>
        </div>
        <div class="arrow-down">↓</div>
    </div>
    
    <!-- Agents Layer -->
    <div class="layer-box">
        <div class="layer-title">Agents Layer</div>
        <div style="text-align: center;">
            <div class="agent-box">📊 Data Extraction<br>Agent</div>
            <div class="agent-box">📈 Statistical Analysis<br>Agent</div>
            <div class="agent-box">📉 Visualization<br>Agent</div>
        </div>
        <div class="arrow-down">↓</div>
    </div>
    
    <!-- Validation Layer -->
    <div class="layer-box">
        <div class="layer-title">Validation & Confidence Layer</div>
        <div style="text-align: center;">
            <div class="validation-box">🔍 ConfidenceEvaluator</div>
            <div class="validation-box">📏 RuleBasedValidator</div>
            <div class="validation-box">🧩 EmbeddingValidator</div>
            <div class="validation-box">🤖 LLMValidator</div>
        </div>
        <div class="arrow-down">↓</div>
    </div>
    
    <!-- HITL Layer -->
    <div class="layer-box">
        <div class="layer-title">Human-in-the-Loop Layer</div>
        <div style="text-align: center;">
            <div class="hitl-box">👤 HITLManager</div>
            <div class="hitl-box">💬 UserInteractionTool</div>
            <div class="hitl-box">📝 FeedbackProcessor</div>
        </div>
        <div class="arrow-down">↕️</div>
    </div>
    
    <!-- State Management Layer -->
    <div class="layer-box">
        <div class="layer-title">State Management Layer</div>
        <div style="text-align: center;">
            <div class="tool-box">📋 WorkflowStateManager</div>
            <div class="tool-box">💾 ContextStore</div>
            <div class="tool-box">📜 HistoryManager</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add key components explanation
    st.subheader("Key Components")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Orchestrator**")
        st.markdown("- Central controller managing workflow and validation")
        
        st.markdown("**Domain Experts**")
        st.markdown("- Specialized agents for different knowledge domains")
        
        st.markdown("**Validation Tools**")
        st.markdown("- Confidence evaluation and validation components")
    
    with col2:
        st.markdown("**HITL Manager**")
        st.markdown("- Human interaction management")
        
        st.markdown("**Content Processor**")
        st.markdown("- Output formatting and enhancement")
        
        st.markdown("**State Management**")
        st.markdown("- Maintains workflow state and context")
    
    # Add color legend
    st.subheader("Color Legend")
    st.markdown("""
    - <span style='background-color: #dae8fc; padding: 3px;'>Blue: Orchestrator</span>
    - <span style='background-color: #d5e8d4; padding: 3px;'>Green: Domain Experts & Content</span>
    - <span style='background-color: #fff2cc; padding: 3px;'>Yellow: Validation Tools</span>
    - <span style='background-color: #f8cecc; padding: 3px;'>Red: HITL Components</span>
    """, unsafe_allow_html=True)

# Interactive Workflow page
elif page == "Interactive Workflow":
    st.header("Interactive Workflow Demonstration")
    
    # Create a workflow demonstration
    workflow_stage = st.selectbox("Select workflow stage to explore:", [
        "1. User submits request to Orchestrator",
        "2. Orchestrator analyzes request",
        "3. Requirements collection & validation",
        "4. Domain Expert processing",
        "5. Result validation",
        "6. Content enhancement",
        "7. Final delivery"
    ])
    
    # Display different content based on selected stage
    if "1. User" in workflow_stage:
        st.subheader("User Request Submission")
        st.write("The workflow begins with a user submitting a request to the system.")
        
        # Simple form to simulate request submission
        with st.form("request_form"):
            request_type = st.selectbox(
                "Request Type", 
                ["Data Analysis", "Document Processing", "Knowledge Synthesis", "System Integration"]
            )
            request_description = st.text_area(
                "Request Description", 
                "Analyze customer feedback data and identify key trends and sentiment patterns."
            )
            priority = st.slider("Priority", 1, 5, 3)
            submitted = st.form_submit_button("Submit Request")
            
            if submitted:
                st.success("Request submitted to Orchestrator!")
                st.json({
                    "request_id": "R-12345",
                    "type": request_type,
                    "description": request_description,
                    "priority": priority,
                    "timestamp": "2023-08-15T14:30:00Z",
                    "status": "received"
                })
    
    elif "2. Orchestrator analyzes" in workflow_stage:
        st.subheader("Request Analysis")
        st.write("The Orchestrator analyzes the incoming request to determine the appropriate workflow.")
        
        # Show a simulated analysis process
        st.code("""
# Pseudocode for Orchestrator request analysis
def analyze_request(request):
    # Extract key information
    request_type = request.get("type")
    description = request.get("description")
    
    # Determine required domain experts
    if "Data Analysis" in request_type:
        primary_agent = "Data Analysis Expert"
    elif "Document" in request_type:
        primary_agent = "Document Processing Expert"
    elif "Knowledge" in request_type:
        primary_agent = "Knowledge Synthesis Expert"
    else:
        primary_agent = "System Integration Expert"
    
    # Identify required information categories
    required_info = extract_required_information(description)
    
    # Plan workflow sequence
    workflow_plan = create_workflow_plan(primary_agent, required_info)
    
    return workflow_plan
        """, language="python")
        
        # Show the analysis results
        with st.expander("View Analysis Results"):
            st.json({
                "request_id": "R-12345",
                "primary_agent": "Data Analysis Expert",
                "required_information": [
                    "data_source",
                    "analysis_type",
                    "output_format",
                    "specific_metrics",
                    "time_period"
                ],
                "confidence_threshold": 90,
                "workflow_steps": [
                    "requirements_gathering",
                    "validation",
                    "data_analysis",
                    "content_enhancement",
                    "final_delivery"
                ]
            })
    
    elif "3. Requirements" in workflow_stage:
        st.subheader("Requirements Collection & Validation")
        st.write("The Orchestrator gathers and validates requirements before processing.")
        
        # Simulate the requirements gathering process
        requirements = [
            {"field": "data_source", "value": "Customer Feedback Database", "confidence": 98},
            {"field": "analysis_type", "value": "Sentiment Analysis & Topic Clustering", "confidence": 95},
            {"field": "output_format", "value": "Interactive Dashboard", "confidence": 87},
            {"field": "specific_metrics", "value": "Sentiment Score, Key Topics, Trend Over Time", "confidence": 92},
            {"field": "time_period", "value": None, "confidence": 0}
        ]
        
        # Display requirements table
        df = pd.DataFrame(requirements)
        st.dataframe(df)
        
        # Show validation process for a specific field
        st.subheader("Validation Process Example")
        field_to_validate = st.selectbox(
            "Select field to see validation process:", 
            ["output_format", "time_period"]
        )
        
        if field_to_validate == "output_format":
            st.write("Validating: 'Interactive Dashboard'")
            with st.expander("Validation Steps"):
                st.write("1. Check ValidationCache: No similar entry found")
                st.write("2. Apply RuleBasedValidator: Passed basic syntax check")
                st.write("3. Apply EmbeddingValidator: 87% similarity to known valid patterns")
                st.write("4. LLMValidator not needed (confidence above threshold)")
                st.write("5. Final confidence score: 87%")
            st.success("Validation passed! (87% > 85% threshold)")
        else:  # time_period
            st.write("Validating: None (Missing information)")
            with st.expander("Validation Steps"):
                st.write("1. Check ValidationCache: No similar entry found")
                st.write("2. Apply RuleBasedValidator: Failed (missing required field)")
                st.write("3. Final confidence score: 0%")
            st.error("Validation failed! (0% < 85% threshold)")
        
        # Show HITL process
        st.subheader("HITL Process Triggered")
        st.write("Human input required for missing information")
        with st.form("hitl_form"):
            time_period = st.text_input(
                "Please specify the time period for analysis:", 
                "Last 6 months (Jan-Jun 2023)"
            )
            submitted = st.form_submit_button("Submit")
            if submitted:
                st.success("Human input received and validated!")
                st.write("New confidence score: 95%")
    
    elif "4. Domain Expert" in workflow_stage:
        st.subheader("Domain Expert Processing")
        st.write("The appropriate Domain Expert agent processes the request based on its specialization.")
        
        # Show processing simulation
        st.info("Data Analysis Expert is processing the request...")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(101):
            # Update progress bar
            progress_bar.progress(i)
            
            # Update status text based on progress
            if i < 20:
                status_text.text("Loading data from Customer Feedback Database...")
            elif i < 40:
                status_text.text("Preprocessing text data...")
            elif i < 60:
                status_text.text("Performing sentiment analysis...")
            elif i < 80:
                status_text.text("Clustering topics...")
            else:
                status_text.text("Generating insights...")
            
            # Add a slight delay
            time.sleep(0.05)
        
        status_text.text("Processing complete!")
        
        # Show results
        st.subheader("Processing Results")
        
        # Create sample results
        results = {
            "sentiment_distribution": {
                "positive": 65,
                "neutral": 20,
                "negative": 15
            },
            "top_topics": [
                {"topic": "Product Quality", "count": 342, "avg_sentiment": 0.78},
                {"topic": "Customer Service", "count": 287, "avg_sentiment": 0.62},
                {"topic": "Pricing", "count": 201, "avg_sentiment": -0.12},
                {"topic": "Delivery Speed", "count": 185, "avg_sentiment": 0.45},
                {"topic": "User Interface", "count": 124, "avg_sentiment": 0.32}
            ],
            "sentiment_trend": {
                "Jan": 0.58,
                "Feb": 0.61,
                "Mar": 0.57,
                "Apr": 0.65,
                "May": 0.72,
                "Jun": 0.75
            },
            "processing_confidence": 92
        }
        
        # Display sentiment distribution
        st.write("**Sentiment Distribution:**")
        fig = go.Figure(data=[
            go.Pie(
                labels=list(results["sentiment_distribution"].keys()),
                values=list(results["sentiment_distribution"].values()),
                hole=.3,
                marker=dict(colors=['#90EE90', '#FFCC00', '#FF6666'])
            )
        ])
        st.plotly_chart(fig)
        
        # Display top topics
        st.write("**Top Topics:**")
        topics_df = pd.DataFrame(results["top_topics"])
        st.dataframe(topics_df)
        
        # Display sentiment trend
        st.write("**Sentiment Trend:**")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(results["sentiment_trend"].keys()),
            y=list(results["sentiment_trend"].values()),
            mode='lines+markers'
        ))
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Sentiment Score",
            yaxis=dict(range=[-1, 1])
        )
        st.plotly_chart(fig)
        
        # Display confidence score
        st.metric("Processing Confidence", f"{results['processing_confidence']}%")
    
    elif "5. Result validation" in workflow_stage:
        st.subheader("Result Validation")
        st.write("The system validates the results before presenting them to the user.")
        
        # Show validation process
        st.write("**Validation Process:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("**Validation Steps:**")
            st.write("1. ✅ Data completeness check")
            st.write("2. ✅ Statistical significance validation")
            st.write("3. ✅ Logical consistency check")
            st.write("4. ❌ Business context validation")
            st.write("5. ❌ Anomaly detection")
            
            st.error("**Validation Issue Detected:**")
            st.write("Unusual spike in negative sentiment for 'Pricing' topic in June requires human verification.")
            
        with col2:
            st.warning("**Human Verification Required**")
            st.write("Please verify the following anomaly:")
            st.write("Negative sentiment for 'Pricing' increased by 45% in June.")
            
            with st.form("validation_form"):
                verification = st.radio(
                    "Is this a valid insight or a data anomaly?",
                    ["Valid insight - Price increase was implemented in June", 
                     "Data anomaly - Needs further investigation",
                     "Valid insight but requires context in report"]
                )
                notes = st.text_area("Additional notes:", "")
                submitted = st.form_submit_button("Submit Verification")
                
                if submitted:
                    st.success("Verification received. Updating results...")
                    st.json({
                        "verification": verification,
                        "notes": notes,
                        "confidence_after_hitl": "98%"
                    })
    
    elif "6. Content enhancement" in workflow_stage:
        st.subheader("Content Enhancement")
        st.write("The system enhances the content for better presentation and understanding.")
        
        # Show enhancement process
        st.write("**Enhancement Process:**")
        
        enhancements = [
            {"type": "Visualization", "status": "Applied", "description": "Interactive charts for sentiment trends"},
            {"type": "Summarization", "status": "Applied", "description": "Executive summary of key findings"},
            {"type": "Recommendations", "status": "Pending", "description": "Business recommendations based on insights"},
            {"type": "Context", "status": "Applied", "description": "Industry benchmarks for comparison"}
        ]
        
        # Display enhancements
        enhancements_df = pd.DataFrame(enhancements)
        st.dataframe(enhancements_df)
        
        # Show recommendation generation
        st.subheader("Recommendation Generation")
        st.write("The system needs human input to generate business recommendations.")
        
        with st.form("recommendation_form"):
            st.write("Based on the analysis, please provide business recommendations:")
            
            pricing_rec = st.text_area(
                "Pricing strategy recommendation:", 
                "Consider a more transparent communication strategy for price changes to reduce negative sentiment."
            )
            
            service_rec = st.text_area(
                "Customer service recommendation:", 
                "Continue the current approach as sentiment is positive and improving."
            )
            
            product_rec = st.text_area(
                "Product quality recommendation:", 
                "Highlight product quality in marketing materials as it's our strongest positive sentiment driver."
            )
            
            submitted = st.form_submit_button("Submit Recommendations")
            
            if submitted:
                st.success("Recommendations received and incorporated into the final report.")
    
    else:  # "7. Final delivery"
        st.subheader("Final Delivery")
        st.write("The completed analysis is delivered to the user with all enhancements and validations.")
        
        # Show final report
        st.subheader("Customer Feedback Analysis Report")
        st.write("**Period:** January - June 2023")
        st.write("**Data Source:** Customer Feedback Database")
        st.write("**Confidence Score:** 98%")
        
        st.write("---")
        
        st.write("### Executive Summary")
        st.write("""
        Customer sentiment shows a positive trend over the analyzed period, with an overall 
        improvement from 0.58 in January to 0.75 in June (+29%). Product Quality remains the 
        most discussed topic with consistently high positive sentiment. Pricing shows increased 
        negative sentiment in June due to the recent price adjustments.
        """)
        
        st.write("### Key Findings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Sentiment Distribution:**")
            fig = go.Figure(data=[
                go.Pie(
                    labels=["Positive", "Neutral", "Negative"],
                    values=[65, 20, 15],
                    hole=.3,
                    marker=dict(colors=['#90EE90', '#FFCC00', '#FF6666'])
                )
            ])
            st.plotly_chart(fig)
        
        with col2:
            st.write("**Sentiment Trend:**")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                y=[0.58, 0.61, 0.57, 0.65, 0.72, 0.75],
                mode='lines+markers'
            ))
            fig.update_layout(
                xaxis_title="Month",
                yaxis_title="Sentiment Score",
                yaxis=dict(range=[0, 1])
            )
            st.plotly_chart(fig)
        
        st.write("### Topic Analysis")
        
        topics_data = {
            "Topic": ["Product Quality", "Customer Service", "Pricing", "Delivery Speed", "User Interface"],
            "Mentions": [342, 287, 201, 185, 124],
            "Sentiment": [0.78, 0.62, -0.12, 0.45, 0.32]
        }
        
        topics_df = pd.DataFrame(topics_data)
        
        # Create a horizontal bar chart
        fig = go.Figure()
        for i, topic in enumerate(topics_df["Topic"]):
            sentiment = topics_df["Sentiment"][i]
            color = '#90EE90' if sentiment > 0.3 else '#FFCC00' if sentiment > 0 else '#FF6666'
            fig.add_trace(go.Bar(
                y=[topic],
                x=[topics_df["Mentions"][i]],
                orientation='h',
                name=topic,
                marker=dict(color=color)
            ))
        
        fig.update_layout(
            title="Topic Mentions and Sentiment",
            xaxis_title="Number of Mentions",
            yaxis_title="Topic",
            height=400
        )
        
        st.plotly_chart(fig)
        
        st.write("### Recommendations")
        
        st.info("""
        **Pricing Strategy:**
        Consider a more transparent communication strategy for price changes to reduce negative sentiment.
        """)
        
        st.info("""
        **Customer Service:**
        Continue the current approach as sentiment is positive and improving.
        """)
        
        st.info("""
        **Product Quality:**
        Highlight product quality in marketing materials as it's our strongest positive sentiment driver.
        """)
        
        st.write("---")
        
        st.write("**Report generated by Human-in-the-Loop Intelligent Orchestration System**")
        st.write("**Human validation applied:** Yes (2 interactions)")
        st.write("**Report ID:** R12345-Final")
        st.write("**Generation Date:** 2023-08-15")

# Confidence Scoring Demo page
elif page == "Confidence Scoring Demo":
    st.header("Confidence Scoring System")
    st.write("""
    Our system uses a sophisticated multi-tiered approach to calculate confidence scores. This determines 
    when human intervention is needed and optimizes resource usage by only using expensive LLM calls when 
    simpler methods are insufficient.
    """)
    
    # Create tabs for different aspects of confidence scoring
    tab1, tab2, tab3 = st.tabs(["Confidence Calculation", "Validation Pipeline", "Interactive Demo"])
    
    with tab1:
        st.subheader("How Confidence Scores Are Calculated")
        st.markdown("""
        The confidence score is calculated through a weighted combination of different validation methods:
        
        1. **Rule-Based Validation (30% weight)**
           - Fast, deterministic checks based on predefined rules
           - Examples: Data type validation, range checks, pattern matching
        
        2. **Embedding-Based Validation (30% weight)**
           - Semantic similarity checks using vector embeddings
           - Compares input against known valid patterns
        
        3. **LLM-Based Validation (40% weight)**
           - Deep contextual understanding using language models
           - Only used when needed for complex validation
        
        The final confidence score is a weighted average of these components, ranging from 0-100%. 
        Human intervention is triggered when the score falls below a configurable threshold (typically 85%).
        """)
        
        # Create a sample visualization of confidence calculation
        st.subheader("Sample Confidence Calculation")
        
        # Sample data
        validation_types = ['Rule-Based', 'Embedding-Based', 'LLM-Based']
        scores = [92, 78, 65]
        weights = [0.3, 0.3, 0.4]
        
        # Calculate weighted score
        weighted_score = sum(s * w for s, w in zip(scores, weights))
        
        # Create a horizontal bar chart
        fig = go.Figure()
        for i, (v_type, score) in enumerate(zip(validation_types, scores)):
            fig.add_trace(go.Bar(
                y=[v_type],
                x=[score],
                orientation='h',
                name=f"{v_type} ({score}%)",
                marker=dict(
                    color=['#90EE90' if score >= 85 else '#FFCC00' if score >= 70 else '#FF6666'][0]
                ),
                text=[f"{score}%"],
                textposition='auto'
            ))
        
        fig.update_layout(
            title="Validation Scores by Method",
            xaxis_title="Confidence Score (%)",
            yaxis_title="Validation Method",
            xaxis=dict(range=[0, 100]),
            height=300,
            showlegend=False
        )
        
        st.plotly_chart(fig)
        
        # Show the final weighted score with a gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = weighted_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Final Confidence Score"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#1E90FF"},
                'steps': [
                    {'range': [0, 50], 'color': "#FF6666"},
                    {'range': [50, 85], 'color': "#FFCC00"},
                    {'range': [85, 100], 'color': "#90EE90"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 2},
                    'thickness': 0.75,
                    'value': 85
                }
            }
        ))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig)
        
        st.info(f"Final Weighted Score: {weighted_score:.1f}% (Below 85% threshold - HITL Required)")
    
    with tab2:
        st.subheader("Tiered Validation Pipeline")
        st.write("""
        Our system implements a tiered validation approach that progressively applies more sophisticated 
        (and computationally expensive) validation methods only when needed.
        """)
        
        # Create a flowchart-like visualization
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            st.markdown("""
            ```
            ┌─────────────────────┐
            │ Input Data          │
            └──────────┬──────────┘
                       ▼
            ┌─────────────────────┐
            │ ValidationCache     │◄───┐
            │ Check for cached    │    │
            │ validation results  │    │
            └──────────┬──────────┘    │
                       │               │
                Cache Miss            │
                       ▼               │
            ┌─────────────────────┐    │
            │ RuleBasedValidator  │    │
            │ Apply simple rules  │    │
            └──────────┬──────────┘    │
                       │               │
            If score < threshold      │
                       ▼               │
            ┌─────────────────────┐    │
            │ EmbeddingValidator  │    │
            │ Check semantic      │    │
            │ similarity          │    │
            └──────────┬──────────┘    │
                       │               │
            If score < threshold      │
                       ▼               │
            ┌─────────────────────┐    │
            │ LLMValidator        │    │
            │ Deep contextual     │    │
            │ validation          │    │
            └──────────┬──────────┘    │
                       │               │
                       │               │
                       ▼               │
            ┌─────────────────────┐    │
            │ ConfidenceEvaluator │    │
            │ Calculate final     │    │
            │ confidence score    │    │
            └──────────┬──────────┘    │
                       │               │
                Store result          │
                       └───────────────┘
            ```
            """)
        
        st.markdown("""
        **Benefits of Tiered Validation:**
        1. **Efficiency**: Most validations can be resolved with fast, inexpensive methods
        2. **Cost Optimization**: LLM calls are only made when necessary
        3. **Scalability**: Can handle high volumes of validation requests
        4. **Improved Latency**: Quick responses for common validation patterns
        5. **Continuous Learning**: Cache builds up over time, improving system performance
        """)
    
    with tab3:
        st.subheader("Confidence Score Simulator")
        st.write("Experiment with different validation scenarios to see how confidence scores are calculated.")

        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Input Parameters")
            validation_scenario = st.selectbox(
                "Select a validation scenario:",
                ["Data Validation", "Code Review", "Content Moderation", "Custom Scenario"]
            )
            
            if validation_scenario == "Custom Scenario":
                rule_score = st.slider("Rule-Based Score", 0, 100, 85)
                embedding_score = st.slider("Embedding-Based Score", 0, 100, 75)
                llm_score = st.slider("LLM-Based Score", 0, 100, 90)
                rule_weight = st.slider("Rule-Based Weight", 0.0, 1.0, 0.3, 0.1)
                embedding_weight = st.slider("Embedding-Based Weight", 0.0, 1.0, 0.3, 0.1)
                llm_weight = st.slider("LLM-Based Weight", 0.0, 1.0, 0.4, 0.1)
                threshold = st.slider("HITL Threshold", 50, 95, 85)
            else:
                # Preset scenarios
                if validation_scenario == "Data Validation":
                    rule_score = 92
                    embedding_score = 78
                    llm_score = 65
                    rule_weight = 0.4
                    embedding_weight = 0.3
                    llm_weight = 0.3
                    threshold = 85
                elif validation_scenario == "Code Review":
                    rule_score = 75
                    embedding_score = 82
                    llm_score = 90
                    rule_weight = 0.2
                    embedding_weight = 0.3
                    llm_weight = 0.5
                    threshold = 80
                elif validation_scenario == "Content Moderation":
                    rule_score = 60
                    embedding_score = 75
                    llm_score = 95
                    rule_weight = 0.2
                    embedding_weight = 0.2
                    llm_weight = 0.6
                    threshold = 90
            
            calculate_button = st.button("Calculate Confidence Score")
        
        with col2:
            st.subheader("Confidence Score Results")
            
            if calculate_button or 'last_calculation' in st.session_state:
                if calculate_button:
                    # Store the calculation in session state
                    st.session_state.last_calculation = {
                        'rule_score': rule_score,
                        'embedding_score': embedding_score,
                        'llm_score': llm_score,
                        'rule_weight': rule_weight,
                        'embedding_weight': embedding_weight,
                        'llm_weight': llm_weight,
                        'threshold': threshold
                    }
                else:
                    # Use the stored calculation
                    rule_score = st.session_state.last_calculation['rule_score']
                    embedding_score = st.session_state.last_calculation['embedding_score']
                    llm_score = st.session_state.last_calculation['llm_score']
                    rule_weight = st.session_state.last_calculation['rule_weight']
                    embedding_weight = st.session_state.last_calculation['embedding_weight']
                    llm_weight = st.session_state.last_calculation['llm_weight']
                    threshold = st.session_state.last_calculation['threshold']
                
                # Calculate weighted score
                weighted_score = (rule_score * rule_weight + 
                                 embedding_score * embedding_weight + 
                                 llm_score * llm_weight)
                
                # Create a horizontal bar chart for individual scores
                fig = go.Figure()
                validation_types = ['Rule-Based', 'Embedding-Based', 'LLM-Based']
                scores = [rule_score, embedding_score, llm_score]
                weights = [rule_weight, embedding_weight, llm_weight]
                
                for i, (v_type, score, weight) in enumerate(zip(validation_types, scores, weights)):
                    fig.add_trace(go.Bar(
                        y=[v_type],
                        x=[score],
                        orientation='h',
                        name=f"{v_type} ({score}%)",
                        marker=dict(
                            color=['#90EE90' if score >= threshold else '#FFCC00' if score >= threshold*0.8 else '#FF6666'][0]
                        ),
                        text=[f"{score}% (weight: {weight:.1f})"],
                        textposition='auto'
                    ))
                
                fig.update_layout(
                    xaxis_title="Score (%)",
                    yaxis_title="Validation Method",
                    xaxis=dict(range=[0, 100]),
                    height=200,
                    margin=dict(l=20, r=20, t=30, b=20),
                    showlegend=False
                )
                
                st.plotly_chart(fig)
                
                # Show the final weighted score with a gauge
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = weighted_score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Final Confidence Score"},
                    gauge = {
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "#1E90FF"},
                        'steps': [
                            {'range': [0, threshold*0.6], 'color': "#FF6666"},
                            {'range': [threshold*0.6, threshold], 'color': "#FFCC00"},
                            {'range': [threshold, 100], 'color': "#90EE90"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 2},
                            'thickness': 0.75,
                            'value': threshold
                        }
                    }
                ))
                
                fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
                st.plotly_chart(fig)
                
                # Show the result
                if weighted_score >= threshold:
                    st.success(f"Final Confidence Score: {weighted_score:.1f}% (Above {threshold}% threshold - No HITL Required)")
                    st.write("The system can proceed automatically without human intervention.")
                else:
                    st.error(f"Final Confidence Score: {weighted_score:.1f}% (Below {threshold}% threshold - HITL Required)")
                    st.write("Human intervention is required for this validation.")
                
                # Show which validation methods failed
                st.subheader("Validation Analysis")
                for v_type, score in zip(validation_types, scores):
                    if score < threshold:
                        st.warning(f"⚠️ {v_type} validation score ({score}%) is below threshold")
                    else:
                        st.info(f"✅ {v_type} validation score ({score}%) meets threshold")

# HITL Integration page
elif page == "HITL Integration":
    st.header("Human-in-the-Loop Integration")
    st.write("""
    Our system intelligently determines when human expertise is needed and seamlessly integrates human input 
    into the workflow.
    """)
    
    # Create tabs for different HITL scenarios
    tab1, tab2, tab3 = st.tabs(["Missing Information", "Low Confidence", "Expert Review"])
    
    with tab1:
        st.subheader("Scenario: Missing Information")
        st.write("""
        When the system detects missing critical information, it automatically triggers a human interaction 
        to gather the required data.
        """)
        
        # Create a visualization of the HITL flow for missing information
        st.markdown("""
        <div style="text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px; margin-bottom: 20px;">
            <div style="font-weight: bold; font-size: 18px; margin-bottom: 15px;">Missing Information HITL Flow</div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="background-color: #dae8fc; padding: 10px; border-radius: 5px; width: 20%;">System</div>
                <div style="width: 50%; text-align: center;">→ Detects missing 'budget_constraint' field →</div>
                <div style="background-color: #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">HITLManager</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="background-color: #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">HITLManager</div>
                <div style="width: 50%; text-align: center;">→ Formats question for human →</div>
                <div style="background-color: #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">UserInteractionTool</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="background-color: #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">UserInteractionTool</div>
                <div style="width: 50%; text-align: center;">→ Presents question through interface →</div>
                <div style="background-color: #ffffff; border: 2px solid #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">Human</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="background-color: #ffffff; border: 2px solid #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">Human</div>
                <div style="width: 50%; text-align: center;">→ Provides missing information →</div>
                <div style="background-color: #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">FeedbackProcessor</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="background-color: #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">FeedbackProcessor</div>
                <div style="width: 50%; text-align: center;">→ Validates and incorporates input →</div>
                <div style="background-color: #d5e8d4; padding: 10px; border-radius: 5px; width: 20%;">ContextStore</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="background-color: #d5e8d4; padding: 10px; border-radius: 5px; width: 20%;">WorkflowStateManager</div>
                <div style="width: 50%; text-align: center;">→ Resumes workflow with new information →</div>
                <div style="background-color: #dae8fc; padding: 10px; border-radius: 5px; width: 20%;">System</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Interactive demo
        st.subheader("Interactive Demo")
        with st.form("missing_info_form"):
            st.write("System has detected missing information:")
            st.info("What is the budget constraint for this analysis project?")
            budget = st.text_input("Budget Constraint:", placeholder="e.g., $5,000 - $10,000")
            submitted = st.form_submit_button("Submit")
            
            if submitted and budget:
                st.success("Thank you! Information received and validated.")
                st.json({
                    "field": "budget_constraint",
                    "value": budget,
                    "confidence": 100,
                    "source": "human_input",
                    "timestamp": "2023-08-15T14:35:22Z"
                })
    
    with tab2:
        st.subheader("Scenario: Low Confidence")
        st.write("""
        When the system's confidence in its understanding or processing falls below the threshold, 
        it requests human verification or clarification.
        """)
        
        # Create a visualization of the HITL flow for low confidence
        st.markdown("""
        <div style="text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px; margin-bottom: 20px;">
            <div style="font-weight: bold; font-size: 18px; margin-bottom: 15px;">Low Confidence HITL Flow</div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="background-color: #fff2cc; padding: 10px; border-radius: 5px; width: 20%;">ConfidenceEvaluator</div>
                <div style="width: 50%; text-align: center;">→ Detects 72% confidence (below threshold) →</div>
                <div style="background-color: #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">HITLManager</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="background-color: #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">HITLManager</div>
                <div style="width: 50%; text-align: center;">→ Prepares verification request →</div>
                <div style="background-color: #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">UserInteractionTool</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="background-color: #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">UserInteractionTool</div>
                <div style="width: 50%; text-align: center;">→ Presents verification request →</div>
                <div style="background-color: #ffffff; border: 2px solid #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">Human</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="background-color: #ffffff; border: 2px solid #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">Human</div>
                <div style="width: 50%; text-align: center;">→ Reviews and corrects information →</div>
                <div style="background-color: #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">FeedbackProcessor</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="background-color: #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">FeedbackProcessor</div>
                <div style="width: 50%; text-align: center;">→ Recalculates confidence with human input →</div>
                <div style="background-color: #dae8fc; padding: 10px; border-radius: 5px; width: 20%;">System</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Interactive demo
        st.subheader("Interactive Demo")
        st.write("System has low confidence (72%) in its interpretation:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("System's interpretation:")
            st.write("Analysis should include **quarterly** breakdown of customer sentiment.")
        
        with col2:
            with st.form("low_confidence_form"):
                st.write("Is this interpretation correct?")
                is_correct = st.radio("", ["Yes", "No"], horizontal=True)
                correction = st.text_input(
                    "If no, please provide correction:", 
                    placeholder="e.g., Monthly breakdown, not quarterly"
                )
                submitted = st.form_submit_button("Submit")
                
                if submitted:
                    if is_correct == "Yes":
                        st.success("Interpretation confirmed! Confidence updated to 100%.")
                    else:
                        st.success("Thank you for the correction! Updated information recorded.")
    
    with tab3:
        st.subheader("Scenario: Expert Review")
        st.write("""
        For critical decisions or high-impact outputs, the system can request expert human review 
        before proceeding.
        """)
        
        # Create a visualization of the expert review process
        st.markdown("""
        <div style="text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px; margin-bottom: 20px;">
            <div style="font-weight: bold; font-size: 18px; margin-bottom: 15px;">Expert Review HITL Flow</div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="background-color: #dae8fc; padding: 10px; border-radius: 5px; width: 20%;">System</div>
                <div style="width: 50%; text-align: center;">→ Generates high-impact analysis →</div>
                <div style="background-color: #fff2cc; padding: 10px; border-radius: 5px; width: 20%;">ConfidenceEvaluator</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="background-color: #fff2cc; padding: 10px; border-radius: 5px; width: 20%;">ConfidenceEvaluator</div>
                <div style="width: 50%; text-align: center;">→ Flags for expert review (high impact) →</div>
                <div style="background-color: #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">HITLManager</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="background-color: #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">HITLManager</div>
                <div style="width: 50%; text-align: center;">→ Prepares expert review request →</div>
                <div style="background-color: #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">UserInteractionTool</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="background-color: #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">UserInteractionTool</div>
                <div style="width: 50%; text-align: center;">→ Presents analysis for review →</div>
                <div style="background-color: #ffffff; border: 2px solid #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">Expert</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="background-color: #ffffff; border: 2px solid #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">Expert</div>
                <div style="width: 50%; text-align: center;">→ Reviews and provides feedback →</div>
                <div style="background-color: #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">FeedbackProcessor</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="background-color: #f8cecc; padding: 10px; border-radius: 5px; width: 20%;">FeedbackProcessor</div>
                <div style="width: 50%; text-align: center;">→ Incorporates expert feedback →</div>
                <div style="background-color: #dae8fc; padding: 10px; border-radius: 5px; width: 20%;">System</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Interactive demo
        st.subheader("Interactive Demo")
        st.write("System has generated an analysis that requires expert review:")
        
        with st.expander("View Generated Analysis"):
            st.write("""
            ## Customer Sentiment Analysis: Q2 2023
            
            Overall sentiment shows a **positive trend** with a 15% increase in positive mentions compared to Q1.
            
            Key areas of improvement:
            1. Product reliability (27% more positive mentions)
            2. Customer service response time (18% improvement)
            3. Mobile app usability (12% improvement)
            
            Areas requiring attention:
            1. Pricing concerns (8% increase in negative mentions)
            2. Website navigation issues (consistent with Q1)
            
            Recommendation: Focus communication on reliability improvements while addressing pricing concerns 
            in upcoming marketing materials.
            """)
        
        with st.form("expert_review_form"):
            st.write("Please review the analysis and provide feedback:")
            accuracy = st.slider("Accuracy Rating", 1, 10, 8)
            completeness = st.slider("Completeness Rating", 1, 10, 7)
            feedback = st.text_area(
                "Additional Feedback or Corrections:", 
                placeholder="Enter any feedback or corrections here..."
            )
            approval = st.radio(
                "Approve for delivery?", 
                ["Approve", "Approve with changes", "Reject"], 
                horizontal=True
            )
            submitted = st.form_submit_button("Submit Review")
            
            if submitted:
                st.success(f"Review submitted! Status: {approval}")
                if approval == "Approve":
                    st.write("Analysis will be delivered as is.")
                elif approval == "Approve with changes":
                    st.write("Analysis will be updated with your feedback before delivery.")
                else:
                    st.write("Analysis will be reworked based on your feedback.")

# Agent Swarm Visualization page
elif page == "Agent Swarm Visualization":
    st.header("Multi-Agent System Architecture")
    st.write("""
    This visualization demonstrates how multiple specialized agents work together in a layered architecture, 
    coordinated by the Orchestrator. The human-in-the-loop functionality is triggered when confidence scores 
    fall below the threshold.
    """)

    # Create tabs for different visualizations
    tab1, tab2 = st.tabs(["System Architecture", "Agent Communication"])
    
    with tab1:
        st.subheader("Multi-Agent System Architecture with HITL")
        
        # Create a more structured visualization with clear layers
        st.markdown("""
        <style>
        .layer-box {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 15px;
        }
        .layer-title {
            font-weight: bold;
            margin-bottom: 10px;
        }
        .agent-box {
            background-color: #dae8fc;
            border-radius: 5px;
            padding: 8px;
            margin: 5px;
            display: inline-block;
            text-align: center;
            width: 180px;
        }
        .tool-box {
            background-color: #d5e8d4;
            border-radius: 5px;
            padding: 8px;
            margin: 5px;
            display: inline-block;
            text-align: center;
            width: 180px;
        }
        .validation-box {
            background-color: #fff2cc;
            border-radius: 5px;
            padding: 8px;
            margin: 5px;
            display: inline-block;
            text-align: center;
            width: 180px;
        }
        .hitl-box {
            background-color: #f8cecc;
            border-radius: 5px;
            padding: 8px;
            margin: 5px;
            display: inline-block;
            text-align: center;
            width: 180px;
        }
        .utility-box {
            background-color: #e1d5e7;
            border-radius: 5px;
            padding: 8px;
            margin: 5px;
            display: inline-block;
            text-align: center;
            width: 180px;
        }
        .user-box {
            background-color: #ffffff;
            border: 2px solid #f8cecc;
            border-radius: 5px;
            padding: 8px;
            margin: 5px;
            display: inline-block;
            text-align: center;
            width: 180px;
        }
        .arrow-down {
            text-align: center;
            font-size: 24px;
            margin: 5px 0;
        }
        .hitl-flow {
            border-left: 3px dashed #f8cecc;
            padding-left: 15px;
            margin-left: 20px;
        }
        </style>
        
        <!-- User Layer -->
        <div style="text-align: center; margin-bottom: 20px;">
            <div class="user-box">👩‍💼 User</div>
            <div class="arrow-down">↕️</div>
        </div>
        
        <!-- Orchestrator Layer -->
        <div class="layer-box">
            <div class="layer-title">Orchestration Layer</div>
            <div style="text-align: center;">
                <div class="agent-box">🧠 Orchestrator<br>(Master Controller)</div>
            </div>
            <div class="arrow-down">↓</div>
        </div>
        
        <!-- Agents Layer -->
        <div class="layer-box">
            <div class="layer-title">Agents Layer</div>
            <div style="text-align: center;">
                <div class="agent-box">📊 Data Extraction<br>Agent</div>
                <div class="agent-box">📈 Statistical Analysis<br>Agent</div>
                <div class="agent-box">📉 Visualization<br>Agent</div>
            </div>
            <div class="arrow-down">↓</div>
        </div>
        
        <!-- Validation Layer -->
        <div class="layer-box">
            <div class="layer-title">Validation & Confidence Layer</div>
            <div style="text-align: center;">
                <div class="validation-box">🔍 ConfidenceEvaluator</div>
                <div class="validation-box">📏 RuleBasedValidator</div>
                <div class="validation-box">🧩 EmbeddingValidator</div>
                <div class="validation-box">🤖 LLMValidator</div>
            </div>
            <div class="arrow-down">↓</div>
        </div>
        
        <!-- HITL Layer -->
        <div class="layer-box">
            <div class="layer-title">Human-in-the-Loop Layer</div>
            <div style="text-align: center;">
                <div class="hitl-box">👤 HITLManager</div>
                <div class="hitl-box">💬 UserInteractionTool</div>
                <div class="hitl-box">📝 FeedbackProcessor</div>
            </div>
            <div class="arrow-down">↕️</div>
        </div>
        
        <!-- State Management Layer -->
        <div class="layer-box">
            <div class="layer-title">State Management Layer</div>
            <div style="text-align: center;">
                <div class="tool-box">📋 WorkflowStateManager</div>
                <div class="tool-box">💾 ContextStore</div>
                <div class="tool-box">📜 HistoryManager</div>
            </div>
        </div>
        
        <!-- Utility Layer -->
        <div class="layer-box">
            <div class="layer-title">Utility Tools Layer</div>
            <div style="text-align: center;">
                <div class="utility-box">🗃️ ValidationCache</div>
                <div class="utility-box">🔧 ModelSelector</div>
                <div class="utility-box">📝 LoggingTool</div>
                <div class="utility-box">🔐 AuthManager</div>
            </div>
        </div>
        
        <!-- HITL Flow Visualization -->
        <div style="margin-top: 30px; padding: 15px; border: 2px dashed #f8cecc; border-radius: 5px;">
            <div class="layer-title">Human-in-the-Loop Flow</div>
            <ol>
                <li>Agent produces output with confidence score below threshold</li>
                <li>ConfidenceEvaluator detects low confidence and triggers HITL process</li>
                <li>HITLManager formulates appropriate question for human</li>
                <li>UserInteractionTool presents the question to the user</li>
                <li>User provides input/feedback</li>
                <li>FeedbackProcessor validates and incorporates human input</li>
                <li>WorkflowStateManager updates context and resumes workflow</li>
                <li>Agent continues processing with human-augmented information</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        # Add key components explanation
        st.subheader("Key Components")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Agents Layer**")
            st.markdown("- **Orchestrator**: Central controller managing workflow and agent interactions")
            st.markdown("- **Domain Expert Agents**: Specialized agents for different tasks")
            
            st.markdown("**Validation Layer**")
            st.markdown("- **ConfidenceEvaluator**: Calculates confidence scores for agent outputs")
            st.markdown("- **RuleBasedValidator**: Applies predefined rules for validation")
            st.markdown("- **EmbeddingValidator**: Uses vector embeddings for semantic validation")
            st.markdown("- **LLMValidator**: Uses LLM for complex validation cases")
        
        with col2:
            st.markdown("**HITL Layer**")
            st.markdown("- **HITLManager**: Manages human-in-the-loop interactions")
            st.markdown("- **UserInteractionTool**: Handles user interface interactions")
            st.markdown("- **FeedbackProcessor**: Processes human feedback")
            
            st.markdown("**State Management Layer**")
            st.markdown("- **WorkflowStateManager**: Manages workflow state and transitions")
            st.markdown("- **ContextStore**: Maintains conversation context")
            st.markdown("- **HistoryManager**: Tracks interaction history")
        
        # Add color legend
        st.subheader("Color Legend")
        st.markdown("""
        - <span style='background-color: #dae8fc; padding: 3px;'>Blue: Orchestrator & Agents</span>
        - <span style='background-color: #d5e8d4; padding: 3px;'>Green: State Management Tools</span>
        - <span style='background-color: #fff2cc; padding: 3px;'>Yellow: Validation Tools</span>
        - <span style='background-color: #f8cecc; padding: 3px;'>Red: HITL Components</span>
        - <span style='background-color: #e1d5e7; padding: 3px;'>Purple: Utility Tools</span>
        """, unsafe_allow_html=True)

    with tab2:
        st.subheader("Agent Communication Patterns")
        st.write("""
        This visualization shows the communication patterns between different agents in the system,
        highlighting how information flows and where human-in-the-loop interactions occur.
        """)
        
        # Create a sample dataset of agent communications
        communications = [
            {"from": "Orchestrator", "to": "Data Extraction Agent", "count": 45, "hitl": False},
            {"from": "Data Extraction Agent", "to": "Orchestrator", "count": 42, "hitl": False},
            {"from": "Orchestrator", "to": "Statistical Analysis Agent", "count": 38, "hitl": False},
            {"from": "Statistical Analysis Agent", "to": "Orchestrator", "count": 35, "hitl": False},
            {"from": "Orchestrator", "to": "Visualization Agent", "count": 27, "hitl": False},
            {"from": "Visualization Agent", "to": "Orchestrator", "count": 25, "hitl": False},
            {"from": "Statistical Analysis Agent", "to": "ConfidenceEvaluator", "count": 32, "hitl": False},
            {"from": "ConfidenceEvaluator", "to": "Statistical Analysis Agent", "count": 24, "hitl": False},
            {"from": "ConfidenceEvaluator", "to": "HITLManager", "count": 18, "hitl": True},
            {"from": "HITLManager", "to": "User", "count": 18, "hitl": True},
            {"from": "User", "to": "HITLManager", "count": 18, "hitl": True},
            {"from": "HITLManager", "to": "Statistical Analysis Agent", "count": 15, "hitl": True},
            {"from": "Visualization Agent", "to": "ConfidenceEvaluator", "count": 22, "hitl": False},
            {"from": "ConfidenceEvaluator", "to": "Visualization Agent", "count": 16, "hitl": False},
            {"from": "ConfidenceEvaluator", "to": "HITLManager", "count": 12, "hitl": True},
            {"from": "HITLManager", "to": "Visualization Agent", "count": 10, "hitl": True},
        ]

        # Create a network graph
        G = nx.DiGraph()
        
        # Add nodes
        agents = [
            {"name": "Orchestrator", "color": "#dae8fc"},
            {"name": "Data Extraction Agent", "color": "#d5e8d4"},
            {"name": "Statistical Analysis Agent", "color": "#d5e8d4"},
            {"name": "Visualization Agent", "color": "#d5e8d4"},
            {"name": "ConfidenceEvaluator", "color": "#fff2cc"},
            {"name": "HITLManager", "color": "#f8cecc"},
            {"name": "User", "color": "#FFFFFF"}
        ]
        
        for agent in agents:
            G.add_node(agent["name"], color=agent["color"])
        
        # Add edges with weights
        for comm in communications:
            G.add_edge(comm["from"], comm["to"], weight=comm["count"], hitl=comm["hitl"])
        
        # Set positions
        pos = {
            "Orchestrator": (0.5, 0.8),
            "Data Extraction Agent": (0.2, 0.6),
            "Statistical Analysis Agent": (0.5, 0.6),
            "Visualization Agent": (0.8, 0.6),
            "ConfidenceEvaluator": (0.3, 0.4),
            "HITLManager": (0.7, 0.4),
            "User": (0.5, 0.2)
        }
        
        # Create figure
        plt.figure(figsize=(12, 8))
        
        # Draw nodes
        node_colors = [G.nodes[node]["color"] for node in G.nodes()]
        nx.draw_networkx_nodes(G, pos, node_size=2500, node_color=node_colors, alpha=0.9)
        
        # Draw edges with different colors and widths based on weight and HITL
        regular_edges = [(u, v) for u, v, d in G.edges(data=True) if not d.get('hitl', False)]
        hitl_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('hitl', False)]
        
        # Get edge weights for sizing
        regular_weights = [G[u][v]['weight'] / 5 for u, v in regular_edges]
        hitl_weights = [G[u][v]['weight'] / 5 for u, v in hitl_edges]
        
        # Draw regular edges
        nx.draw_networkx_edges(G, pos, edgelist=regular_edges, width=regular_weights, edge_color='blue', alpha=0.7, arrows=True, arrowsize=15)
        
        # Draw HITL edges
        nx.draw_networkx_edges(G, pos, edgelist=hitl_edges, width=hitl_weights, edge_color='red', alpha=0.7, arrows=True, arrowsize=15, style='dashed')
        
        # Draw node labels
        nx.draw_networkx_labels(G, pos, font_size=11, font_weight="bold")
        
        # Draw edge labels (communication counts)
        edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)
        
        plt.axis('off')
        st.pyplot(plt)
        
        # Add legend
        st.markdown("""
        **Legend:**
        - **Node colors** represent different agent types
        - **Blue edges** represent standard agent-to-agent communication
        - **Red dashed edges** represent human-in-the-loop interactions
        - **Edge numbers** show the frequency of communication
        - **Edge thickness** corresponds to communication frequency
        """)
        
        # Communication statistics
        st.subheader("Communication Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Total communications
            total_comms = sum(comm["count"] for comm in communications)
            st.metric("Total Communications", total_comms)
            
            # HITL percentage
            hitl_comms = sum(comm["count"] for comm in communications if comm["hitl"])
            hitl_percentage = (hitl_comms / total_comms) * 100
            st.metric("HITL Interactions", f"{hitl_percentage:.1f}%")
        
        with col2:
            # Most active agent
            agent_activity = {}
            for comm in communications:
                if comm["from"] not in agent_activity:
                    agent_activity[comm["from"]] = 0
                if comm["to"] not in agent_activity:
                    agent_activity[comm["to"]] = 0
                agent_activity[comm["from"]] += comm["count"]
                agent_activity[comm["to"]] += comm["count"]
            
            most_active = max(agent_activity.items(), key=lambda x: x[1])
            st.metric("Most Active Agent", most_active[0], f"{most_active[1]} interactions")
            
            # Most common path
            most_common = max(communications, key=lambda x: x["count"])
            st.metric("Most Common Path", f"{most_common['from']} → {most_common['to']}", f"{most_common['count']} times")
        
        with col3:
            # Average communications per workflow
            avg_comms = total_comms / 100  # Assuming 100 workflows
            st.metric("Avg. Communications per Workflow", f"{avg_comms:.1f}")
            
            # HITL efficiency
            st.metric("HITL Efficiency", "87%", "↑ 12%")

        # Add key features section
        st.subheader("Key Features")
        
        st.markdown("""
        - **Tiered Validation**: Multi-level validation process that escalates from simple rules to LLM only when needed
        - **Confidence Scoring**: Quantitative measurement of agent certainty
        - **Human-in-the-Loop**: Seamless integration of human expertise when needed
        - **Efficient Resource Usage**: Only uses expensive LLM calls when simpler methods are insufficient
        - **Context Preservation**: Maintains conversation context across interactions
        """)

# Performance Metrics page
elif page == "Performance Metrics":
    st.header("System Performance Metrics")
    st.write("""
    Our consolidated Orchestrator approach with human-in-the-loop capabilities delivers significant 
    improvements in efficiency, accuracy, and resource utilization.
    """)
    
    # Create tabs for different metrics
    tab1, tab2, tab3 = st.tabs(["Efficiency Metrics", "Accuracy Metrics", "Resource Utilization"])
    
    with tab1:
        st.subheader("Efficiency Improvements")
        
        # Create sample data
        categories = ['Processing Time', 'Response Latency', 'Throughput', 'Task Completion Rate']
        baseline = [100, 100, 100, 100]
        hitl_only = [85, 90, 105, 110]
        tiered_validation = [65, 72, 135, 125]
        
        # Create bar chart
        fig = go.Figure(data=[
            go.Bar(name='Baseline System', x=categories, y=baseline),
            go.Bar(name='HITL Only', x=categories, y=hitl_only),
            go.Bar(name='Tiered Validation with HITL', x=categories, y=tiered_validation)
        ])
        
        fig.update_layout(
            title="Efficiency Comparison (Baseline = 100%)",
            xaxis_title="Metric",
            yaxis_title="Relative Performance (%)",
            barmode='group',
            height=500
        )
        
        st.plotly_chart(fig)
        
        st.markdown("""
        **Key Efficiency Improvements:**
        - **35% reduction** in average processing time
        - **28% reduction** in response latency
        - **35% increase** in system throughput
        - **25% improvement** in task completion rate
        
        The tiered validation approach with HITL significantly outperforms both the baseline system and a 
        system with only HITL capabilities. By using a multi-level validation strategy, we minimize expensive 
        operations while maintaining high quality.
        """)
    
    with tab2:
        st.subheader("Accuracy Improvements")
        
        # Create sample data for accuracy metrics over time
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        baseline_acc = [76, 77, 75, 78, 77, 79]
        hitl_only_acc = [85, 86, 87, 86, 88, 87]
        tiered_hitl_acc = [85, 88, 91, 93, 95, 96]
        
        # Create line chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=baseline_acc, mode='lines+markers', name='Baseline System'))
        fig.add_trace(go.Scatter(x=months, y=hitl_only_acc, mode='lines+markers', name='HITL Only'))
        fig.add_trace(go.Scatter(x=months, y=tiered_hitl_acc, mode='lines+markers', name='Tiered Validation with HITL'))
        
        fig.update_layout(
            title="Accuracy Trend Over Time",
            xaxis_title="Month",
            yaxis_title="Accuracy (%)",
            yaxis=dict(range=[70, 100]),
            height=400
        )
        
        st.plotly_chart(fig)
        
        # Create a pie chart for error reduction
        labels = ['Remaining Errors', 'Errors Eliminated']
        values = [21, 79]  # 79% error reduction
        
        fig = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values, 
            hole=.3, 
            marker=dict(colors=['#FF6666', '#90EE90'])
        )])
        
        fig.update_layout(title="Error Reduction", height=300)
        st.plotly_chart(fig)
        
        st.markdown("""
        **Key Accuracy Improvements:**
        - **17 percentage point improvement** in overall accuracy compared to baseline
        - **9 percentage point improvement** over HITL-only approach
        - **79% reduction** in critical errors requiring rework
        - **Consistent upward trend** as the system learns from human feedback
        
        The combination of tiered validation and human-in-the-loop shows a clear advantage over both baseline 
        and HITL-only approaches, with accuracy continuing to improve over time as the system learns from 
        human interactions.
        """)
    
    with tab3:
        st.subheader("Resource Utilization")
        
        # Create sample data for resource utilization
        resource_types = ['LLM API Calls', 'Embedding API Calls', 'Human Interventions', 'Cache Hits']
        baseline_resources = [100, 100, 100, 0]  # Baseline has no caching
        hitl_only_resources = [95, 90, 65, 0]  # HITL only has no caching
        tiered_hitl_resources = [42, 65, 35, 55]  # Tiered approach uses caching
        
        # Create bar chart
        fig = go.Figure(data=[
            go.Bar(name='Baseline System', x=resource_types, y=baseline_resources),
            go.Bar(name='HITL Only', x=resource_types, y=hitl_only_resources),
            go.Bar(name='Tiered Validation with HITL', x=resource_types, y=tiered_hitl_resources)
        ])
        
        fig.update_layout(
            title="Resource Utilization (Baseline = 100%)",
            xaxis_title="Resource Type",
            yaxis_title="Relative Usage (%)",
            barmode='group',
            height=500
        )
        
        st.plotly_chart(fig)
        
        # Create a line chart showing cost over time
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        baseline_cost = [100, 102, 105, 103, 106, 108]
        hitl_only_cost = [90, 88, 85, 87, 84, 86]
        tiered_hitl_cost = [85, 75, 68, 62, 55, 48]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=baseline_cost, mode='lines+markers', name='Baseline System'))
        fig.add_trace(go.Scatter(x=months, y=hitl_only_cost, mode='lines+markers', name='HITL Only'))
        fig.add_trace(go.Scatter(x=months, y=tiered_hitl_cost, mode='lines+markers', name='Tiered Validation with HITL'))
        
        fig.update_layout(
            title="Relative Cost Over Time (Baseline Jan = 100%)",
            xaxis_title="Month",
            yaxis_title="Relative Cost (%)",
            height=400
        )
        
        st.plotly_chart(fig)
        
        st.markdown("""
        **Key Resource Optimization:**
        - **58% reduction** in expensive LLM API calls
        - **35% reduction** in human interventions required
        - **55% of validations** handled by cache hits, avoiding redundant processing
        - **52% overall cost reduction** after 6 months of operation
        
        The tiered validation approach with caching demonstrates significant resource efficiency improvements 
        over time. As the validation cache builds up and the system learns from human interactions, both 
        computational and human resources are used more efficiently. This leads to substantial cost savings 
        while maintaining or improving accuracy and performance metrics.
        """)
        
        # ROI calculation
        st.subheader("Return on Investment")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("6-Month Cost Savings", "52%")
            st.metric("Reduction in Human Hours", "65%")
            st.metric("Throughput Improvement", "35%")
        
        with col2:
            st.metric("Estimated Annual ROI", "285%")
            st.metric("Payback Period", "4.2 months")
            st.metric("Quality Improvement", "17 points")

# Add footer
st.markdown("---")
st.markdown("© 2023 Human-in-the-Loop Intelligent Orchestration System | All Rights Reserved")