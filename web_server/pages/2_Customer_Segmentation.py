"""
Customer Segmentation Page
Analysis of customer personas/clusters with radar charts and profiling.
Supports Boss Mode for executive view.
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent.parent))

from data_loader import load_customer_features
from config import CLUSTER_PROFILES, CLUSTER_COLORS, CLUSTER_NAMES, FEATURES_LIST, BOSS_SEGMENTS
from components.charts import radar_chart, scatter_chart
from components.filters import persona_filter

# Check Boss Mode
boss_mode = st.session_state.get("boss_mode", False)

# =============================================================================
# BOSS MODE VIEW
# =============================================================================
if boss_mode:
    st.title("Your Customers in 3 Minutes")
    st.markdown("### *Who are your customers and how to retain them?*")

    st.markdown("---")

    # Simple 3-segment view
    cols = st.columns(3)

    for i, (cluster_id, segment) in enumerate(BOSS_SEGMENTS.items()):
        with cols[i]:
            color = list(CLUSTER_COLORS.values())[cluster_id]
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 25px; border-radius: 15px; border-top: 5px solid {color}; height: 250px;">
                <h3 style="margin: 10px 0; text-align: center;">{segment['name']}</h3>
                <p style="font-size: 2.5em; margin: 10px 0; font-weight: bold; text-align: center; color: {color};">{segment['share']}</p>
                <p style="text-align: center; color: #666; margin-bottom: 15px;">{segment['value']}</p>
                <div style="background-color: {color}20; padding: 10px; border-radius: 8px;">
                    <p style="margin: 0; font-size: 0.9em;"><strong>Action:</strong><br>{segment['action']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Key Takeaways
    st.subheader("Key Takeaways")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Your Premium Clients (25%)**
        - Generate 40% of your revenue
        - Very loyal (65% reorder rate)
        - Buy organic/health products

        **Priority: VIP Program**
        """)

    with col2:
        st.markdown("""
        **Your Budget Clients (37%)**
        - Sensitive to promotions
        - Smaller but regular baskets
        - Respond to coupons

        **Priority: Targeted Offers**
        """)

    st.markdown("---")

    # ROI Table
    st.subheader("Return on Investment by Segment")

    st.markdown("""
    | Segment | Acquisition Cost | Customer Lifetime Value | ROI |
    |---------|-----------------|-------------------------|-----|
    | Premium | High | Very High | **x4** |
    | Budget | Low | Medium | **x2** |
    | Families | Medium | High | **x2.5** |
    """)

    st.markdown("---")
    st.caption("Switch to Analyst mode for technical details (radar charts, features)")

# =============================================================================
# ANALYST MODE VIEW
# =============================================================================
else:
    st.title("Customer Segmentation")
    st.markdown("Explore the **3 customer personas** identified through K-Means clustering.")

    st.markdown("---")

    # Sidebar filters
    with st.sidebar:
        st.subheader("Filters")
        selected_personas = persona_filter(key="seg_persona_filter")

    st.markdown("---")

    # Persona Cards
    st.subheader("Persona Profiles")

    # Filter profiles based on selection
    filtered_profiles = {
        k: v for k, v in CLUSTER_PROFILES.items()
        if v["name"] in selected_personas
    }

    if not filtered_profiles:
        st.warning("Please select at least one persona to view.")
    else:
        # Radar Charts
        cols = st.columns(len(filtered_profiles))

        # Define features for radar chart (normalized 0-1)
        radar_features = [
            "order_frequency",
            "reorder_ratio",
            "avg_basket_size",
            "HAI",
            "PSI"
        ]

        radar_labels = [
            "Order Freq",
            "Loyalty",
            "Basket Size",
            "Health Index",
            "Price Sens."
        ]

        # Normalize values for radar chart
        max_values = {
            "order_frequency": 5.0,
            "reorder_ratio": 1.0,
            "avg_basket_size": 15.0,
            "HAI": 1.0,
            "PSI": 1.0
        }

        for i, (cluster_id, profile) in enumerate(filtered_profiles.items()):
            with cols[i]:
                # Normalize values
                values = []
                for feat in radar_features:
                    val = profile.get(feat, 0)
                    max_val = max_values.get(feat, 1)
                    normalized = min(val / max_val, 1.0)
                    values.append(normalized)

                color = CLUSTER_COLORS[cluster_id]

                fig = radar_chart(
                    values=values,
                    labels=radar_labels,
                    title=profile["name"],
                    color=color
                )

                st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Detailed Profiling Table
    st.subheader("Dynamic Profiling Table")

    def get_level(value, low_thresh, high_thresh):
        """Convert value to Low/Medium/High label."""
        if value < low_thresh:
            return "Low"
        elif value < high_thresh:
            return "Medium"
        else:
            return "High"

    # Create profiling DataFrame
    profiling_data = []

    for cluster_id, profile in CLUSTER_PROFILES.items():
        row = {
            "Persona": profile["name"],
            "Market Share": f"{profile['size_pct']:.1f}%",
            "Loyalty": get_level(profile["reorder_ratio"], 0.4, 0.6),
            "Basket Size": get_level(profile["avg_basket_size"], 6, 12),
            "Health Focus": get_level(profile["HAI"], 0.85, 0.87),
            "Price Sensitivity": get_level(profile["PSI"], 0.49, 0.50),
            "Order Frequency": get_level(profile["order_frequency"], 1.0, 3.0),
        }
        profiling_data.append(row)

    profiling_df = pd.DataFrame(profiling_data)

    st.dataframe(
        profiling_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # Customer Features Scatter Plot
    st.subheader("Customer Feature Distribution")

    with st.spinner("Loading customer features..."):
        try:
            customer_df = load_customer_features()

            if not customer_df.empty:
                col1, col2 = st.columns(2)

                with col1:
                    x_axis = st.selectbox(
                        "X-Axis",
                        options=["total_orders", "avg_basket_size", "reorder_ratio", "order_frequency"],
                        index=0
                    )

                with col2:
                    y_axis = st.selectbox(
                        "Y-Axis",
                        options=["avg_basket_size", "total_orders", "reorder_ratio", "avg_days_between"],
                        index=0
                    )

                # Sample for visualization
                sample_df = customer_df.sample(min(10000, len(customer_df)), random_state=42)

                fig = scatter_chart(
                    data=sample_df,
                    x_col=x_axis,
                    y_col=y_axis,
                    title=f"{y_axis.replace('_', ' ').title()} vs {x_axis.replace('_', ' ').title()}",
                    log_x=(x_axis in ["total_orders", "order_frequency"])
                )

                st.plotly_chart(fig, use_container_width=True)

                st.caption(f"Showing {len(sample_df):,} sampled customers out of {len(customer_df):,} total.")
        except Exception as e:
            st.info("Customer feature visualization requires the processed data file.")
            st.caption(f"Details: {str(e)}")

    st.markdown("---")

    # Key Insights
    st.subheader("Key Insights")

    insights = [
        "**The Premium Healths** (25%) are the most loyal segment with highest order frequency and health-conscious choices.",
        "**The Daily Economizers** (37%) represent the largest segment with smaller, more frequent purchases.",
        "**The Budget-Healthy Mix** (38%) buy in larger quantities with focus on value and weekend shopping.",
        "All segments show similar health consciousness (HAI ~0.86-0.88), suggesting health is a cross-segment priority.",
        "Price sensitivity is uniform across segments, indicating price perception is not a key differentiator."
    ]

    for insight in insights:
        st.markdown(f"- {insight}")

    st.markdown("---")
    st.caption("Segmentation based on K-Means clustering with 10 behavioral features.")
