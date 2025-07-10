import pandas as pd
import plotly.graph_objects as go

# --- Production-ready function for metric vs. time line plot ---
def plot_metrics_vs_time(df, output_file, colors=None):
    """
    Plots all metrics present in the DataFrame (except the first column, which is the time axis) vs. time and saves as an HTML file.
    Args:
        df: pandas DataFrame with the data. The first column is used as the time axis (x), all others are metrics (y).
        output_file: HTML file to save the plot (for frontend integration)
        colors: list of color hex codes (optional, default palette for up to 6 metrics)
    Usage:
        # The integrator should provide a DataFrame like:
        #   | Time | Metric1 | Metric2 | ... |
        # plot_metrics_vs_time(df, 'output.html')
    """
    # The first column is the time axis
    time_col = df.columns[0]
    # All other columns are metrics
    metric_cols = list(df.columns[1:])
    if not metric_cols:
        raise ValueError("No metric columns found in the DataFrame.")
    fig = go.Figure()
    if colors is None:
        # Default color palette (yellow, gray, white, blue, green, red)
        colors = ['#ffe066', '#bfc1c2', '#ffffff', '#2196F3', '#43A047', '#E53935']
    # Add a line for each metric
    for i, metric in enumerate(metric_cols):
        color = colors[i % len(colors)]
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        fig.add_trace(go.Scatter(
            x=df[time_col],
            y=df[metric],
            mode='lines',
            name=metric,
            line=dict(color=color, width=6, shape='spline'),
            fill='tozeroy',
            fillcolor=f'rgba({r},{g},{b},0.35)',
            opacity=1.0
        ))
    # Style the layout
    fig.update_layout(
        plot_bgcolor='rgba(180,210,230,0.7)',
        paper_bgcolor='rgba(180,210,230,0.7)',
        font=dict(family='Arial', size=16, color='#222'),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.08,
            xanchor='center',
            x=0.5,
            font=dict(size=18)
        ),
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis=dict(showgrid=False, zeroline=False, showline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.3)', zeroline=False, showline=False),
        title='',
        autosize=True,
    )
    # Save the plot as HTML
    fig.write_html(output_file)
    print(f"Line plot saved as {output_file}") 