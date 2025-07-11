from dash import Dash, Input, Output, html

from components.header import create_header
from components.temperature.layout import create_temperature_layout
from components.sea_levels.layout import create_sea_levels_layout
from components.correlation.layout import create_correlation_layout
from components.deforestation.layout import create_deforestation_layout
from components.greenhouse_gas import get_layout as create_ghg_layout

from components.temperature.callbacks import register_temperature_callbacks
# greenhouse gas callbacks are registered on import

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server

app.layout = create_header()

@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    if value == 'temperature':
        return create_temperature_layout()
    elif value == 'ghg':
        return create_ghg_layout()
    elif value == 'sea':
        return create_sea_levels_layout()
    elif value == 'correlation':
        return create_correlation_layout()
    elif value == 'deforestation':
        return create_deforestation_layout()
    return html.Div()  # Return empty div if no value matches

register_temperature_callbacks(app)
# greenhouse gas callbacks auto-registered

if __name__ == '__main__':
    app.run(debug=True)





import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
import seaborn as sns

data = pd.read_csv('avg_dataset.csv')
sns.pairplot(data)



import pandas as pd
import plotly.express as px

# Load data from CSV file
data_emissions = pd.read_csv('dataset/avg_dataset.csv')

# Create a stacked bar chart with Plotly
fig_emissions = px.bar(data_emissions, x='Year', y=['Average_Emissions (MtCO₂e)', 'Average_Land_Temperature (celsius)', 'Average_LandOcean_Temperature (celsius)'],
                      title='Greenhouse Gas Emissions vs Temperature')

# Customize the layout
fig_emissions.update_layout(
    font_family='Arial',
    title_font_size=24,
    title_font_color='#404040',
    xaxis=dict(
        title='Year',
        title_font_size=18,
        tickfont_size=14,
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=0.1
    ),
    yaxis=dict(
        title='Value',
        title_font_size=18,
        tickfont_size=14,
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=0.1
    ),
    legend=dict(
        title='Variable',
        title_font_size=18,
        font_size=10,
        bgcolor='rgba(0,0,0,0)',
        yanchor='top',
        y=0.001,
        xanchor='right',
        x=1
    ),
    barmode='stack',
    plot_bgcolor='white',
    hoverlabel=dict(
        font_size=16,
        font_family='Arial',
        bgcolor='white',
        bordercolor='black'
    )
)

# Show the chart
fig_emissions.show()



