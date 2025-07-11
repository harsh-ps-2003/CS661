from dash.dependencies import Input, Output, State
from dash import callback, html
import plotly.graph_objects as go
import plotly.express as px
import logging
from .data import load_sea_level_data, load_sea_ice_data, calculate_seasonal_cycle, calculate_monthly_trends

logger = logging.getLogger(__name__)

def create_empty_figure(title="No data available"):
    """Create an empty figure with a message."""
    fig = go.Figure()
    fig.add_annotation(
        text=title,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=20)
    )
    fig.update_layout(
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, showticklabels=False)
    )
    return fig

@callback(
    [
        Output('sea-level-bar', 'figure'),
        Output('sea-level-scatter', 'figure'),
        Output('sea-level-area', 'figure'),
        Output('sea-ice-seasonal', 'figure'),
        Output('sea-ice-trends', 'figure'),
        Output('sea-ice-extent', 'figure')
    ],
    [Input('sea-levels-container', 'children')]
)
def update_sea_level_figures(_):
    """Update all sea level and sea ice figures."""
    try:
        logger.info("Starting to update sea level figures")
        
        # Load sea level data
        sea_level_data = load_sea_level_data()
        if sea_level_data.empty:
            logger.warning("No sea level data available")
            return tuple(create_empty_figure() for _ in range(6))
        
        # Create sea level bar chart
        fig_bar = go.Figure(
            data=[go.Bar(x=sea_level_data['Year'], y=sea_level_data['Sea Level'])],
            layout=go.Layout(
                title=go.layout.Title(text="Sea Level Change Over Time", font=dict(size=24)),
                xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text="Year")),
                yaxis=go.layout.YAxis(title=go.layout.yaxis.Title(text="Sea Level (mm)")),
                width=1000,
                height=500,
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgb(245, 245, 245)',
                showlegend=False
            )
        )

        # Scatter plot
        fig_scatter = px.scatter(
            sea_level_data,
            x='Year',
            y='Sea Level',
            title='Sea Level Scatter Plot',
            labels={'Sea Level': 'Sea Level (mm)'},
            color_discrete_sequence=['#1f77b4']
        )
        fig_scatter.update_layout(
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

        # Area chart
        fig_area = px.area(
            sea_level_data,
            x='Year',
            y='Sea Level',
            title='Sea Level Area Chart',
            labels={'Sea Level': 'Sea Level (mm)'},
            color_discrete_sequence=['#3D9970']
        )
        fig_area.update_traces(
            line_color='darkblue',
            line_width=1,
            opacity=0.5
        )
        fig_area.update_layout(
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
        
        # Load and process sea ice data
        ice_data = load_sea_ice_data()
        if ice_data.empty:
            logger.warning("No sea ice data available")
            return (
                fig_bar,
                fig_scatter,
                fig_area,
                create_empty_figure("No sea ice data available"),
                create_empty_figure("No sea ice data available"),
                create_empty_figure("No sea ice data available")
            )
        
        seasonal_stats = calculate_seasonal_cycle(ice_data)
        monthly_avg, trends = calculate_monthly_trends(ice_data)

        # Create seasonal cycle plot
        fig_seasonal = go.Figure()
        
        fig_seasonal.add_trace(go.Scatter(
            x=seasonal_stats['DayOfYear'],
            y=seasonal_stats['Mean_Extent'],
            name='Mean Extent',
            line=dict(color='blue', width=2)
        ))
        
        fig_seasonal.add_trace(go.Scatter(
            x=seasonal_stats['DayOfYear'],
            y=seasonal_stats['Mean_Extent'] + seasonal_stats['Std_Extent'],
            fill=None,
            mode='lines',
            line_color='rgba(0,100,255,0)',
            showlegend=False
        ))
        
        fig_seasonal.add_trace(go.Scatter(
            x=seasonal_stats['DayOfYear'],
            y=seasonal_stats['Mean_Extent'] - seasonal_stats['Std_Extent'],
            fill='tonexty',
            mode='lines',
            line_color='rgba(0,100,255,0)',
            name='±1 Std Dev'
        ))
        
        fig_seasonal.update_layout(
            title='Sea Ice Extent Seasonal Cycle',
            xaxis_title='Day of Year',
            yaxis_title='Sea Ice Extent (million sq km)',
            hovermode='x unified',
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

        # Create monthly trends plot
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        if not trends.empty:
            trends['Month_Name'] = trends['Month'].map(lambda x: month_names[x-1])
            
            fig_trends = px.bar(
                trends,
                x='Month_Name',
                y='Trend',
                title='Monthly Sea Ice Extent Trends',
                labels={'Trend': 'Change Rate (million sq km/year)', 'Month_Name': 'Month'},
                color='Trend',
                color_continuous_scale='RdBu'
            )
        else:
            fig_trends = create_empty_figure("No trend data available")
        
        fig_trends.update_layout(
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

        # Create area plot for sea ice extent over time
        fig_extent = px.area(
            ice_data,
            x='Date',
            y='Extent',
            title='Sea Ice Extent Over Time',
            labels={'Extent': 'Sea Ice Extent (million sq km)', 'Date': 'Year'},
            color_discrete_sequence=['#3D9970']
        )
        
        fig_extent.update_traces(
            line_color='darkblue',
            line_width=1,
            opacity=0.5
        )
        
        fig_extent.update_layout(
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

        logger.info("Successfully updated all figures")
        return fig_bar, fig_scatter, fig_area, fig_seasonal, fig_trends, fig_extent
    except Exception as e:
        logger.error(f"Error updating figures: {e}")
        return tuple(create_empty_figure("Error loading data") for _ in range(6))
