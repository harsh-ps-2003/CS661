from dash import dcc, html
import plotly.express as px
import pandas as pd
import numpy as np

from .data import get_countries, get_metrics, load_air_quality_data

# ------------------------------------------------------------------
# Build choropleth of composite air quality (considering all pollutants)
# ------------------------------------------------------------------

aq_df = load_air_quality_data()
# Guard against empty
if not aq_df.empty:
    # Get all pollutants
    pollutants = ['pm25', 'pm10', 'so2', 'no2', 'co', 'o3']
    
    # Calculate mean for each pollutant by country
    country_means = {}
    for pollutant in pollutants:
        means = aq_df.groupby('country')[pollutant].mean()
        # Normalize each pollutant (0-1 scale)
        if not means.empty:
            min_val = means.min()
            max_val = means.max()
            if max_val > min_val:  # Avoid division by zero
                means = (means - min_val) / (max_val - min_val)
            country_means[pollutant] = means
    
    # Create composite score (average of normalized pollutants)
    composite_scores = pd.DataFrame()
    for pollutant in pollutants:
        if pollutant in country_means:
            if composite_scores.empty:
                composite_scores = country_means[pollutant].to_frame('score')
            else:
                composite_scores['score'] += country_means[pollutant]
    
    if not composite_scores.empty:
        composite_scores['score'] /= len(pollutants)
        composite_scores = composite_scores.reset_index()
        
        fig_aq_map = px.choropleth(
            composite_scores,
            locations='country',
            locationmode='country names',
            color='score',
            color_continuous_scale='Blues',  # Now darker = worse air quality
            range_color=(0, 1),
            labels={'score': 'Air Quality Score<br>(Higher = Worse)'},
            title='Composite Air Quality by Country<br>(Considering PM2.5, PM10, SO2, NO2, CO, O3)'
        )
        fig_aq_map.update_layout(
            geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
            margin=dict(l=0, r=0, t=50, b=0)
        )
else:
    fig_aq_map = px.choropleth(title='Air quality data not available')


def create_layout():
    countries = get_countries()
    metrics = get_metrics()

    return html.Div([
        html.H1("Global Air Quality Analysis", style={'textAlign': 'center', 'color': 'white'}),

        # Choropleth Map section
        html.Div([
            dcc.Graph(id='aq-global-map', figure=fig_aq_map, style={'height': '600px'})
        ], style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '15px', 'margin': '20px'}),

        # Controls
        html.Div([
            dcc.Dropdown(
                id='aq-country-dropdown',
                options=[{'label': c, 'value': c} for c in countries],
                value=countries[0] if countries else None,
                placeholder="Select a country",
                style={'width': '200px', 'marginRight': '10px'}
            ),
            dcc.Dropdown(
                id='aq-city-dropdown',
                placeholder="Select a city",
                style={'width': '200px', 'marginRight': '10px'}
            ),
            dcc.Dropdown(
                id='aq-metric-dropdown',
                options=[{'label': m.replace('_', ' ').title(), 'value': m} for m in metrics],
                value=metrics[0],
                clearable=False,
                style={'width': '200px', 'marginRight': '10px'}
            ),
        ], style={'display': 'flex', 'justifyContent': 'center', 'padding': '20px'}),

        # Visualizations
        html.Div([
            dcc.Graph(id='aq-timeseries-plot'),
            dcc.Graph(id='aq-boxplot'),
        ], style={'padding': '20px'})

    ], style={'backgroundColor': '#363636', 'padding': '30px', 'minHeight': '100vh'}) 