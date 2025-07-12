from dash import html, dcc
from .data import available_gases, get_all_countries


def create_layout():
    gases = available_gases()
    countries = get_all_countries()
    return html.Div([
        html.H1('Global Greenhouse Gas Emissions', style={'textAlign': 'center', 'color': 'white'}),
        html.Div([
            html.Div([
                html.Label('Select Gas:', style={'color': 'white', 'marginRight': '10px'}),
                dcc.Dropdown(
                    id='ghg-gas-dropdown',
                    options=[{'label': g, 'value': g} for g in gases],
                    value=gases[0],
                    clearable=False,
                    style={'width': '300px'}
                )
            ], style={'marginBottom': '20px'}),
            html.Div([
                html.Label("Select countries to display for scatter plot:", style={'color': 'white'}),
                dcc.Dropdown(
                    id="ghg-country-dropdown",
                    options=[{"label": country, "value": country} for country in countries],
                    value=countries[:2] if countries else [],
                    multi=True,
                    style={'width': '700px'}
                )
            ], style={'marginBottom': '20px'}),
        ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'}),

        # Graphs
        html.Div([
            dcc.Graph(id="ghg-scatterplot", style={"margin-bottom": "10px", 'border': '3px solid #2A547E'}),
            html.H1(id='racing-bar-title', children='Top 10 Emitting Countries - Growth', style={'font-size': '20px', 'color': 'white', 'padding-left': '10px'}),
            dcc.Graph(id='ghg-racing-bar', style={"margin-bottom": "10px", 'border': '3px solid #2A547E'}),
            dcc.Interval(id='ghg-interval-component', interval=600, n_intervals=0),
            html.Div(
                children=[
                    dcc.Graph(id='ghg-top-5-bar', style={"margin-bottom": "10px", 'border': '3px solid #2A547E'}),
                    dcc.Graph(id='ghg-bottom-5-bar', style={"margin-bottom": "10px", 'border': '3px solid #2A547E'}),
                ],
                style={"display": "flex", "flex-direction": "row", "justify-content": "space-between", "width": "100%"}
            ),
            dcc.Graph(id="ghg-bubble-map", style={"margin-bottom": "10px", 'border': '3px solid #2A547E'}),
            dcc.Graph(id='ghg-top-5-line', style={"margin-bottom": "10px", 'border': '3px solid #2A547E'}),
            dcc.Graph(id='ghg-bottom-5-line', style={"margin-bottom": "10px", 'border': '3px solid #2A547E'}),
            dcc.Graph(id='ghg-choropleth-map', style={"margin-bottom": "10px", 'border': '3px solid #2A547E', 'width': '100%', 'height': '850px'}),
        ], style={'margin': 'auto', 'width': '95%'}),
    ], style={'backgroundColor': '#4482C1', 'padding': '30px', 'minHeight': '100vh'}) 