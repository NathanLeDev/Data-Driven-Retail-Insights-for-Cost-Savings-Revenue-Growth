"""
Reusable filter components for the Streamlit app.
"""

import streamlit as st
from config import CLUSTER_NAMES


def persona_filter(key: str = "persona_filter", default_all: bool = True) -> list:
    """
    Multi-select filter for customer personas/clusters.

    Args:
        key: Unique key for the widget
        default_all: If True, all personas selected by default

    Returns:
        List of selected persona names
    """
    personas = list(CLUSTER_NAMES.values())
    default = personas if default_all else []

    return st.multiselect(
        "Select Customer Personas",
        options=personas,
        default=default,
        key=key
    )


def product_search(products: list, key: str = "product_search") -> str:
    """
    Product search with autocomplete dropdown.

    Args:
        products: List of product names
        key: Unique key for the widget

    Returns:
        Selected product name or empty string
    """
    return st.selectbox(
        "Search Product",
        options=[""] + sorted(products),
        key=key,
        help="Start typing to search for a product"
    )


def department_filter(departments: list, key: str = "dept_filter", default_all: bool = True) -> list:
    """
    Multi-select filter for departments.

    Args:
        departments: List of department names
        key: Unique key for the widget
        default_all: If True, all departments selected by default

    Returns:
        List of selected department names
    """
    default = departments if default_all else []

    return st.multiselect(
        "Select Departments",
        options=sorted(departments),
        default=default,
        key=key
    )


def time_range_filter(key: str = "time_range") -> tuple:
    """
    Hour of day range slider.

    Args:
        key: Unique key for the widget

    Returns:
        Tuple of (start_hour, end_hour)
    """
    return st.slider(
        "Hour Range",
        min_value=0,
        max_value=23,
        value=(6, 22),
        key=key,
        help="Filter orders by time of day"
    )


def day_of_week_filter(key: str = "dow_filter") -> list:
    """
    Multi-select filter for days of the week.

    Args:
        key: Unique key for the widget

    Returns:
        List of selected day indices (0=Sunday, 6=Saturday)
    """
    days = {
        "Sunday": 0,
        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 3,
        "Thursday": 4,
        "Friday": 5,
        "Saturday": 6
    }

    selected = st.multiselect(
        "Select Days",
        options=list(days.keys()),
        default=list(days.keys()),
        key=key
    )

    return [days[d] for d in selected]


def metric_selector(metrics: list, key: str = "metric_select", default: str = None) -> str:
    """
    Dropdown to select a metric for visualization.

    Args:
        metrics: List of metric names
        key: Unique key for the widget
        default: Default selected metric

    Returns:
        Selected metric name
    """
    default_idx = metrics.index(default) if default and default in metrics else 0

    return st.selectbox(
        "Select Metric",
        options=metrics,
        index=default_idx,
        key=key
    )
