"""
Overview Dashboard Page
Main landing page with key KPIs and summary visualizations.
Supports Boss Mode for executive view.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent.parent))

from data_loader import load_aggregated_stats, load_department_stats
from config import (
    CLUSTER_PROFILES, CLUSTER_COLORS, REPORTS_PATH,
    BOSS_SEGMENTS, BOSS_KEY_INSIGHTS, BOSS_BUNDLES, BOSS_SUMMARY
)
from components.charts import pie_chart, bar_chart
from components.metrics import kpi_row

# Check Boss Mode
boss_mode = st.session_state.get("boss_mode", False)

# Load data
with st.spinner("Loading statistics..."):
    stats = load_aggregated_stats()
    dept_stats = load_department_stats()

# =============================================================================
# BOSS MODE VIEW
# =============================================================================
if boss_mode:
    st.title("Executive Dashboard")
    st.markdown("### *How much can you earn with our insights?*")

    st.markdown("---")

    # Big 3 KPIs for Boss
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; text-align: center; color: white;">
            <h1 style="margin: 0; font-size: 3em;">{BOSS_KEY_INSIGHTS['revenue_potential']}</h1>
            <p style="margin: 5px 0; font-size: 1.2em;">Net Profit</p>
            <p style="margin: 0; font-size: 0.9em; opacity: 0.9;">{BOSS_KEY_INSIGHTS['revenue_description']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 25px; border-radius: 15px; text-align: center; color: white;">
            <h1 style="margin: 0; font-size: 3em;">{BOSS_KEY_INSIGHTS['savings_potential']}</h1>
            <p style="margin: 5px 0; font-size: 1.2em;">Avoided Losses</p>
            <p style="margin: 0; font-size: 0.9em; opacity: 0.9;">{BOSS_KEY_INSIGHTS['savings_description']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%); padding: 25px; border-radius: 15px; text-align: center; color: white;">
            <h1 style="margin: 0; font-size: 2em;">{BOSS_KEY_INSIGHTS['best_time']}</h1>
            <p style="margin: 5px 0; font-size: 1.2em;">Best Promo Time</p>
            <p style="margin: 0; font-size: 0.9em; opacity: 0.9;">{BOSS_KEY_INSIGHTS['best_time_description']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Executive Summary
    st.subheader("Executive Summary")

    for insight in BOSS_SUMMARY:
        st.markdown(f"- {insight}")

    st.markdown("---")

    # 3 Customer Segments (Simple)
    st.subheader("Your 3 Customer Types")

    cols = st.columns(3)
    for i, (cluster_id, segment) in enumerate(BOSS_SEGMENTS.items()):
        with cols[i]:
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-top: 4px solid {list(CLUSTER_COLORS.values())[cluster_id]};">
                <h3 style="margin: 0;">{segment['name']}</h3>
                <p style="font-size: 2em; margin: 10px 0; font-weight: bold;">{segment['share']}</p>
                <p style="margin: 5px 0; color: #666;">{segment['value']}</p>
                <hr>
                <p style="margin: 5px 0; font-size: 0.9em;"><strong>Action:</strong> {segment['action']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Top Bundles to Promote
    st.subheader("Bundles to Promote")
    st.markdown("*Sell these products together to increase average basket*")

    for bundle in BOSS_BUNDLES[:5]:
        col1, col2, col3 = st.columns([3, 1, 3])
        with col1:
            st.markdown(f"**{bundle['bundle']}**")
        with col2:
            st.markdown(f"<span style='color: green; font-weight: bold; font-size: 1.3em;'>{bundle['gain']}</span>", unsafe_allow_html=True)
        with col3:
            st.caption(bundle['why'])

    st.markdown("---")

    # Simple Action Plan
    st.subheader("Immediate Action Plan")

    st.markdown("""
    | Priority | Action | Expected Impact |
    |----------|--------|-----------------|
    | **HIGH** | Deploy 50,649 personalized offers | +5,378€ net profit |
    | **HIGH** | Block unprofitable promotions (GO/NO GO system) | 174€ saved |
    | **MEDIUM** | Sunday 10am-2pm targeted campaigns | +44% order volume |
    | **MEDIUM** | Premium segment VIP program (65% loyalty) | Higher retention |
    """)

    st.markdown("---")
    st.caption("Switch to Analyst mode (sidebar) for technical details")

# =============================================================================
# ANALYST MODE VIEW (Original)
# =============================================================================
else:
    st.title("Overview Dashboard")
    st.markdown("Welcome to the **Retail Analytics Dashboard** - Insights from Instacart grocery data.")

    st.markdown("---")

    # KPI Row
    st.subheader("Key Metrics")

    if stats:
        kpi_row([
            ("Total Customers", f"{stats.get('total_customers', 0):,}", None),
            ("Total Orders", f"{stats.get('total_orders', 0):,}", None),
            ("Total Products", f"{stats.get('total_products', 0):,}", None),
            ("Avg Reorder Rate", f"{stats.get('avg_reorder_rate', 0):.1%}", None),
        ])
    else:
        st.warning("Unable to load statistics. Please ensure the data file exists.")

    st.markdown("---")

    # Two-column layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Customer Personas Distribution")

        # Persona distribution from config
        persona_labels = [p["name"] for p in CLUSTER_PROFILES.values()]
        persona_sizes = [p["size_pct"] for p in CLUSTER_PROFILES.values()]
        persona_colors = list(CLUSTER_COLORS.values())

        fig_personas = pie_chart(
            labels=persona_labels,
            values=persona_sizes,
            colors=persona_colors,
            title="Customer Segmentation (3 Clusters)",
            hole=0.4
        )
        st.plotly_chart(fig_personas, use_container_width=True)

    with col2:
        st.subheader("Top Departments by Volume")

        if not dept_stats.empty:
            top_depts = dept_stats.head(10)
            fig_depts = bar_chart(
                data=top_depts,
                x_col="department",
                y_col="total_items",
                title="Top 10 Departments by Total Items",
                color="reorder_rate",
                orientation="h"
            )
            st.plotly_chart(fig_depts, use_container_width=True)

    st.markdown("---")

    # Persona Summaries
    st.subheader("Persona Profiles Summary")

    cols = st.columns(3)

    for i, (cluster_id, profile) in enumerate(CLUSTER_PROFILES.items()):
        with cols[i]:
            color = CLUSTER_COLORS[cluster_id]
            st.markdown(f"""
            <div style="background-color: {color}20; padding: 15px; border-radius: 10px; border-left: 4px solid {color};">
            <h4 style="color: {color}; margin: 0;">{profile['name']}</h4>
            <p style="margin: 5px 0;"><strong>{profile['size_pct']:.1f}%</strong> of customers</p>
            <p style="margin: 5px 0; font-size: 0.9em;">{profile['description']}</p>
            <hr style="margin: 10px 0;">
            <p style="margin: 3px 0; font-size: 0.85em;">Avg Basket: <strong>{profile['avg_basket_size']:.1f}</strong> items</p>
            <p style="margin: 3px 0; font-size: 0.85em;">Reorder Rate: <strong>{profile['reorder_ratio']:.1%}</strong></p>
            <p style="margin: 3px 0; font-size: 0.85em;">Health Index: <strong>{profile['HAI']:.1%}</strong></p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Show existing report images if available
    st.subheader("Analysis Reports")

    reports_path = Path(__file__).parent.parent / REPORTS_PATH

    if reports_path.exists():
        report_images = list(reports_path.glob("*.png"))

        if report_images:
            # Show nutriscore overview if available
            nutriscore_img = reports_path / "nutriscore_overview.png"
            if nutriscore_img.exists():
                st.image(str(nutriscore_img), caption="Nutriscore Distribution Overview", use_container_width=True)

            # Show other reports in expander
            with st.expander("View More Reports"):
                cols = st.columns(2)
                for idx, img in enumerate(report_images[:6]):
                    if img.name != "nutriscore_overview.png":
                        with cols[idx % 2]:
                            st.image(str(img), caption=img.stem.replace("_", " ").title(), use_container_width=True)
        else:
            st.info("No report images found in the reports folder.")
    else:
        st.info("Reports folder not found.")

    st.markdown("---")
    st.caption("Data source: Instacart Online Grocery Basket Analysis Dataset")
