"""Plotly chart helpers for the song popularity analysis."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def target_distribution(df: pd.DataFrame, target_column: str) -> go.Figure:
    """Create a histogram for the selected popularity target."""

    fig = px.histogram(df, x=target_column, nbins=50, title="Popularity Target Distribution")
    fig.update_layout(xaxis_title=target_column, yaxis_title="Track count")
    return fig


def segment_comparison(comparison: pd.DataFrame, title: str) -> go.Figure:
    """Create a bar chart of top segment differences by driver."""

    plot_df = comparison.copy()
    if "difference" not in plot_df.columns:
        plot_df["difference"] = 0
    fig = px.bar(
        plot_df,
        x="driver",
        y="difference",
        color="driver_type" if "driver_type" in plot_df.columns else None,
        title=title,
    )
    fig.update_layout(xaxis_title="Driver", yaxis_title="Top 10% minus remaining")
    return fig


def ranked_drivers(ranked: pd.DataFrame) -> go.Figure:
    """Create a ranked driver bar chart."""

    fig = px.bar(
        ranked.sort_values("rank", ascending=False),
        x="abs_difference",
        y="driver",
        color="driver_type" if "driver_type" in ranked.columns else None,
        orientation="h",
        title="Ranked Popularity Drivers",
    )
    fig.update_layout(xaxis_title="Absolute difference", yaxis_title="Driver")
    return fig


def tag_lift_chart(
    summary: pd.DataFrame,
    label_column: str,
    title: str,
    top_n: int = 15,
) -> go.Figure:
    """Create a horizontal bar chart for overrepresented tags."""

    plot_df = summary.sort_values("pct_point_diff", ascending=False).head(top_n).copy()
    plot_df = plot_df.sort_values("pct_point_diff")
    fig = px.bar(
        plot_df,
        x="pct_point_diff",
        y=label_column,
        orientation="h",
        title=title,
        hover_data=["top_pct", "remaining_pct", "lift"],
    )
    fig.update_layout(
        xaxis_title="Top 10% minus remaining share",
        yaxis_title="Tag",
        xaxis_tickformat=".0%",
    )
    return fig


def tag_share_chart(
    summary: pd.DataFrame,
    label_column: str,
    title: str,
    top_n: int = 10,
) -> go.Figure:
    """Create grouped bars comparing top-decile and remaining tag shares."""

    plot_df = summary.sort_values("pct_point_diff", ascending=False).head(top_n)
    long = plot_df.melt(
        id_vars=[label_column],
        value_vars=["top_pct", "remaining_pct"],
        var_name="segment",
        value_name="share",
    )
    long["segment"] = long["segment"].map(
        {"top_pct": "Top 10%", "remaining_pct": "Remaining"}
    )
    fig = px.bar(
        long,
        x=label_column,
        y="share",
        color="segment",
        barmode="group",
        title=title,
    )
    fig.update_layout(xaxis_title="Tag", yaxis_title="Share of tracks", yaxis_tickformat=".0%")
    return fig


def tag_venn_chart(
    top_tags: pd.DataFrame,
    regions: pd.DataFrame,
    title: str = "Top Tags On Popular Songs",
) -> go.Figure:
    """Create a three-circle Venn-style chart for popular-song tag overlaps."""

    fig = go.Figure()
    if len(top_tags) < 3 or regions.empty:
        fig.update_layout(title=title)
        return fig

    tag_names = top_tags["tag"].astype(str).tolist()
    circle_specs = [
        {"name": tag_names[0], "x": 0.0, "y": 0.35, "color": "rgba(31, 119, 180, 0.32)"},
        {"name": tag_names[1], "x": 1.0, "y": 0.35, "color": "rgba(214, 39, 40, 0.32)"},
        {"name": tag_names[2], "x": 0.5, "y": -0.45, "color": "rgba(44, 160, 44, 0.32)"},
    ]
    radius = 0.78

    for spec in circle_specs:
        fig.add_shape(
            type="circle",
            x0=spec["x"] - radius,
            y0=spec["y"] - radius,
            x1=spec["x"] + radius,
            y1=spec["y"] + radius,
            fillcolor=spec["color"],
            line={"color": spec["color"].replace("0.32", "0.85"), "width": 2},
        )

    count_by_region = dict(zip(regions["region"], regions["count"], strict=False))
    annotations = [
        (-0.38, 0.45, str(count_by_region.get("100", 0))),
        (1.38, 0.45, str(count_by_region.get("010", 0))),
        (0.50, -0.84, str(count_by_region.get("001", 0))),
        (0.50, 0.47, str(count_by_region.get("110", 0))),
        (0.18, -0.20, str(count_by_region.get("101", 0))),
        (0.82, -0.20, str(count_by_region.get("011", 0))),
        (0.50, 0.00, str(count_by_region.get("111", 0))),
        (0.00, 1.23, f"{tag_names[0]} ({int(top_tags.iloc[0]['popular_count']):,})"),
        (1.00, 1.23, f"{tag_names[1]} ({int(top_tags.iloc[1]['popular_count']):,})"),
        (0.50, -1.35, f"{tag_names[2]} ({int(top_tags.iloc[2]['popular_count']):,})"),
    ]
    for x, y, text in annotations:
        fig.add_annotation(x=x, y=y, text=text, showarrow=False, font={"size": 14})

    outside = int(count_by_region.get("000", 0))
    fig.add_annotation(
        x=0.5,
        y=-1.65,
        text=f"Popular songs without these tags: {outside:,}",
        showarrow=False,
        font={"size": 12, "color": "#555"},
    )
    fig.update_xaxes(visible=False, range=[-0.9, 1.9])
    fig.update_yaxes(visible=False, range=[-1.8, 1.45], scaleanchor="x", scaleratio=1)
    fig.update_layout(
        title=title,
        plot_bgcolor="white",
        width=850,
        height=650,
        margin={"l": 20, "r": 20, "t": 70, "b": 20},
    )
    return fig


def save_figure(fig: go.Figure, output_path: Path | str) -> Path:
    """Save a Plotly figure as HTML and return its path."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".html":
        fig.write_html(path)
    else:
        fig.write_image(path)
    return path
