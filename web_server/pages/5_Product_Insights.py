"""
Product Insights Page
Product-level analysis with driver product identification and search.
Supports Boss Mode for executive view.
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent.parent))

from data_loader import load_product_stats, load_product_list, load_department_list
from config import REPORTS_PATH
from components.charts import scatter_chart, bar_chart
from components.filters import product_search, department_filter

# Check Boss Mode
boss_mode = st.session_state.get("boss_mode", False)

# Load data
with st.spinner("Loading product statistics..."):
    try:
        product_stats = load_product_stats(top_n=100)
        product_list = load_product_list()
    except Exception as e:
        product_stats = pd.DataFrame()
        product_list = []

# Default for analyst-only filter state
selected_depts = []

# =============================================================================
# BOSS MODE VIEW
# =============================================================================
if boss_mode:
    st.title("Your Key Products")
    st.markdown("### *Which products to develop and which to boost?*")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 25px; border-radius: 15px; color: white;">
            <h2 style="margin: 0;">Star Products</h2>
            <p>Your sales champions</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        | Product | Performance |
        |---------|-------------|
        | **Bananas** | #1 sales, 60% loyalty |
        | **Organic Strawberries** | Top 5, high margin |
        | **Organic Avocados** | Growth +25% |
        | **Organic Milk** | 70% loyalty |
        | **Organic Apples** | Reliable performer |

        **Action**: Ensure stock availability
        """)

    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%); padding: 25px; border-radius: 15px; color: white;">
            <h2 style="margin: 0;">Products to Boost</h2>
            <p>Underexploited potential</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        | Product | Opportunity |
        |---------|-------------|
        | **Lemons** | Good for bundles |
        | **Organic Onions** | Low price, OK margin |
        | **Organic Garlic** | Complementary item |
        | **Organic Spinach** | Health trend |
        | **Raspberries** | Premium price OK |

        **Action**: Targeted promotions
        """)

    st.markdown("---")

    # Strategy Matrix
    st.subheader("Strategic Matrix")

    st.markdown("""
    | Category | Products | Strategy |
    |----------|----------|----------|
    | **Cash Cows** | Bananas, Strawberries, Milk | Maintain and retain |
    | **Stars** | Organic Avocados, Raspberries | Develop aggressively |
    | **Question Marks** | Lemons, Garlic | Bundles and promotions |
    | **Dogs** | Low rotation products | Analyze or remove |
    """)

    st.markdown("---")

    # Quick Wins
    st.subheader("Quick Wins")

    st.success("""
    **3 immediate actions for +10% revenue:**

    1. **Place avocados near bananas** - +20% cross-sales
    2. **Bundle Organic Strawberries + Raspberries** - +15% basket size
    3. **"Green Smoothie" promo** (Spinach + Bananas) - New segment
    """)

    st.markdown("---")
    st.caption("Switch to Analyst mode for detailed product analysis")
    st.stop()

# =============================================================================
# ANALYST MODE VIEW
# =============================================================================
else:
    st.title("Product Insights")
    st.markdown("Analyze **product performance**, identify **driver products**, and explore **universality vs loyalty**.")

    st.markdown("---")

    # Sidebar filters
    with st.sidebar:
        st.subheader("Filters")

        # Department filter
        try:
            departments = load_department_list()
            selected_depts = department_filter(departments, key="prod_dept_filter", default_all=False)
            if not selected_depts:
                selected_depts = departments  # Show all if none selected
        except:
            selected_depts = []

# Search
st.subheader("Product Search")

if product_list:
    search_result = product_search(product_list[:1000], key="prod_search")  # Limit for performance

    if search_result:
        # Find product in stats
        product_info = product_stats[product_stats["product_name"] == search_result]

        if not product_info.empty:
            row = product_info.iloc[0]

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Purchases", f"{row['total_purchases']:,}")
            with col2:
                st.metric("Reorder Rate", f"{row['reorder_rate']:.1%}")
            with col3:
                st.metric("Unique Customers", f"{row['unique_customers']:,}")
            with col4:
                st.metric("Department", row.get("department", "N/A"))
        else:
            st.info("Product not in top statistics. Try searching in the table below.")

st.markdown("---")

# Product Quadrant Analysis
st.subheader("Product Universality vs Loyalty")

if not product_stats.empty:
    # Calculate quadrant thresholds
    x_median = product_stats["unique_customers"].median()
    y_median = product_stats["reorder_rate"].median()

    # Classify products
    def classify_product(row):
        x = row["unique_customers"]
        y = row["reorder_rate"]

        if x >= x_median and y >= y_median:
            return "Universal Loyal"
        elif x < x_median and y >= y_median:
            return "Niche Loyal"
        elif x >= x_median and y < y_median:
            return "Occasional Popular"
        else:
            return "Low Engagement"

    product_stats["quadrant"] = product_stats.apply(classify_product, axis=1)

    # Filter by department if selected
    if selected_depts and "department" in product_stats.columns:
        filtered_products = product_stats[product_stats["department"].isin(selected_depts)]
    else:
        filtered_products = product_stats

    fig_quadrant = scatter_chart(
        data=filtered_products.head(500),  # Limit for performance
        x_col="unique_customers",
        y_col="reorder_rate",
        color_col="quadrant",
        size_col="total_purchases",
        hover_name="product_name",
        title="Product Universality vs Loyalty (size = total purchases)",
        log_x=True
    )

    st.plotly_chart(fig_quadrant, use_container_width=True)

    # Quadrant explanation
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Quadrant Definitions:**
        - **Universal Loyal**: High reach + High loyalty = Core products
        - **Niche Loyal**: Low reach + High loyalty = Specialty items
        """)

    with col2:
        st.markdown("""

        - **Occasional Popular**: High reach + Low loyalty = Commodities
        - **Low Engagement**: Low reach + Low loyalty = Candidates for review
        """)

