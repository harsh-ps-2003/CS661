from dash import html, dcc
from .data import available_gases


def create_layout():
    gases = available_gases()
    return html.Div([
        html.H1('Global Greenhouse Gas Emissions', style={'textAlign': 'center', 'color': 'white'}),
        html.Div([
            html.Label('Select Gas:', style={'color': 'white', 'marginRight': '10px'}),
            dcc.Dropdown(
                id='ghg-gas-dropdown',
                options=[{'label': g, 'value': g} for g in gases],
                value=gases[0],
                clearable=False,
                style={'width': '300px'}
            )
        ], style={'textAlign': 'center', 'marginBottom': '20px'}),

        # Graphs
        html.Div([
            dcc.Graph(id='ghg-scatter', style={'border': '3px solid #2A547E', 'marginBottom': '20px'}),
            dcc.Graph(id='ghg-timeseries', style={'border': '3px solid #2A547E', 'marginBottom': '20px'}),
            dcc.Graph(id='ghg-barchart', style={'border': '3px solid #2A547E', 'marginBottom': '20px'}),
            dcc.Graph(id='ghg-map', style={'border': '3px solid #2A547E', 'marginBottom': '20px'}),
        ], style={'margin': 'auto', 'width': '95%'}),
    ], style={'backgroundColor': '#4482C1', 'padding': '30px', 'minHeight': '100vh'}) 