import pandas as pd
import plotly.express as px

# --- Production-ready function for scatter plot ---
def plot_scatter(
    df,
    x_col,
    y_col,
    output_file,
    color_col=None,
    size_col=None,
    hover_col=None,
    colors=None
):
    """
    Plots a scatter plot for two variables, with optional color, size, and hover label encoding.
    Args:
        df: pandas DataFrame with the data (already filtered as needed)
        x_col: column name for the X-axis
        y_col: column name for the Y-axis
        output_file: HTML file to save the plot (for frontend integration)
        color_col: (optional) column name for color-coding points
        size_col: (optional) column name for varying point sizes
        hover_col: (optional) column name for hover label
        colors: (optional) list of color hex codes (default palette for up to 6 categories)
    Usage:
        # The integrator should provide a DataFrame like:
        #   | country | co2_emissions | temperature_anomaly | humidity | rainfall |
        # plot_scatter(df, 'co2_emissions', 'temperature_anomaly', 'output.html', color_col='humidity', size_col='rainfall', hover_col='country')
    """
    # Default color palette (same as other charts)
    if colors is None:
        colors = ['#ffe066', '#bfc1c2', '#ffffff', '#2196F3', '#43A047', '#E53935']
    # Build the scatter plot
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        size=size_col,
        hover_name=hover_col,
        color_discrete_sequence=colors if color_col and (df[color_col].dtype == object or df[color_col].dtype.name == 'category') else None,
        opacity=0.85,
        template=None
    )
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
        xaxis=dict(showgrid=True, zeroline=False, showline=False, gridcolor='rgba(255,255,255,0.3)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.3)', zeroline=False, showline=False),
        title='',
        autosize=True,
    )
    # Save the plot as HTML
    fig.write_html(output_file)
    print(f"Scatter plot saved as {output_file}") 