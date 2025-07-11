import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- Helper function to prepare plot data for a given year ---
def prepare_plot_data(df, year):
    all_regions = df['region'].unique()
    df_year = df[df['year'] == year]
    df_plot = pd.DataFrame({'region': all_regions})
    df_plot = df_plot.merge(df_year[['region', 'value', 'color']], on='region', how='left')
    df_plot['color'] = df_plot['color'].fillna('#ffffff')
    df_plot['value'] = df_plot['value'].fillna('')
    return df_plot

# --- Production-ready function for 2D choropleth map (country or state level) ---
def plot_choropleth_map_2d(
    df,
    output_file,
    region_type='auto',  # 'auto', 'country', or 'state'
    country_name=None    # Required if region_type is 'state'
):
    """
    Plots a 2D choropleth map (country or state level) with animation over years, using provided region names and color codes.
    Args:
        df: pandas DataFrame with columns: 'year', 'region', 'value', 'color'.
        output_file: HTML file to save the plot (for frontend integration)
        region_type: 'auto', 'country', or 'state'. If 'auto', infers from data.
        country_name: (optional) required if plotting state-level map (e.g., 'India', 'United States')
    Notes:
        - Uses Mercator projection.
        - No color scale/legend (color is provided).
        - Hover tooltip shows region name and value.
        - Animation over years (user can scrub/select year).
        - Missing regions are colored white.
        - Styling matches other plots (background, font, etc.).
        - Title is left blank.
    """
    # Infer region type if needed
    if region_type == 'auto':
        if country_name is not None:
            region_type = 'state'
        else:
            region_type = 'country'

    years = sorted(df['year'].unique())
    has_animation = len(years) > 1

    if region_type == 'country':
        locationmode = 'country names'
        scope = 'world'
    elif region_type == 'state':
        if country_name and country_name.lower() in ['united states', 'usa', 'us', 'america']:
            locationmode = 'USA-states'
            scope = 'usa'
        else:
            locationmode = None
            scope = country_name
    else:
        raise ValueError("region_type must be 'country' or 'state'")

    # Prepare frames for animation
    frames = []
    for year in years:
        df_plot = prepare_plot_data(df, year)
        if region_type == 'country':
            frame = go.Choropleth(
                locations=df_plot['region'],
                z=[0]*len(df_plot),
                text=[f"{r}<br>Value: {v}" if v != '' else f"{r}<br>No data" for r, v in zip(df_plot['region'], df_plot['value'])],
                hoverinfo='text',
                locationmode=locationmode,
                marker=dict(line=dict(color='black', width=0.5)),
                showscale=False,
                autocolorscale=False,
                zmin=0,
                zmax=0,
                colorscale=[[0, '#ffffff'], [1, '#ffffff']],
                customdata=df_plot['color'],
            )
        elif region_type == 'state':
            frame = go.Choropleth(
                locations=df_plot['region'],
                z=[0]*len(df_plot),
                text=[f"{r}<br>Value: {v}" if v != '' else f"{r}<br>No data" for r, v in zip(df_plot['region'], df_plot['value'])],
                hoverinfo='text',
                locationmode=locationmode,
                marker=dict(line=dict(color='black', width=0.5)),
                showscale=False,
                autocolorscale=False,
                zmin=0,
                zmax=0,
                colorscale=[[0, '#ffffff'], [1, '#ffffff']],
                customdata=df_plot['color'],
            )
        frames.append(frame)

    # Initial data (first year)
    df_plot = prepare_plot_data(df, years[0])
    if region_type == 'country':
        choropleth = go.Choropleth(
            locations=df_plot['region'],
            z=[0]*len(df_plot),
            text=[f"{r}<br>Value: {v}" if v != '' else f"{r}<br>No data" for r, v in zip(df_plot['region'], df_plot['value'])],
            hoverinfo='text',
            locationmode=locationmode,
            marker=dict(line=dict(color='black', width=0.5)),
            showscale=False,
            autocolorscale=False,
            zmin=0,
            zmax=0,
            colorscale=[[0, '#ffffff'], [1, '#ffffff']],
            customdata=df_plot['color'],
        )
    elif region_type == 'state':
        choropleth = go.Choropleth(
            locations=df_plot['region'],
            z=[0]*len(df_plot),
            text=[f"{r}<br>Value: {v}" if v != '' else f"{r}<br>No data" for r, v in zip(df_plot['region'], df_plot['value'])],
            hoverinfo='text',
            locationmode=locationmode,
            marker=dict(line=dict(color='black', width=0.5)),
            showscale=False,
            autocolorscale=False,
            zmin=0,
            zmax=0,
            colorscale=[[0, '#ffffff'], [1, '#ffffff']],
            customdata=df_plot['color'],
        )

    fig = go.Figure(data=[choropleth])
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
            projection=dict(type='mercator'),
            showland=True,
            landcolor='rgba(180,210,230,0.7)',
            showcountries=True,
            countrycolor='black',
            showframe=False,
            showcoastlines=True,
            coastlinecolor='black',
            scope=scope,
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
    print(f"Choropleth map (2D) saved as {output_file}") 