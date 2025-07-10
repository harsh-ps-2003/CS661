import pandas as pd
import plotly.graph_objects as go
import calendar

# --- Production-ready function for calendar heatmap ---
def plot_calendar_heatmap(
    df,
    output_file,
    date_col='date',
    value_col='value',
    color_col='color',
    region=None,
    metric=None,
    unit=None
):
    """
    Plots a calendar heatmap: years as rows, months as columns, each cell is a day colored by the 'color' column.
    Args:
        df: pandas DataFrame with columns: 'date' (datetime), 'value', 'region', 'metric', 'unit', 'color' (hex/rgba)
        output_file: HTML file to save the plot (for frontend integration)
        date_col: column name for date (default 'date')
        value_col: column name for value (default 'value')
        color_col: column name for cell color (default 'color')
        region, metric, unit: (optional) for hover info
    Notes:
        - Each cell is colored using the 'color' column; blank if missing.
        - Tooltip shows date, value, region, and metric.
        - No color scale/legend. Black borders for months/years.
        - No filtering or transformation is done in this function.
    """
    # Ensure date column is datetime
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df['year'] = df[date_col].dt.year
    df['month'] = df[date_col].dt.month
    df['day'] = df[date_col].dt.day
    years = sorted(df['year'].unique())
    months = list(range(1, 13))

    # Build grid: for each year, for each month, for each day, get color/value
    cell_x = []  # month index (0-11)
    cell_y = []  # year index (0 = top row)
    cell_day = []
    cell_color = []
    cell_value = []
    cell_date = []
    cell_hover = []
    for y_idx, year in enumerate(years):
        for m_idx, month in enumerate(months):
            ndays = calendar.monthrange(year, month)[1]
            for day in range(1, ndays + 1):
                this_date = pd.Timestamp(year=year, month=month, day=day)
                row = df[(df['year'] == year) & (df['month'] == month) & (df['day'] == day)]
                if not row.empty and pd.notnull(row.iloc[0][color_col]):
                    color = row.iloc[0][color_col]
                    value = row.iloc[0][value_col]
                    hover = f"{this_date.strftime('%Y-%m-%d')}<br>Value: {value}"
                    if region:
                        hover += f"<br>Region: {region}"
                    if metric:
                        hover += f"<br>Metric: {metric}"
                    cell_color.append(color)
                    cell_value.append(value)
                else:
                    color = 'rgba(255,255,255,0)'  # blank/white
                    value = None
                    hover = f"{this_date.strftime('%Y-%m-%d')}<br>No data"
                    if region:
                        hover += f"<br>Region: {region}"
                    if metric:
                        hover += f"<br>Metric: {metric}"
                    cell_color.append(color)
                    cell_value.append(value)
                cell_x.append(m_idx)
                cell_y.append(y_idx)
                cell_day.append(day)
                cell_date.append(this_date)
                cell_hover.append(hover)

    # Plotly scatter for each cell (as a square marker)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=cell_x,
        y=cell_y,
        mode='markers',
        marker=dict(
            symbol='square',
            size=24,
            color=cell_color,
            line=dict(width=1, color='black'),
        ),
        text=cell_hover,
        hoverinfo='text',
        showlegend=False
    ))
    # Set axis labels and ticks
    fig.update_xaxes(
        tickvals=list(range(12)),
        ticktext=[calendar.month_abbr[m] for m in months],
        showgrid=False,
        zeroline=False,
        showline=False,
        tickangle=0
    )
    fig.update_yaxes(
        tickvals=list(range(len(years))),
        ticktext=[str(y) for y in years],
        showgrid=False,
        zeroline=False,
        showline=False,
        autorange='reversed'  # years top to bottom
    )
    # Style the layout
    fig.update_layout(
        plot_bgcolor='rgba(180,210,230,0.7)',
        paper_bgcolor='rgba(180,210,230,0.7)',
        font=dict(family='Arial', size=16, color='#222'),
        margin=dict(l=40, r=40, t=60, b=40),
        title='',
        autosize=True,
        xaxis_title='',
        yaxis_title='',
        hovermode='closest',
    )
    # Save the plot as HTML
    fig.write_html(output_file)
    print(f"Calendar heatmap saved as {output_file}") 