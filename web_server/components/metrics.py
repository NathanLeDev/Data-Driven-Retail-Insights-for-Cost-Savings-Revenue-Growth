"""
Reusable metric/KPI card components.
"""

import streamlit as st


def kpi_card(label: str, value: str, delta: str = None, delta_color: str = "normal"):
    """
    Display a single KPI metric card.

    Args:
        label: Metric label
        value: Metric value (formatted string)
        delta: Optional delta/change value
        delta_color: Color scheme for delta ("normal", "inverse", "off")
    """
    st.metric(
        label=label,
        value=value,
        delta=delta,
        delta_color=delta_color
    )


def kpi_row(metrics: list):
    """
    Display a row of KPI cards.

    Args:
        metrics: List of tuples (label, value, delta) or (label, value)
    """
    cols = st.columns(len(metrics))

    for col, metric in zip(cols, metrics):
        with col:
            if len(metric) >= 3:
                kpi_card(metric[0], metric[1], metric[2])
            else:
                kpi_card(metric[0], metric[1])


def stat_box(title: str, value: str, description: str = None, icon: str = None):
    """
    Display a styled statistics box.

    Args:
        title: Box title
        value: Main value to display
        description: Optional description text
        icon: Optional emoji icon
    """
    with st.container():
        if icon:
            st.markdown(f"### {icon} {title}")
        else:
            st.markdown(f"### {title}")

        st.markdown(f"# {value}")

        if description:
            st.caption(description)


def progress_metric(label: str, value: float, max_value: float = 1.0, format_str: str = "{:.1%}"):
    """
    Display a metric with a progress bar.

    Args:
        label: Metric label
        value: Current value
        max_value: Maximum value for progress calculation
        format_str: Format string for the value display
    """
    progress = min(value / max_value, 1.0) if max_value > 0 else 0

    st.markdown(f"**{label}**")
    st.progress(progress)
    st.caption(format_str.format(value))
