from dash import callback, Input, Output, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .data import load_air_quality_data, get_cities

@callback(
    Output('aq-city-dropdown', 'options'),
    Output('aq-city-dropdown', 'value'),
    Input('aq-country-dropdown', 'value')
)
def set_cities_options(selected_country):
    if not selected_country:
        return [], None
    cities = get_cities(selected_country)
    options = [{'label': c, 'value': c} for c in cities]
    value = cities[0] if cities else None
    return options, value

def create_calendar_heatmap(df, metric):
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['year'] = df['date'].dt.year
    df['day_of_week'] = df['date'].dt.day_name()
    
    # Pivot data for heatmap
    pivot_table = df.pivot_table(values=metric, index='day_of_week', columns='day', aggfunc='mean')
    
    # Order days of the week correctly
    ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_table = pivot_table.reindex(ordered_days)

    fig = px.imshow(pivot_table,
                    labels=dict(x="Day of Month", y="Day of Week", color=metric.replace('_', ' ').title()),
                    x=pivot_table.columns,
                    y=pivot_table.index,
                    title=f'Calendar Heatmap for {metric.replace("_", " ").title()}')
    fig.update_xaxes(side="top")
    return fig

@callback(
    Output('aq-timeseries-plot', 'figure'),
    Output('aq-boxplot', 'figure'),
    Output('aq-scatterplot', 'figure'),
    Output('aq-calendar-heatmap', 'figure'),
    Output('aq-bar-chart', 'figure'),
    Input('aq-city-dropdown', 'value'),
    Input('aq-metric-dropdown', 'value'),
    Input('aq-country-dropdown', 'value')
)
def update_air_quality_graphs(city, metric, country):
    if not city or not metric:
        empty_fig = go.Figure().update_layout(
            paper_bgcolor="#1E3A5F", plot_bgcolor="#1E3A5F", 
            font_color="white", title_text="Please select a city and metric"
        )
        return empty_fig, empty_fig, empty_fig, empty_fig, empty_fig

    df = load_air_quality_data()
    city_df = df[df['city'] == city].sort_values(by='date')
    metric_label = metric.replace('_', ' ').title()

    # Time Series
    ts_fig = px.line(city_df, x='date', y=metric, title=f'{metric_label} Over Time in {city}')
    
    # Box Plot
    box_fig = px.box(city_df, y=metric, title=f'Distribution of {metric_label} in {city}')

    # Scatter Plot (example: metric vs. wind speed)
    scatter_fig = px.scatter(city_df, x='wind_speed', y=metric, 
                             title=f'{metric_label} vs. Wind Speed in {city}',
                             labels={'wind_speed': 'Wind Speed (m/s)'})

    # Calendar Heatmap
    calendar_fig = create_calendar_heatmap(city_df, metric)
    
    # Bar chart (comparing with other cities in the same country)
    country_df = df[df['country'] == country]
    bar_data = country_df.groupby('city')[metric].mean().reset_index()
    bar_fig = px.bar(bar_data, x='city', y=metric, title=f'Average {metric_label} Comparison in {country}')
    
    # Update layout for all figures to match the app's theme
    for fig in [ts_fig, box_fig, scatter_fig, calendar_fig, bar_fig]:
        fig.update_layout(paper_bgcolor="white", plot_bgcolor="white", font_color="black")

    return ts_fig, box_fig, scatter_fig, calendar_fig, bar_fig 