from dash import callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .data import load_clean_data, latest_year, top_emitters


def _scatter(df, gas):
    fig = px.scatter(
        df[df['Gas'] == gas],
        x='Year', y='Value',
        color='Country',
        title=f'{gas} Emissions Over Time (All Countries)',
        labels={'Value': 'Emissions (kt CO₂e)', 'Year': 'Year'}
    )
    fig.update_layout(showlegend=False, width=1000, height=500)
    return fig


def _timeseries(df, gas):
    yr = latest_year()
    top = top_emitters(gas, yr, n=5)['Country']
    subset = df[(df['Gas'] == gas) & (df['Country'].isin(top))]
    fig = px.line(
        subset, x='Year', y='Value', color='Country', markers=True,
        title=f'Top 5 Emitters – {gas} Trend',
        labels={'Value': 'Emissions (kt CO₂e)', 'Year': 'Year'}
    )
    fig.update_layout(width=1000, height=500)
    return fig


def _barchart(df, gas):
    yr = latest_year()
    top_df = top_emitters(gas, yr)
    fig = px.bar(
        top_df[::-1],  # reverse for horizontal bar
        x='Value', y='Country', orientation='h',
        title=f'Top 10 {gas} Emitters in {yr}',
        labels={'Value': 'Emissions (kt CO₂e)', 'Country': ''}
    )
    fig.update_layout(width=1000, height=500)
    return fig


def _choropleth(df, gas):
    yr = latest_year()
    subset = df[(df['Gas'] == gas) & (df['Year'] == yr)]
    fig = px.choropleth(
        subset, locations='Country', locationmode='country names',
        color='Value',
        title=f'{gas} Emissions – {yr}',
        color_continuous_scale='YlOrRd',
        labels={'Value': 'Emissions (kt CO₂e)'}
    )
    fig.update_layout(width=1000, height=500, margin=dict(l=0, r=0, t=40, b=0))
    return fig


df_cached = load_clean_data()


@callback(
    Output('ghg-scatter', 'figure'),
    Output('ghg-timeseries', 'figure'),
    Output('ghg-barchart', 'figure'),
    Output('ghg-map', 'figure'),
    Input('ghg-gas-dropdown', 'value')
)
def update_ghg_graphs(gas):
    scatter = _scatter(df_cached, gas)
    line = _timeseries(df_cached, gas)
    bar = _barchart(df_cached, gas)
    cmap = _choropleth(df_cached, gas)
    return scatter, line, bar, cmap 