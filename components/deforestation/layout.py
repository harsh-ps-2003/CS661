from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
from .data import load_deforestation_data, calculate_regional_stats

# Load and process data
df, time_series_df = load_deforestation_data()
regional_stats = calculate_regional_stats(df)

# ------------------------------------------------------------------
# Build Choropleth Map - % Forest Remaining (2020 vs 2000)
# ------------------------------------------------------------------

# Compute percentage remaining
df['Percent_Remain'] = (df['forests_2020'] / df['forests_2000']) * 100.0

fig_map = px.choropleth(
    df,
    locations='Country and Area',
    locationmode='country names',
    color='Percent_Remain',
    hover_name='Country and Area',
    hover_data={'Percent_Remain': ':.2f', 'forests_2020': ':,', 'forests_2000': ':,'},
    color_continuous_scale='Greens',
    range_color=(df['Percent_Remain'].min(), df['Percent_Remain'].max()),
    labels={'Percent_Remain': '% Forests Left'},
    title='% Forest Cover Remaining (2020 vs 2000)'
)

fig_map.update_layout(
    geo=dict(showframe=False, showcoastlines=False, projection_type='natural earth'),
    margin=dict(l=0, r=0, t=50, b=0),
    coloraxis_colorbar=dict(title='% Remaining')
)

regional_time_series = time_series_df.groupby(['Region', 'Year'])['Forest_Cover'].mean().reset_index()

# Define a consistent color palette for regions
color_palette = px.colors.qualitative.Plotly
region_colors = {region: color_palette[i % len(color_palette)] for i, region in enumerate(regional_stats['Region'])}

# --- Improved Bar Plot ---
fig_bar = go.Figure()

# Add zero line
fig_bar.add_vline(x=0, line_width=2, line_dash="dash", line_color="grey")

# Add bars
fig_bar.add_trace(go.Bar(
    y=regional_stats['Region'],
    x=regional_stats['Total_Loss'],
    orientation='h',
    marker_color=[region_colors[r] for r in regional_stats['Region']],
    text=regional_stats['Total_Loss'].apply(lambda x: f'{x:,.2f} km²'),
    textposition='auto'
))

# Annotations for context
fig_bar.add_annotation(
    x=regional_stats.loc[regional_stats['Region'] == 'South America', 'Total_Loss'].values[0],
    y='South America',
    text="Amazon deforestation",
    showarrow=True, arrowhead=1, ax=-40, ay=-40
)

fig_bar.update_layout(
    title='Total Forest Cover Change by Region (2000–2020)',
    xaxis_title='Total Forest Loss (km²)',
    yaxis_title='Region',
    paper_bgcolor='white',
    plot_bgcolor='#f8f9fa'
)

# --- Improved Line Plot ---
fig_line = go.Figure()

for region in regional_time_series['Region'].unique():
    region_df = regional_time_series[regional_time_series['Region'] == region]
    fig_line.add_trace(go.Scatter(
        x=region_df['Year'],
        y=region_df['Forest_Cover'],
        mode='lines+markers',
        name=region,
        line=dict(color=region_colors[region], width=2),
        marker=dict(size=8)
    ))

fig_line.update_layout(
    title='Regional Forest Cover Trend (2000–2020)',
    xaxis_title='Year',
    yaxis_title='Average Forest Cover (km²)',
    hovermode='x unified',
    legend_title='Region',
    legend=dict(x=1.05, y=1, xanchor='left', yanchor='top'),
    paper_bgcolor='white',
    plot_bgcolor='#f8f9fa'
)

# --- Main Layout ---
def create_deforestation_layout():
    return html.Div([
        html.H1("Global Deforestation Analysis", style={'textAlign': 'center', 'color': 'white'}),

        # Choropleth Map Section
        html.Div([
            html.H3("Global Forests Remaining (2020 vs 2000)", style={'textAlign': 'center'}),
            dcc.Graph(id='deforestation-choropleth', figure=fig_map, style={'height': '600px'})
        ], style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '15px', 'margin': '20px'}),

        # Bar Plot Section
            html.Div([
            html.H3("Forest Cover Change by Region", style={'textAlign': 'center'}),
            dcc.Graph(id='deforestation-bar-plot', figure=fig_bar)
        ], style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '15px', 'margin': '20px'}),

        # Line Plot Section
            html.Div([
            html.H3("Regional Trends Over Time", style={'textAlign': 'center'}),
            dcc.Graph(id='deforestation-line-plot', figure=fig_line)
        ], style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '15px', 'margin': '20px'})

    ], style={'backgroundColor': '#004d00', 'padding': '30px', 'minHeight': '100vh'}) 