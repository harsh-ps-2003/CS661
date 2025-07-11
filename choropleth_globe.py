import pandas as pd
import plotly.graph_objects as go

# --- Helper function to prepare plot data for a given year (3D globe) ---
def prepare_globe_plot_data(df, year):
    df_year = df[df['year'] == year].copy()
    # Fill missing color with white
    df_year['color'] = df_year['color'].fillna('#ffffff')
    df_year['value'] = df_year['value'].fillna('')
    return df_year

# --- Production-ready function for 3D globe choropleth map ---
def plot_choropleth_globe(
    df,
    output_file
):
    """
    Plots a 3D globe choropleth map with animation over years, using provided region names, color codes, and lat/lon.
    Args:
        df: pandas DataFrame with columns: 'year', 'region', 'value', 'color', 'lat', 'lon'.
        output_file: HTML file to save the plot (for frontend integration)
    Notes:
        - Plots colored points on a 3D globe (not height/extrusion).
        - Animation over years (user can scrub/select year).
        - Missing data is colored white.
        - Hover tooltip shows region name, value, and year.
        - Users can rotate/zoom the globe.
        - Styling matches other plots (background, font, etc.).
        - No title or legend.
    """
    # Input check for required columns
    required_columns = {'year', 'region', 'value', 'color', 'lat', 'lon'}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in DataFrame: {missing}")

    years = sorted(df['year'].unique())
    has_animation = len(years) > 1

    # Prepare frames for animation
    frames = []
    for year in years:
        df_plot = prepare_globe_plot_data(df, year)
        frame = go.Scattergeo(
            lon=df_plot['lon'],
            lat=df_plot['lat'],
            mode='markers',
            marker=dict(
                size=18,
                color=df_plot['color'],
                line=dict(width=1, color='black'),
                opacity=0.85
            ),
            text=[f"<b>{r}</b><br><b>Value:</b> {v}<br><b>Year:</b> {year}" if v != '' else f"<b>{r}</b><br>No data<br><b>Year:</b> {year}" for r, v in zip(df_plot['region'], df_plot['value'])],
            hoverinfo='text',
            showlegend=False
        )
        frames.append(frame)

    # Initial data (first year)
    df_plot = prepare_globe_plot_data(df, years[0])
    scatter = go.Scattergeo(
        lon=df_plot['lon'],
        lat=df_plot['lat'],
        mode='markers',
        marker=dict(
            size=18,
            color=df_plot['color'],
            line=dict(width=1, color='black'),
            opacity=0.85
        ),
        text=[f"<b>{r}</b><br><b>Value:</b> {v}<br><b>Year:</b> {years[0]}" if v != '' else f"<b>{r}</b><br>No data<br><b>Year:</b> {years[0]}" for r, v in zip(df_plot['region'], df_plot['value'])],
        hoverinfo='text',
        showlegend=False
    )

    fig = go.Figure(data=[scatter])
    if has_animation:
        fig.frames = [go.Frame(data=[f], name=str(y)) for f, y in zip(frames, years)]
        fig.update_layout(
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [
                    {
                        'label': 'Play',
                        'method': 'animate',
                        'args': [None, {'frame': {'duration': 1000, 'redraw': True}, 'fromcurrent': True, 'mode': 'immediate'}]
                    }
                ],
                'x': 0.1,
                'y': -0.1,
                'xanchor': 'left',
                'yanchor': 'top'
            }],
            sliders=[{
                'steps': [
                    {
                        'method': 'animate',
                        'label': str(y),
                        'args': [[str(y)], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate'}]
                    } for y in years
                ],
                'transition': {'duration': 0},
                'x': 0.1,
                'y': -0.08,
                'currentvalue': {'prefix': 'Year: '},
                'len': 0.8
            }]
        )
    fig.update_layout(
        geo=dict(
            projection_type='orthographic',
            showland=True,
            landcolor='rgba(180,210,230,0.7)',
            showcountries=True,
            countrycolor='black',
            showframe=False,
            showcoastlines=True,
            coastlinecolor='black',
            lataxis=dict(showgrid=True, gridwidth=0.5, gridcolor='rgba(255,255,255,0.3)'),
            lonaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='rgba(255,255,255,0.3)'),
        ),
        plot_bgcolor='rgba(180,210,230,0.7)',
        paper_bgcolor='rgba(180,210,230,0.7)',
        font=dict(family='Arial', size=16, color='#222'),
        margin=dict(l=40, r=40, t=60, b=40),
        title='',
        autosize=True,
        hovermode='closest',
        showlegend=False
    )
    fig.write_html(output_file)
    print(f"Choropleth globe (3D) saved as {output_file}")
