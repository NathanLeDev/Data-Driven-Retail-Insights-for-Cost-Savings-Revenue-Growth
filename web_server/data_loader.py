"""
Data loading utilities with Polars for efficient handling of large datasets.
Uses Streamlit caching for performance.
"""

import streamlit as st
import polars as pl
import pandas as pd
from pathlib import Path

from config import DATA_PATH


def get_data_path() -> Path:
    """Get the absolute path to the data file."""
    return Path(__file__).parent / DATA_PATH


@st.cache_data(ttl=3600, show_spinner="Loading aggregated statistics...")
def load_aggregated_stats() -> dict:
    """
    Load pre-computed aggregate statistics using Polars lazy evaluation.
    This is fast even on 33M rows as it uses columnar operations.
    """
    data_path = get_data_path()

    if not data_path.exists():
        st.error(f"Data file not found: {data_path}")
        return {}

    lf = pl.scan_parquet(str(data_path))

    stats = {
        "total_orders": lf.select(pl.col("order_id").n_unique()).collect().item(),
        "total_customers": lf.select(pl.col("user_id").n_unique()).collect().item(),
        "total_products": lf.select(pl.col("product_id").n_unique()).collect().item(),
        "total_transactions": lf.select(pl.count()).collect().item(),
        "avg_reorder_rate": lf.select(pl.col("reordered").mean()).collect().item(),
    }

    return stats


@st.cache_data(ttl=3600, show_spinner="Loading department statistics...")
def load_department_stats() -> pd.DataFrame:
    """Load department-level aggregations."""
    data_path = get_data_path()
    lf = pl.scan_parquet(str(data_path))

    dept_stats = (
        lf.group_by("department")
        .agg([
            pl.count().alias("total_items"),
            pl.col("reordered").mean().alias("reorder_rate"),
            pl.col("user_id").n_unique().alias("unique_customers"),
            pl.col("order_id").n_unique().alias("unique_orders"),
        ])
        .sort("total_items", descending=True)
        .collect()
        .to_pandas()
    )

    return dept_stats


@st.cache_data(ttl=3600, show_spinner="Loading temporal patterns...")
def load_temporal_stats() -> dict:
    """Load temporal distribution statistics."""
    data_path = get_data_path()
    lf = pl.scan_parquet(str(data_path))

    # Hourly distribution
    hourly = (
        lf.group_by("order_hour_of_day")
        .agg(pl.count().alias("count"))
        .sort("order_hour_of_day")
        .collect()
        .to_pandas()
    )

    # Daily distribution
    daily = (
        lf.group_by("order_dow")
        .agg(pl.count().alias("count"))
        .sort("order_dow")
        .collect()
        .to_pandas()
    )

    # Heatmap data: day x hour
    heatmap = (
        lf.group_by(["order_dow", "order_hour_of_day"])
        .agg(pl.count().alias("count"))
        .collect()
        .to_pandas()
    )

    # Reorder rate heatmap
    reorder_heatmap = (
        lf.group_by(["order_dow", "order_hour_of_day"])
        .agg(pl.col("reordered").mean().alias("reorder_rate"))
        .collect()
        .to_pandas()
    )

    return {
        "hourly": hourly,
        "daily": daily,
        "heatmap": heatmap,
        "reorder_heatmap": reorder_heatmap
    }


@st.cache_data(ttl=3600, show_spinner="Loading product statistics...")
def load_product_stats(top_n: int = 50) -> pd.DataFrame:
    """Load top products by various metrics."""
    data_path = get_data_path()
    lf = pl.scan_parquet(str(data_path))

    product_stats = (
        lf.group_by(["product_id", "product_name", "department", "aisle"])
        .agg([
            pl.count().alias("total_purchases"),
            pl.col("reordered").mean().alias("reorder_rate"),
            pl.col("user_id").n_unique().alias("unique_customers"),
            pl.col("order_id").n_unique().alias("unique_orders"),
        ])
        .sort("total_purchases", descending=True)
        .head(top_n * 10)  # Get more for filtering
        .collect()
        .to_pandas()
    )

    return product_stats


@st.cache_data(ttl=3600, show_spinner="Computing customer features...")
def load_customer_features() -> pd.DataFrame:
    """
    Compute customer-level features for segmentation analysis.
    This aggregates data at the user level.
    """
    data_path = get_data_path()
    lf = pl.scan_parquet(str(data_path))

    customer_features = (
        lf.group_by("user_id")
        .agg([
            pl.col("order_id").n_unique().alias("total_orders"),
            pl.col("days_since_prior_order").mean().alias("avg_days_between"),
            pl.col("reordered").mean().alias("reorder_ratio"),
            (pl.col("product_id").count() / pl.col("order_id").n_unique()).alias("avg_basket_size"),
            pl.col("department").n_unique().alias("dept_diversity"),
        ])
        .collect()
        .to_pandas()
    )

    # Compute order frequency
    customer_features["order_frequency"] = (
        customer_features["total_orders"] /
        (customer_features["avg_days_between"].fillna(30) + 1)
    )

    return customer_features


@st.cache_data(ttl=3600, show_spinner="Loading sample data...")
def load_sample_data(n_rows: int = 500_000) -> pd.DataFrame:
    """
    Load a sample of the full dataset for interactive visualizations.
    Sampling ensures fast rendering while maintaining data distribution.
    """
    data_path = get_data_path()

    df = (
        pl.scan_parquet(str(data_path))
        .head(n_rows)
        .collect()
        .to_pandas()
    )

    return df


@st.cache_data(ttl=3600, show_spinner="Loading product list...")
def load_product_list() -> list:
    """Load unique product names for search/filter."""
    data_path = get_data_path()
    lf = pl.scan_parquet(str(data_path))

    products = (
        lf.select(pl.col("product_name").unique())
        .collect()
        .to_pandas()["product_name"]
        .sort_values()
        .tolist()
    )

    return products


@st.cache_data(ttl=3600, show_spinner="Loading department list...")
def load_department_list() -> list:
    """Load unique department names."""
    data_path = get_data_path()
    lf = pl.scan_parquet(str(data_path))

    departments = (
        lf.select(pl.col("department").unique())
        .collect()
        .to_pandas()["department"]
        .sort_values()
        .tolist()
    )

    return departments


@st.cache_data(ttl=3600, show_spinner="Loading aisle list...")
def load_aisle_list() -> list:
    """Load unique aisle names."""
    data_path = get_data_path()
    lf = pl.scan_parquet(str(data_path))

    aisles = (
        lf.select(pl.col("aisle").unique())
        .collect()
        .to_pandas()["aisle"]
        .sort_values()
        .tolist()
    )

    return aisles
