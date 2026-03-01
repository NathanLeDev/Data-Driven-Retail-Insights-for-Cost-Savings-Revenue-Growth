"""
Retail Analytics Dashboard - Main Application
Streamlit multi-page application for Instacart data analysis.
"""

import streamlit as st

from config import APP_TITLE, APP_ICON

# Page configuration - must be first Streamlit command
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define pages
overview_page = st.Page("pages/1_Overview.py", title="Overview", default=True)
segmentation_page = st.Page("pages/2_Customer_Segmentation.py", title="Customer Segmentation")
association_page = st.Page("pages/3_Association_Rules.py", title="Association Rules")
eda_page = st.Page("pages/4_EDA_Explorer.py", title="EDA Explorer")
product_page = st.Page("pages/5_Product_Insights.py", title="Product Insights")

# Navigation
pg = st.navigation([
    overview_page,
    segmentation_page,
    association_page,
    eda_page,
    product_page
])

# Sidebar branding
with st.sidebar:
    st.title(APP_TITLE)
    st.markdown("---")

    # Boss Mode Toggle
    boss_mode = st.toggle(
        "Executive Mode",
        key="boss_mode",
        help="Simplified view for decision makers - focus on business impact"
    )

    if boss_mode:
        st.success("Executive Mode - Business View")
    else:
        st.info("Analyst Mode - Detailed View")

    st.markdown("---")
    st.markdown("""
    **Data-Driven Retail Insights**

    Analysis of Instacart Online Grocery data for:
    - Customer segmentation
    - Market basket analysis
    - Business optimization
    """)
    st.markdown("---")
    st.caption("DSTI - Python ML Project 2025")

# Run the selected page
pg.run()
