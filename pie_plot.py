import pandas as pd
import plotly.graph_objects as go

# --- Production-ready function for pie/donut chart ---
def plot_metric_pie_chart(df, output_file, donut=False, minor_threshold=0.05, colors=None):
    """
    Plots a pie or donut chart for a metric broken down by category, grouping minor categories into 'Other'.
    Args:
        df: pandas DataFrame with two columns: first is category (slice label), second is value.
        output_file: HTML file to save the plot (for frontend integration)
        donut: bool, if True makes a donut chart, else a pie chart
        minor_threshold: float, categories with less than this fraction of total are grouped into 'Other'
        colors: list of color hex codes (optional, default palette for up to 6 categories)
    Usage:
        # The integrator should provide a DataFrame like:
        #   | Category | Value |
        # plot_metric_pie_chart(df, 'output.html', donut=True)
    """
    # The first column is the category, the second is the value
    category_col = df.columns[0]
    value_col = df.columns[1]
    # Group minor categories into 'Other'
    total = df[value_col].sum()
    df['fraction'] = df[value_col] / total
    major = df[df['fraction'] >= minor_threshold].copy()
    minor = df[df['fraction'] < minor_threshold].copy()
    if not minor.empty:
        other_value = minor[value_col].sum()
        other_row = pd.DataFrame({category_col: ['Other'], value_col: [other_value], 'fraction': [other_value / total]})
        major = pd.concat([major, other_row], ignore_index=True)
    plot_df = major
    if colors is None:
        # Default color palette (yellow, gray, white, blue, green, red)
        colors = ['#ffe066', '#bfc1c2', '#ffffff', '#2196F3', '#43A047', '#E53935']
    # Pie or donut chart
    fig = go.Figure(go.Pie(
        labels=plot_df[category_col],
        values=plot_df[value_col],
        marker=dict(colors=colors),
        hole=0.5 if donut else 0,
        sort=False,
        textinfo='label+percent',
        insidetextorientation='radial',
        pull=[0.05 if label == 'Other' else 0 for label in plot_df[category_col]]
    ))
    # Style the layout
    fig.update_layout(
        plot_bgcolor='rgba(180,210,230,0.7)',
        paper_bgcolor='rgba(180,210,230,0.7)',
        font=dict(family='Arial', size=16, color='#222'),
        margin=dict(l=40, r=40, t=60, b=40),
        title='',
        autosize=True,
        showlegend=True
    )
    # Save the plot as HTML
    fig.write_html(output_file)
    print(f"Pie/Donut plot saved as {output_file}") 