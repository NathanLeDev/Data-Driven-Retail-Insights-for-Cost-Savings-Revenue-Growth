"""
Reusable chart components using Plotly.
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd


def radar_chart(
    values: list,
    labels: list,
    title: str,
    color: str = "#1f77b4",
    fill_opacity: float = 0.3
) -> go.Figure:
    """
    Create a radar/spider chart for persona profiles.

    Args:
        values: List of values (0-1 normalized)
        labels: List of feature labels
        title: Chart title
        color: Line and fill color
        fill_opacity: Opacity of the fill area

    Returns:
        Plotly Figure object
    """
    # Close the polygon
    values_closed = values + [values[0]]
    labels_closed = labels + [labels[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=labels_closed,
        fill='toself',
        fillcolor=color,
        opacity=fill_opacity,
        line=dict(color=color, width=2),
        name=title
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                tickfont=dict(size=11)
            )
        ),
        showlegend=False,
        title=dict(text=title, x=0.5, font=dict(size=14)),
        margin=dict(l=60, r=60, t=60, b=60),
        height=400
    )

    return fig


def heatmap_chart(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    value_col: str,
    x_labels: list = None,
    y_labels: list = None,
    title: str = "",
    colorscale: str = "Viridis"
) -> go.Figure:
    """
    Create a heatmap chart.

    Args:
        data: DataFrame with x, y, and value columns
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        value_col: Column name for values
        x_labels: Custom x-axis labels
        y_labels: Custom y-axis labels
        title: Chart title
        colorscale: Plotly colorscale name

    Returns:
        Plotly Figure object
    """
    # Pivot data for heatmap
    pivot = data.pivot(index=y_col, columns=x_col, values=value_col)

    # Apply custom labels if provided
    if y_labels:
        pivot.index = y_labels
    if x_labels:
        pivot.columns = x_labels

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale=colorscale,
        hoverongaps=False
    ))

    fig.update_layout(
        title=dict(text=title, x=0.5),
        xaxis_title=x_col.replace("_", " ").title(),
        yaxis_title=y_col.replace("_", " ").title(),
        height=400
    )

    return fig


def pie_chart(
    labels: list,
    values: list,
    colors: list = None,
    title: str = "",
    hole: float = 0.4
) -> go.Figure:
    """
    Create a donut/pie chart.

    Args:
        labels: Category labels
        values: Values for each category
        colors: Custom colors for each category
        title: Chart title
        hole: Size of the center hole (0 for pie, >0 for donut)

    Returns:
        Plotly Figure object
    """
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=hole,
        marker=dict(colors=colors) if colors else None,
        textinfo='label+percent',
        textposition='outside'
    )])

    fig.update_layout(
        title=dict(text=title, x=0.5),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        height=400,
        margin=dict(l=20, r=20, t=60, b=80)
    )

    return fig


def bar_chart(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str = "",
    color: str = None,
    orientation: str = "v",
    color_continuous_scale: str = "Viridis"
) -> go.Figure:
    """
    Create a bar chart.

    Args:
        data: DataFrame with data
        x_col: Column for x-axis (or y for horizontal)
        y_col: Column for y-axis (or x for horizontal)
        title: Chart title
        color: Column for color encoding or fixed color
        orientation: 'v' for vertical, 'h' for horizontal

    Returns:
        Plotly Figure object
    """
    if orientation == "h":
        fig = px.bar(
            data,
            x=y_col,
            y=x_col,
            color=color if color and color in data.columns else None,
            orientation="h",
            title=title,
            color_continuous_scale=color_continuous_scale
        )
    else:
        fig = px.bar(
            data,
            x=x_col,
            y=y_col,
            color=color if color and color in data.columns else None,
            title=title,
            color_continuous_scale=color_continuous_scale
        )

    fig.update_layout(
        title=dict(text=title, x=0.5),
        height=400
    )

    return fig


def scatter_chart(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: str = None,
    size_col: str = None,
    hover_name: str = None,
    title: str = "",
    log_x: bool = False,
    log_y: bool = False
) -> go.Figure:
    """
    Create a scatter plot.

    Args:
        data: DataFrame with data
        x_col: Column for x-axis
        y_col: Column for y-axis
        color_col: Column for color encoding
        size_col: Column for size encoding
        hover_name: Column for hover labels
        title: Chart title
        log_x: Use log scale for x-axis
        log_y: Use log scale for y-axis

    Returns:
        Plotly Figure object
    """
    fig = px.scatter(
        data,
        x=x_col,
        y=y_col,
        color=color_col,
        size=size_col,
        hover_name=hover_name,
        title=title,
        log_x=log_x,
        log_y=log_y
    )

    fig.update_layout(
        title=dict(text=title, x=0.5),
        height=500
    )

    return fig
