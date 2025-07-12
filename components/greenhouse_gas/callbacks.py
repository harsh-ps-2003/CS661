from dash import callback, Input, Output, State, no_update
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .data import load_clean_data, get_top_bottom_countries
from functools import lru_cache

df_cached = load_clean_data()

# Callback for the scatter plot
@callback(
    Output('ghg-scatterplot', 'figure'),
    [Input('ghg-country-dropdown', 'value'),
     Input('ghg-gas-dropdown', 'value')]
)
def update_scatterplot(countries, gas):
    if not countries or not gas:
        return go.Figure()

    filtered_df = df_cached[(df_cached['Country'].isin(countries)) & (df_cached['Gas'] == gas)]
    
    fig = px.scatter(
        filtered_df,
        x="Year",
        y="Value",
        color="Country",
        title=f"Scatter Plot - Average {gas} Emissions by Country",
        labels={'Value': f'Emissions (kt CO₂e)', 'Year': 'Year'},
        hover_data=["Country"]
    )
    fig.update_layout(
        font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    return fig

# Callback for bar and line charts
@callback(
    Output('ghg-top-5-bar', 'figure'),
    Output('ghg-bottom-5-bar', 'figure'),
    Output('ghg-top-5-line', 'figure'),
    Output('ghg-bottom-5-line', 'figure'),
    Input('ghg-gas-dropdown', 'value')
)
def update_bar_line_charts(gas):
    if not gas:
        return go.Figure(), go.Figure(), go.Figure(), go.Figure()

    gas_df = df_cached[df_cached['Gas'] == gas]
    top_countries, bottom_countries = get_top_bottom_countries(gas, n=5)

    # Top 5 charts
    top5_df = gas_df[gas_df['Country'].isin(top_countries)]
    fig_top_5_bar = px.bar(top5_df, x='Country', y='Value', color='Year', barmode='group',
                           labels={'Country': 'Country', 'Value': f'{gas} Emissions (kt CO₂e)', 'Year': 'Year'},
                           title=f'Bar Chart - Top 5 Countries in {gas} Emissions')
    fig_top_5_line = px.line(top5_df, x="Year", y="Value", color="Country",
                             title=f"Line Chart - Top 5 Countries in {gas} Emissions")

    # Bottom 5 charts
    bottom5_df = gas_df[gas_df['Country'].isin(bottom_countries)]
    fig_bottom_5_bar = px.bar(bottom5_df, x='Country', y='Value', color='Year', barmode='group',
                              labels={'Country': 'Country', 'Value': f'{gas} Emissions (kt CO₂e)', 'Year': 'Year'},
                              title=f'Bar Chart - Bottom 5 Countries in {gas} Emissions')
    fig_bottom_5_line = px.line(bottom5_df, x="Year", y="Value", color="Country",
                                title=f"Line Chart - Bottom 5 Countries in {gas} Emissions")
    
    for fig in [fig_top_5_bar, fig_top_5_line, fig_bottom_5_bar, fig_bottom_5_line]:
        fig.update_layout(height=400, yaxis_title=f"{gas} Emissions (kt CO₂e)", font=dict(family="Courier New, monospace", size=12, color="#7f7f7f"))

    return fig_top_5_bar, fig_bottom_5_bar, fig_top_5_line, fig_bottom_5_line


# Callback for animated choropleth map
@callback(
    Output('ghg-choropleth-map', 'figure'),
    Input('ghg-gas-dropdown', 'value')
)
def update_choropleth_map(gas):
    if not gas:
        return go.Figure()

    gas_df = df_cached[df_cached['Gas'] == gas].sort_values(by="Year", ascending=True)
    if gas_df.empty:
        return go.Figure(layout={'title': f'No data for {gas}'})
        
    min_val, max_val = gas_df['Value'].quantile([0.05, 0.95])
    
    fig = px.choropleth(
        gas_df,
        locations="Country",
        locationmode="country names",
        color="Value",
        animation_frame="Year",
        range_color=[min_val, max_val if max_val > min_val else min_val+1],
        title=f"Choropleth Map - Average {gas} Emissions by Country"
    )
    return fig

# Callback for bubble map
@callback(
    Output('ghg-bubble-map', 'figure'),
    Input('ghg-gas-dropdown', 'value')
)
def update_bubble_map(gas):
    if not gas:
        return go.Figure()

    gas_df = df_cached[df_cached['Gas'] == gas]
    if gas_df.empty:
        return go.Figure(layout={'title': f'No data for {gas}'})
        
    # This mapping is incomplete and a better source for country->continent should be used in the future
    country_to_region = {'United States': 'North America', 'China': 'Asia', 'European Union (27)': 'Europe', 'India': 'Asia', 'Russian Federation': 'Europe', 'Japan': 'Asia', 'Germany': 'Europe', 'Korea, Republic of': 'Asia', 'Iran (Islamic Republic of)': 'Middle East', 'Canada': 'North America', 'Saudi Arabia': 'Middle East', 'Brazil': 'South America', 'Indonesia': 'Asia', 'United Kingdom': 'Europe', 'Australia': 'Oceania', 'France': 'Europe', 'Italy': 'Europe', 'Spain': 'Europe', 'Turkey': 'Middle East', 'Ukraine': 'Europe', 'Poland': 'Europe', 'Netherlands': 'Europe', 'Belgium': 'Europe'}
    gas_df['Region'] = gas_df['Country'].map(country_to_region).fillna('Other')
    
    fig = px.scatter(
        gas_df,
        x='Value',
        y='Year',
        size='Value',
        color='Region',
        log_x=True,
        hover_name='Country',
        animation_frame='Year',
        title=f'{gas} Emissions by Country and Year'
    )
    fig.update_layout(xaxis_title=f'Total {gas} Emissions (kt CO₂e)', yaxis_title='Year', legend_title='Region', font=dict(size=12))
    return fig


@lru_cache(maxsize=8) # cache for each gas
def get_racing_bar_figure(gas):
    gas_df = df_cached[df_cached['Gas'] == gas]
    years = sorted(gas_df['Year'].unique())
    if not years:
        return None
        
    df_total = gas_df.groupby(['Country', 'Year'])['Value'].sum().reset_index()
    max_val = df_total['Value'].max() * 1.1

    initial_year = years[0]
    initial_data = df_total[df_total.Year == initial_year].nlargest(10, 'Value').sort_values('Value')
    
    fig = go.Figure(
        data=[go.Bar(
            x=initial_data['Value'], y=initial_data['Country'], orientation='h',
            text=initial_data['Value'].apply(lambda x: f' {x:,.0f}'),
            textposition='auto', insidetextanchor='end',
        )],
        layout=go.Layout(
            xaxis=dict(range=[0, max_val]),
            title_text=f'Top 10 {gas} Emitters - {initial_year}',
            yaxis={'categoryorder': 'total ascending'}
        )
    )

    frames = []
    for year in years:
        df_year = df_total[df_total['Year'] == year].nlargest(10, 'Value').sort_values('Value')
        frame = go.Frame(
            data=[go.Bar(
                x=df_year['Value'], y=df_year['Country'], orientation='h',
                text=df_year['Value'].apply(lambda x: f' {x:,.0f}'),
                textposition='auto', insidetextanchor='end',
            )],
            name=str(year),
            layout=go.Layout(title_text=f'Top 10 {gas} Emitters - {year}')
        )
        frames.append(frame)
    
    fig.frames = frames

    fig.update_layout(
        updatemenus=[dict(
            type="buttons",
            direction="down",
            buttons=[
                dict(label="Play",
                     method="animate",
                     args=[None, {"frame": {"duration": 500, "redraw": True},
                                  "fromcurrent": True, "transition": {"duration": 300, "easing": "linear"}}]),
                dict(label="Pause",
                     method="animate",
                     args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate",
                                    "transition": {"duration": 0}}])
            ],
        )],
        xaxis_title=f"{gas} Emissions (kt CO₂e)",
        yaxis_title=""
    )
    fig.update_yaxes(automargin=True)
    
    return fig

# Callback for racing bar chart
@callback(
    Output('ghg-racing-bar', 'figure'),
    Output('racing-bar-title', 'children'),
    Input('ghg-gas-dropdown', 'value')
)
def update_racing_bar_chart(gas):
    if not gas:
        return go.Figure(), "Top 10 Emitting Countries - Growth"

    fig = get_racing_bar_figure(gas)
    if fig is None:
        return go.Figure(layout={'title': f'No data for {gas}'}), f"Top 10 {gas} Emitting Countries - Growth"

    return fig, no_update 