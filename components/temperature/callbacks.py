from dash import Input, Output, dependencies
import plotly.graph_objects as go
import pandas as pd

from .data import load_major_city_temps
from .layout import fig11, fig21, fig31, fig41, fig51, fig61

def register_temperature_callbacks(app):
    @app.callback(Output('choropleth-map11', 'figure'),
                  [Input('choro-dropdown', 'value')])
    def update_choro(value):
        if value == 'fig11':
            return fig11
        elif value == 'fig21':
            return fig21
        elif value == 'fig31':
            return fig31
        elif value == 'fig41':
            return fig41
        elif value == 'fig51':
            return fig51
        elif value == 'fig61':
            return fig61

    @app.callback(
        [Output('city-dropdown', 'options'),
         Output('city-dropdown', 'value')],
        [Input('country-dropdown', 'value')])
    def update_cities(selected_country):
        if not selected_country:
            return [], None
            
        df = load_major_city_temps()
        filtered_cities = sorted(df[df['Country'] == selected_country]['City'].unique())
        options = [{'label': city, 'value': city} for city in filtered_cities]
        value = filtered_cities[0] if filtered_cities else None
        return options, value

    @app.callback(
        Output('monthly-temperature', 'figure'),
        [Input('country-dropdown', 'value'),
         Input('city-dropdown', 'value'),
         Input('year-dropdown', 'value')])
    def update_monthly_temperature(country, city, year):
        if not all([country, city, year]):
            return go.Figure().update_layout(
                title="Please select country, city, and year",
                xaxis_title="Day",
                yaxis_title="Month"
            )

        df = load_major_city_temps()
        mask = (
            (df['Country'] == country) & 
            (df['City'] == city) & 
            (df['Year'] == year) & 
            (df['AverageTemperature'] != -99)
        )
        df_filtered = df[mask].copy()
        
        if df_filtered.empty:
            return go.Figure().update_layout(
                title=f"No data available for {city}, {country} in {year}",
                xaxis_title="Day",
                yaxis_title="Month"
            )

        # Convert temperature from Fahrenheit to Celsius
        df_filtered.loc[:, 'AverageTemperature'] = (df_filtered['AverageTemperature'] - 32) * 5/9

        # Create a pivot table for the heatmap
        pivot_data = df_filtered.pivot_table(
            values='AverageTemperature',
            index='Month',
            columns='Day',
            aggfunc='mean'
        )

        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='RdBu_r',
            colorbar=dict(title="Temperature (°C)"),
            hoverongaps=False,
            hovertemplate="Day: %{x}<br>Month: %{y}<br>Temperature: %{z:.1f}°C<extra></extra>"
        ))

        fig.update_layout(
            title=f"Monthly Average Temperature in {city}, {country} ({year})",
            xaxis_title="Day of Month",
            yaxis_title="Month",
            yaxis=dict(
                ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                tickvals=list(range(1, 13))
            ),
            width=800,
            height=500
        )

        return fig
