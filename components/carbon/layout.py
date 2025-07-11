from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
from .data import load_historical_emissions_data, load_sorted_emissions_data
import pandas as pd

def create_carbon_layout():
    data_carbon = load_historical_emissions_data()
    data_heat_carbon = load_sorted_emissions_data()

    # Barcharts
    top5 = data_carbon.groupby('Country')['CO2 Emissions'].sum().nlargest(5).reset_index()
    top5_df = data_carbon.loc[data_carbon['Country'].isin(top5['Country'])]
    bottom5 = data_carbon.groupby('Country')['CO2 Emissions'].sum().nsmallest(5).reset_index()
    bottom5_df = data_carbon.loc[data_carbon['Country'].isin(bottom5['Country'])]

    fig_top_5 = px.bar(top5_df, x='Country', y='CO2 Emissions', color='Year', barmode='group',
                       labels={'Country': 'Country', 'CO2 Emissions': 'Carbon Emissions (MTCO2e)', 'Year': 'Year'},
                       title='Bar Chart - Top five Countries in Carbon Emissions')
    fig_top_5.update_layout(height=400)

    fig_bottom_5 = px.bar(bottom5_df, x='Country', y='CO2 Emissions', color='Year', barmode='group',
                          labels={'Country': 'Country', 'CO2 Emissions': 'Carbon Emissions (MTCO2e)', 'Year': 'Year'},
                          title='Bar Chart - Bottom five Countries in Carbon Emissions')
    fig_bottom_5.update_layout(height=400)

    # Line charts
    top_5_countries = data_carbon.groupby('Country')['CO2 Emissions'].sum().nlargest(5).index
    bottom_5_countries = data_carbon.groupby('Country')['CO2 Emissions'].sum().nsmallest(5).index
    filtered_data_carbon_line = data_carbon[data_carbon['Country'].isin(top_5_countries) | data_carbon['Country'].isin(bottom_5_countries)]
    
    top_5_fig = px.line(filtered_data_carbon_line[filtered_data_carbon_line['Country'].isin(top_5_countries)], x="Year", y="CO2 Emissions", color="Country",
                        title="Line Chart - Top five Countries in Carbon Emissions")
    top_5_fig.update_layout(xaxis_title="Year", yaxis_title="C02 Emissions (MTCO2e)", font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"), height=400)

    bottom_5_fig = px.line(filtered_data_carbon_line[filtered_data_carbon_line['Country'].isin(bottom_5_countries)], x="Year", y="CO2 Emissions", color="Country",
                           title="Line Chart - Bottom five Countries in Carbon Emissions")
    bottom_5_fig.update_layout(xaxis_title="Year", yaxis_title="C02 Emissions (MTCO2e)", font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"), height=400)
    
    # Heatmap
    fig_heat_carbon = px.density_map(data_heat_carbon, lat='latitude', lon='longitude', z='CO2 Emissions',
                                     hover_data=['Country', 'CO2 Emissions', 'Year'], radius=20, zoom=1,
                                     map_style="carto-positron", animation_frame='Year', opacity=0.9,
                                     title='Heatmap of Average Temperature by Country',
                                     color_continuous_scale=px.colors.sequential.Viridis)
    
    # Racing bar chart
    race = data_carbon[data_carbon['Year'].between(1990, 2018)]
    df_total = race.groupby(['Country', 'Year'])['CO2 Emissions'].sum().reset_index()
    top10_countries = (df_total.groupby('Year').apply(lambda x: x.nlargest(10, 'CO2 Emissions'), include_groups=False).reset_index().drop('level_1', axis=1))
    top10_countries['Rank'] = top10_countries.groupby('Year')['CO2 Emissions'].rank(ascending=False)
    top10_countries['Color'] = pd.factorize(top10_countries['Country'])[0]

    frames = []
    for year in top10_countries['Year'].unique():
        df_year = top10_countries[top10_countries['Year'] == year]
        frame = go.Frame(data=[go.Bar(
            x=df_year['Country'], y=df_year['CO2 Emissions'],
            text=df_year['CO2 Emissions'].apply(lambda x: '{:.1f}'.format(x)),
            textposition='auto', marker_color=df_year['Color'],
            hovertemplate='%{y:.2f} MT CO2<extra></extra>',
        )])
        frames.append(frame)

    fig_race = go.Figure(
        data=[go.Bar(x=top10_countries[top10_countries['Rank'] == 1]['Country'], y=top10_countries[top10_countries['Rank'] == 1]['CO2 Emissions'],
                     text=top10_countries[top10_countries['Rank'] == 1]['CO2 Emissions'].apply(lambda x: '{:.1f}'.format(x)),
                     textposition='auto', marker_color=top10_countries[top10_countries['Rank'] == 1]['Color'],
                     hovertemplate='%{y:.2f} MT CO2<extra></extra>',
        )],
        layout=go.Layout(title='Top 10 Carbon Emitting Countries - 1990', xaxis=dict(title='Country'), yaxis=dict(title='Carbon Emissions (MT CO2)'), title_font=dict(color='black')),
        frames=frames,
    )

    # Bubble map
    df_bb = data_carbon[data_carbon['Year'].between(1990, 2018)]
    df_total1 = df_bb.groupby(['Country', 'Year'])['CO2 Emissions'].sum().reset_index()
    country_to_region = {'United States': 'North America', 'China': 'Asia', 'European Union (28)': 'Europe', 'India': 'Asia', 'Russia': 'Europe', 'Japan': 'Asia', 'Germany': 'Europe', 'South Korea': 'Asia', 'Iran': 'Middle East', 'Canada': 'North America', 'Saudi Arabia': 'Middle East', 'Brazil': 'South America', 'Indonesia': 'Asia'}
    df_total1['Region'] = df_total1['Country'].map(country_to_region)
    fig_bb = px.scatter(df_total1, x='CO2 Emissions', y='Year', size='CO2 Emissions', color='Region', log_x=True, range_x=[100, 15000], range_y=[1990, 2018], hover_name='Country', animation_frame='Year', title='CO2 Emissions by Country and Year')
    fig_bb.update_layout(xaxis_title='Total CO2 Emissions (metric tons)', yaxis_title='Year', legend_title='Region', font=dict(size=12))

    # Choropleth map
    data_carbon_choro = data_carbon.sort_values(by="Year", ascending=True)
    fig_carbon_choro = px.choropleth(data_carbon_choro, locations="Country", locationmode="country names", color="CO2 Emissions", animation_frame="Year", range_color=[0, 1000], title="Choropleth Map - Average Carbon Emissions by Country")

    return html.Div(
        children=[
            html.Div(
                children=[
                    html.H1(children='Carbon Emissions Visualization', style={'font-size': '36px', 'color': 'white'}),
                    html.P(children='This dashboard visualizes Global Carbon Emissions Data over the years (MTCO2e)', style={'font-size': '20px', 'color': 'white', 'margin-top': '0px'})
                ],
                style={'text-align': 'center', 'padding-top': '50px', "display": 'block', "font-family": "PT Sans Narrow"}
            ),
            html.Div([
                html.Div([
                    html.Label("Select countries to display:"),
                    dcc.Dropdown(id="country-dropdown",
                                 options=[{"label": country, "value": country} for country in data_carbon["Country"].unique()],
                                 value=["United States", "China"],
                                 multi=True)
                ], style={'width': '700px', "margin-top": "20px", 'margin-bottom': '20px', 'padding-left': '20px', 'font-size': '15px', 'border-color': '#2A547E', 'border-width': '2px'})
            ]),
            dcc.Graph(id="carbon-emissions-scatterplot", style={"margin-bottom": "10px", 'border': '3px solid #2A547E'}),
            html.H1(children='Top 10 Carbon Emitting Countries - Growth', style={'font-size': '20px', 'color': 'white', 'padding-left': '10px'}),
            dcc.Graph(id='carbon-emissions-bar', figure=fig_race, style={"margin-bottom": "10px", 'border': '3px solid #2A547E'}),
            dcc.Interval(id='interval-component', interval=600, n_intervals=0),
            html.Div(
                children=[
                    dcc.Graph(id='carbon-emissions-top-5', figure=fig_top_5, style={"margin-bottom": "10px", 'border': '3px solid #2A547E'}),
                    dcc.Graph(id='carbon-emissions-bottom-5', figure=fig_bottom_5, style={"margin-bottom": "10px", 'border': '3px solid #2A547E'}),
                ],
                style={"display": "flex", "flex-direction": "row", "justify-content": "space-between", "width": "100%"}
            ),
            dcc.Graph(id="carbon-bubble", figure=fig_bb, style={"margin-bottom": "10px", 'border': '3px solid #2A547E'}),
            dcc.Graph(id='top-5-chart', figure=top_5_fig, style={"margin-bottom": "10px", 'border': '3px solid #2A547E'}),
            dcc.Graph(id='bottom-5-chart', figure=bottom_5_fig, style={"margin-bottom": "10px", 'border': '3px solid #2A547E'}),
            dcc.Graph(id='choropleth-carbon-emissions', figure=fig_carbon_choro, style={"margin-bottom": "10px", 'border': '3px solid #2A547E', 'width': '100%', 'height': '850px'}),
            dcc.Graph(id='heatmap-carbon-emissions', figure=fig_heat_carbon, style={"margin-bottom": "10px", 'border': '3px solid #2A547E', 'width': '100%', 'height': '850px'}),
        ],
        style={'background-color': '#4482C1'}
    )
