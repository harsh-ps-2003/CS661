from dash import dcc, html
import base64

with open("dataset/earth_image1.png", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

def create_header():
    return html.Div([
        html.Div(
            [
                html.Img(src=f"data:image/jpg;base64,{encoded_image}", style={"height": "300px", "display": "block", "margin": "auto"}),
                html.H1("EARTH'S CLIMATE ANALYTICS", style={"text-align": "center", "font-family": "PT Sans Narrow", 'font-size': '45px'}),
                html.H4("Track changes in Earth's temperature, Carbon Emissions, Sea Levels & Deforestation over time", style={"text-align": "center", "font-family": "PT Sans Narrow", 'font-size': '20px'}),
            ],
            style={"padding-top": "10px", 'padding-bottom': '10px', "background-color": "black", "color": "white", 'box-shadow': '5px 5px 5px grey', "border-radius": "15px"}
        ),
        dcc.Dropdown(
            id="demo-dropdown",
            options=[
                {"label": "Temperature", "value": "temperature"},
                {"label": "Greenhouse Gases", "value": "ghg"},
                {"label": "Sea Levels", "value": "sea"},
                {"label": "Correlation", "value": "correlation"},
                {"label": "Deforestation", "value": "deforestation"}
            ],
            value="",
            placeholder="Select the Desired Visualization",
            style={'width': '450px', "margin-top": "20px", 'margin-bottom': '20px', 'padding-left': '20px', 'font-size': '15px', 'border-color': '#2A547E', 'border-width': '2px'}
        ),
        html.Div(id='dd-output-container'),
    ], style={"background-color": "#CDDEEE", "padding": "10px"})
