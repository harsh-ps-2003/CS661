from dash import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .data import load_historical_emissions_data

data_carbon = load_historical_emissions_data()

# Prepare data for racing bar chart
race = data_carbon[data_carbon['Year'].between(1990, 2018)]
df_total = race.groupby(['Country', 'Year'])['CO2 Emissions'].sum().reset_index()
top10_countries = (df_total.groupby('Year')
                   .apply(lambda x: x.nlargest(10, 'CO2 Emissions'), include_groups=False)
                   .reset_index()
                   .drop('level_1', axis=1))
top10_countries['Rank'] = top10_countries.groupby('Year')['CO2 Emissions'].rank(ascending=False)
top10_countries['Color'] = pd.factorize(top10_countries['Country'])[0]

frames = []
for year in top10_countries['Year'].unique():
    df_year = top10_countries[top10_countries['Year'] == year]
    frame = go.Frame(data=[go.Bar(
        x=df_year['Country'],
        y=df_year['CO2 Emissions'],
        text=df_year['CO2 Emissions'].apply(lambda x: '{:.1f}'.format(x)),
        textposition='auto',
        marker_color=df_year['Color'],
        hovertemplate='%{y:.2f} MT CO2<extra></extra>',
    )])
    frames.append(frame)
    
fig_race = go.Figure(
    data=[go.Bar(x=top10_countries[top10_countries['Rank'] == 1]['Country'],
                 y=top10_countries[top10_countries['Rank'] == 1]['CO2 Emissions'],
                 text=top10_countries[top10_countries['Rank'] == 1]['CO2 Emissions'].apply(lambda x: '{:.1f}'.format(x)),
                 textposition='auto',
                 marker_color=top10_countries[top10_countries['Rank'] == 1]['Color'],
                 hovertemplate='%{y:.2f} MT CO2<extra></extra>',
    )],
    layout=go.Layout(
        title='Top 10 Carbon Emitting Countries - 1990',
        xaxis=dict(title='Country'),
        yaxis=dict(title='Carbon Emissions (MT CO2)'),
        title_font=dict(color='black')
    ),
    frames=frames,
)


def register_carbon_callbacks(app):
    @app.callback(Output("carbon-emissions-scatterplot", "figure"),
                  [Input("country-dropdown", "value")])
    def update_scatterplot(countries):
        filtered_data_carbon_scatter = data_carbon[data_carbon["Country"].isin(countries)]
        fig = px.scatter(filtered_data_carbon_scatter, title="Scatter Plot - Average Carbon Emissions by Country", x="Year", y="CO2 Emissions", color="Country", hover_data=["Country"])
        fig.update_layout(xaxis_title="Year",
                          yaxis_title="CO2 Emissions (MTCO2e) ",
                          font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"),
                          xaxis=dict(showgrid=False),
                          yaxis=dict(showgrid=False))
        return fig

    @app.callback(Output('carbon-emissions-bar', 'figure'),
                  Input('interval-component', 'n_intervals'))
    def update_carbon_emissions_bar(n):
        frame_index = n % len(frames)
        current_year = top10_countries['Year'].unique()[frame_index]
        fig_race.update_layout(title=f'Top 10 Carbon Emitting Countries - {current_year}')
        return frames[frame_index]
