from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
from .data import load_correlation_data

def create_correlation_layout():
    data_temp = load_correlation_data()
    years = data_temp['Year']
    temp = data_temp['Average_Land_Temperature (celsius)']
    temp1 = data_temp['Average_LandOcean_Temperature (celsius)']
    emissions = data_temp['Average_Emissions (MtCO₂e)']
    sea = data_temp['Average_Sealevel (mm)']

    fig_corr1 = go.Figure()
    fig_corr1.add_trace(go.Scatter(x=years, y=temp, mode='lines+markers', name='Land Temperature', line=dict(color='red', width=2), marker=dict(color='red', size=8)))
    fig_corr1.add_trace(go.Scatter(x=years, y=emissions, mode='lines+markers', name='Carbon Emissions', line=dict(color='blue', width=2), marker=dict(color='blue', size=8), yaxis='y2'))
    fig_corr1.add_trace(go.Scatter(x=years, y=sea, mode='lines+markers', name='Sea level', line=dict(color='green', width=2), marker=dict(color='green', size=8), yaxis='y3'))
    fig_corr1.update_layout(
        font=dict(family='Arial', size=12, color='black'),
        title=dict(text='Correlation between Average Land Temperature, Carbon Emissions and Sea level (1990-2020)', xanchor='center', yanchor='top', x=0.5, y=0.95),
        xaxis=dict(title='Year', tickmode='linear', tick0=1990, dtick=5),
        yaxis=dict(title='Temperature (°C above pre-industrial levels)', range=[8.6, 10], color='red', title_font=dict(size=16)),
        yaxis2=dict(title='Carbon Emissions (metric tons per capita)', range=[22500, 37000], overlaying='y', side='right', color='blue', title_font=dict(size=16)),
        yaxis3=dict(title='Sea level(mm)', range=[-25, 69], overlaying='y', side='right', position=.94, color='green', title_font=dict(size=16)),
        legend=dict(orientation='h', yanchor='bottom', y=-0.2),
    )

    fig_corr3 = go.Figure()
    fig_corr3.add_trace(go.Scatter(x=years, y=temp1, mode='lines+markers', name='Land and Ocean Temperature', line=dict(color='red', width=2, shape='spline'), marker=dict(color='red', size=8)))
    fig_corr3.add_trace(go.Scatter(x=years, y=emissions, mode='lines+markers', name='Carbon Emissions', line=dict(color='blue', width=2, shape='spline'), marker=dict(color='blue', size=8), yaxis='y2'))
    fig_corr3.add_trace(go.Scatter(x=years, y=sea, mode='lines+markers', name='Sea level', line=dict(color='green', width=2, shape='spline'), marker=dict(color='green', size=8), yaxis='y3'))
    fig_corr3.update_layout(
        font=dict(family='Arial', size=12, color='black'),
        title=dict(text='Correlation between Average Land and Ocean Temperature, Carbon Emissions and Sea level (1990-2020)', xanchor='center', yanchor='top', x=0.5, y=0.95),
        xaxis=dict(title='Year', tickmode='linear', tick0=1990, dtick=5),
        yaxis=dict(title='Temperature (°C above pre-industrial levels)', range=[14, 18], color='red', title_font=dict(size=16)),
        yaxis2=dict(title='Carbon Emissions (metric tons per capita)', range=[22500, 37000], overlaying='y', side='right', color='blue', title_font=dict(size=16)),
        yaxis3=dict(title='Sea level(mm)', range=[-25, 69], overlaying='y', side='right', position=.94, color='green', title_font=dict(size=16)),
        legend=dict(orientation='h', yanchor='bottom', y=-0.2),
    )

    data_temp_subset = data_temp[['Year', 'Average_Land_Temperature (celsius)', 'Average_Emissions (MtCO₂e)', 'Average_Sealevel (mm)']]
    fig_corr2 = px.scatter(data_temp_subset, x='Average_Emissions (MtCO₂e)', y='Average_Land_Temperature (celsius)', color='Year',
                           size='Average_Emissions (MtCO₂e)', hover_data=['Year', 'Average_Land_Temperature (celsius)', 'Average_Emissions (MtCO₂e)', 'Average_Sealevel (mm)']).update_layout(title=dict(text='Correlation between Average Land Temperature, Carbon Emissions and Sea level (1990-2020)', xanchor='center', yanchor='top', x=0.5, y=0.95), xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))

    df_corr = data_temp
    fig_corr_temp = {
        'data': [
            {'x': df_corr['Year'], 'y': df_corr['Average_Land_Temperature (celsius)'], 'type': 'bar', 'name': 'Average Land Temperature', 'marker': {'color': 'green'}, "width": 0.5},
            {'x': df_corr['Year'], 'y': df_corr['Average_LandOcean_Temperature (celsius)'], 'type': 'bar', 'name': 'Average Land and Ocean Temperature', 'marker': {'color': 'pink'}, "width": 0.5},
        ],
        'layout': {
            'title': 'Average Temperatures by Year',
            'xaxis': {'title': 'Year'},
            'yaxis': {'title': 'Temperature', 'range': [8, 17]},
            'bargroupgap': 2,
            'bargap': 2,
        }
    }

    data_emissions = data_temp
    fig_emissions = px.bar(data_emissions, x='Year', y=['Average_Emissions (MtCO₂e)', 'Average_Land_Temperature (celsius)', 'Average_LandOcean_Temperature (celsius)'],
                          title='Greenhouse Gas Emissions vs Temperature')
    fig_emissions.update_layout(
        font_family='Arial',
        title_font_size=24,
        title_font_color='#404040',
        xaxis=dict(title='Year', title_font_size=18, tickfont_size=14, showgrid=True, gridcolor='lightgray', gridwidth=0.1),
        yaxis=dict(title='Carbon Emissions(MTCO2e)', title_font_size=18, tickfont_size=14, showgrid=True, gridcolor='lightgray', gridwidth=0.1),
        legend=dict(title='Variable', title_font_size=14, font_size=12, bgcolor='rgba(0,0,0,0)', yanchor='bottom', y=0.01, xanchor='right', x=1.4),
        barmode='stack',
        plot_bgcolor='white',
        hoverlabel=dict(font_size=14, font_family='Arial', bgcolor='white', bordercolor='black')
    )

    return html.Div(
        children=[
            html.Div(
                children=[
                    html.H1(children='Correlation between Average Land & Ocean Temperature, Carbon Emissions and Sea level (1990-2020)',
                            style={'font-size': '36px', 'color': 'white'}),
                    html.P(children='This dashboard visualizes Average Land temperature, Average Carbon Emission and Average Sea Level in a single plot',
                           style={'font-size': '20px', 'color': 'white', 'margin-top': '0px'})
                ],
                style={'text-align': 'center', 'padding-top': '50px', "display": 'block', "font-family": "PT Sans Narrow"}
            ),
            html.Div(
                children=[
                    dcc.Graph(id='corr_line_temp', figure=fig_corr_temp, style={"margin-bottom": "10px", 'border': '3px solid #2A547E'}),
                    dcc.Graph(id='corr_line', figure=fig_corr1, style={"margin-bottom": "10px", 'border': '3px solid #2A547E'}),
                    dcc.Graph(id='corr_bar_em', figure=fig_emissions, style={"margin-bottom": "10px", 'border': '3px solid #2A547E'}),
                    dcc.Graph(id='corr_line_1', figure=fig_corr3, style={"margin-bottom": "10px", 'border': '3px solid #2A547E'}),
                    dcc.Graph(id='corr_scatter', figure=fig_corr2, style={"margin-bottom": "10px", 'border': '3px solid #2A547E'}),
                ],
                style={'margin': '10px', 'display': 'block', 'flex-wrap': 'wrap'}
            )
        ],
        style={'background-color': '#4482C1'}
    )