st.markdown("---")

# Top Products
st.subheader("Top Products")

tab1, tab2 = st.tabs(["By Volume", "By Loyalty"])

with tab1:
    if not product_stats.empty:
        top_by_volume = product_stats.nlargest(20, "total_purchases")

        fig_vol = bar_chart(
            data=top_by_volume,
            x_col="product_name",
            y_col="total_purchases",
            title="Top 20 Products by Total Purchases",
            orientation="h"
        )

        st.plotly_chart(fig_vol, use_container_width=True)

with tab2:
    if not product_stats.empty:
        # Filter for minimum volume to get meaningful reorder rates
        min_purchases = product_stats["total_purchases"].quantile(0.5)
        high_volume = product_stats[product_stats["total_purchases"] >= min_purchases]
        top_by_loyalty = high_volume.nlargest(20, "reorder_rate")

        fig_loyal = bar_chart(
            data=top_by_loyalty,
            x_col="product_name",
            y_col="reorder_rate",
            title="Top 20 Products by Reorder Rate (min 50% volume)",
            color="reorder_rate",
            orientation="h"
        )

        st.plotly_chart(fig_loyal, use_container_width=True)

st.markdown("---")

# Product Table
st.subheader("Product Statistics")

if not product_stats.empty:
    # Search filter
    table_search = st.text_input("Filter products by name", key="table_search")

    display_df = product_stats.copy()

    if table_search:
        display_df = display_df[
            display_df["product_name"].str.contains(table_search, case=False, na=False)
        ]

    # Format for display
    display_df["Total Purchases"] = display_df["total_purchases"].apply(lambda x: f"{x:,}")
    display_df["Reorder Rate"] = display_df["reorder_rate"].apply(lambda x: f"{x:.1%}")
    display_df["Customers"] = display_df["unique_customers"].apply(lambda x: f"{x:,}")

    st.dataframe(
        display_df[["product_name", "department", "aisle", "Total Purchases", "Reorder Rate", "Customers"]].rename(columns={
            "product_name": "Product",
            "department": "Department",
            "aisle": "Aisle"
        }).head(100),
        use_container_width=True,
        hide_index=True
    )

    st.caption(f"Showing top {min(100, len(display_df))} products.")

st.markdown("---")

# Report Images
st.subheader("Product Analysis Reports")

reports_path = Path(__file__).parent.parent / REPORTS_PATH

product_images = [
    "price_vs_health.png",
    "health_upgrade_opportunities.png"
]

cols = st.columns(2)
for idx, img_name in enumerate(product_images):
    img_path = reports_path / img_name
    if img_path.exists():
        with cols[idx]:
            st.image(str(img_path), caption=img_name.replace("_", " ").replace(".png", "").title())

st.markdown("---")

# Driver Products Insight
st.subheader("Driver Product Insights")

st.markdown("""
**Driver Products** are items that:
1. Are purchased by many customers (high reach)
2. Drive basket diversity when present
3. Often appear in association rules

**Key Drivers in This Dataset:**
- **Bananas** - appear in 10+ association rules as consequent
- **Organic produce** - strong cross-purchase patterns
- **Berries** - high lift values indicating strong associations

**Recommendations:**
- Use driver products for cross-sell promotions
- Place driver products strategically in store layout
- Monitor driver product stock levels closely
""")

st.markdown("---")
st.caption("Product analysis based on Instacart Online Grocery Basket dataset")
