from dash import dcc, html
from .data import get_countries, get_metrics

def create_layout():
    countries = get_countries()
    metrics = get_metrics()

    return html.Div([
        html.H1("Global Air Quality Analysis", style={'textAlign': 'center', 'color': 'white'}),
        
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