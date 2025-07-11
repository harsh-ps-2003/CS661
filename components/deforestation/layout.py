from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
from .data import load_deforestation_data, calculate_regional_stats

def create_deforestation_layout():
    # Load and process data
    df, time_series_df = load_deforestation_data()
    regional_stats = calculate_regional_stats(df)
    
    # Create REGIONAL trend plot (average forest cover per region, 2000 vs 2020)
    trend_df = (
        time_series_df
        .groupby(['Region', 'Year'])['Forest_Cover']
        .mean()
        .reset_index()
    )

    fig_trend = px.line(
        trend_df,
        x='Year',
        y='Forest_Cover',
        color='Region',
        markers=True,
        title='Regional Forest Cover Trend (2000 → 2020)',
        labels={'Forest_Cover': 'Average Forest Cover (%)', 'Year': 'Year'}
    )
    fig_trend.update_layout(
        width=1000,
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgb(245, 245, 245)',
        title_x=0.5,
        title_y=0.95,
        title_font_size=20,
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgb(228, 228, 228)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgb(228, 228, 228)')
    )

    # Create regional comparison bar chart
    fig_regional = px.bar(regional_stats,
                         x='Region',
                         y='Total_Loss',
                         title='Total Forest Cover Change by Region (2000-2020)',
                         labels={'Total_Loss': 'Change in Forest Cover (%)',
                                'Region': 'Region'},
                         color='Total_Loss',
                         color_continuous_scale='RdYlGn')  # Red for loss, green for gain
    fig_regional.update_layout(
        width=1000,
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgb(245, 245, 245)',
        title_x=0.5,
        title_y=0.95,
        title_font_size=20,
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgb(228, 228, 228)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgb(228, 228, 228)')
    )

    # Scatter Plot removed as per user request

    # Create box plot for current forest cover distribution by region
    fig_box = px.box(df,
                     x='Region',
                     y='forests_2020',
                     title='Current Forest Cover Distribution by Region',
                     labels={'forests_2020': 'Forest Cover in 2020 (%)',
                            'Region': 'Region'})
    fig_box.update_layout(
        width=1000,
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgb(245, 245, 245)',
        title_x=0.5,
        title_y=0.95,
        title_font_size=20,
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgb(228, 228, 228)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgb(228, 228, 228)')
    )

    return html.Div(
        children=[
            html.H1('Global Deforestation Analysis (2000-2020)', 
                   style={'textAlign': 'center', 'color': 'white', 'marginBottom': '30px', 'fontSize': '2.5em', 'fontWeight': 'bold'}),
            
            # Regional Trend Plot Section
            html.Div([
                html.H3('Regional Forest Cover Trend (2000 → 2020)', 
                        style={'textAlign': 'center', 'marginBottom': '20px', 'color': '#2c3e50', 'fontSize': '1.8em'}),
                dcc.Graph(
                    figure=fig_trend,
                    style={'margin': 'auto'}
                ),
            ], style={'margin': '20px', 'padding': '25px', 'backgroundColor': 'white', 'borderRadius': '15px', 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'}),
            
            # Regional Comparison Section
            html.Div([
                html.H3('Regional Forest Cover Changes', 
                        style={'textAlign': 'center', 'marginBottom': '20px', 'color': '#2c3e50', 'fontSize': '1.8em'}),
                dcc.Graph(
                    figure=fig_regional,
                    style={'margin': 'auto'}
                ),
            ], style={'margin': '20px', 'padding': '25px', 'backgroundColor': 'white', 'borderRadius': '15px', 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'}),
            
            # Scatter Plot removed as per user request
            
            # Box Plot Section
            html.Div([
                html.H3('Current Forest Cover by Region', 
                        style={'textAlign': 'center', 'marginBottom': '20px', 'color': '#2c3e50', 'fontSize': '1.8em'}),
                dcc.Graph(
                    figure=fig_box,
                    style={'margin': 'auto'}
                ),
            ], style={'margin': '20px', 'padding': '25px', 'backgroundColor': 'white', 'borderRadius': '15px', 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'})
        ],
        style={
            'background-color': '#4482C1',
            'padding': '30px',
            'maxWidth': '1400px',
            'margin': 'auto',
            'minHeight': '100vh'
        }
    ) 