from dash import Dash, dcc, html, Input, Output
import dash
import base64
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool
import json
from bokeh.embed import json_item
import matplotlib.pyplot as plt
from dash.dependencies import Input, Output

#Sea Level Card
# Load data from CSV file
data = pd.read_csv('dataset/Global_sea_level_rise.csv')
data.rename(columns={'year': 'Year', 'mmfrom1993-2008average': 'Sea Level'}, inplace=True)


# Create the bar chart
fig_bar = go.Figure(
    data=[go.Bar(x=data['Year'], y=data['Sea Level'],)],
    layout=go.Layout(
        title=go.layout.Title(text="Bar Chart", font=dict(size=24)),
        xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text="Year")),
        yaxis=go.layout.YAxis(title=go.layout.yaxis.Title(text="Sea Level (mm)")),
    )
)


area_fig = px.area(data, x='Year', y='Sea Level', title='Area Chart',
              labels={'Year': 'Year', 'Sea Level': 'Sea Level (mm)'},
              color_discrete_sequence=['#3D9970'])

# Add a gradient fill
area_fig.update_traces(mode='lines', fillcolor="aqua")

# Add a line color and shape
area_fig.update_traces(line_color='darkblue', line_shape='spline', line_smoothing=1.3, line_width=3)

# Adjust the opacity
area_fig.update_traces(opacity=0.2)

# Customize the layout
area_fig.update_layout(
    font_family='Arial',
    title_font_size=24,
    title_font_color='#404040',
    xaxis=dict(
        title_font_size=24,
        tickfont_size=14,
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=0.1,
        tickfont=dict(size=10)
    ),
    yaxis=dict(
        tickmode='linear',
        dtick=25,
        zeroline=True,
        zerolinecolor='lightgray',
        zerolinewidth=0.1,
        title_font_size=18,
        tickfont_size=14,
        showgrid=False,
        gridcolor='lightgray',
        gridwidth=0.01,
        tickfont=dict(size=10)
    ),
    legend=dict(
        title_font_size=18,
        font_size=14,
        bgcolor='rgba(0,0,0,0)',
        yanchor='bottom',
        y=0.01,
        xanchor='left',
        x=0.01
    ),
    plot_bgcolor='white',
    hoverlabel=dict(
        font_size=16,
        font_family='Arial',
        bgcolor='white',
        bordercolor='black'
    ),
    dragmode='zoom',
    clickmode='event+select'
)


# Create a box and whiskers plot with Plotly
fig_box = go.Figure()

fig_box.add_trace(go.Box(
    y=data['Sea Level'],
    name='Sea Level',
    boxmean=True, # set boxmean to True to color the box
    fillcolor='#d9b3ff', # set fillcolor to change the color of the box
    marker=dict(
        color='blue'
    ),
    line=dict(
        color='#00004d'
    )
))

# Create a scatter plot with Plotly
scatter_fig = px.scatter(data, x='Year', y='Sea Level', title='Scatter Plot',
                 labels={'Year': 'Year', 'Sea Level': 'Sea Level (mm)'}, color_discrete_sequence=['#3D9970'])

# Customize the layout
scatter_fig.update_layout(
    font_family='Arial',
    title_font_size=24,
    title_font_color='#404040',
    xaxis=dict(
        title_font_size=18,
        tickfont_size=14,
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=0.1,
        tickfont=dict(size=10)
    ),
    yaxis=dict(
        zeroline=True,
        zerolinecolor='lightgray',
        zerolinewidth=0.1,
        title_font_size=18,
        tickfont_size=14,
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=0.01,
        tickfont=dict(size=10)
    ),
    legend=dict(
        title_font_size=18,
        font_size=14,
        bgcolor='rgba(0,0,0,0)',
        yanchor='bottom',
        y=0.01,
        xanchor='left',
        x=0.01
    ),
    plot_bgcolor='white',
    hoverlabel=dict(
        font_size=16,
        font_family='Arial',
        bgcolor='white',
        bordercolor='black'
    )
)

# Customize the box plot layout
fig_box.update_layout(
    font_family='Arial',
    title="Box and Whiskers Plot",
    title_font_size=24,
    title_font_color='#404040',
    xaxis=dict(
        title_font_size=18,
        tickfont_size=14,
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=0.1,
        tickfont=dict(size=10)
    ),
    yaxis=dict(
        tickmode='linear',
        dtick=25,
        zeroline=True,
        zerolinecolor='lightgray',
        zerolinewidth=0.1,
        title_font_size=18,
        tickfont_size=14,
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=0.01,
        tickfont=dict(size=10)
    ),
    legend=dict(
        title_font_size=18,
        font_size=14,
        bgcolor='rgba(0,0,0,0)',
        yanchor='bottom',
        y=0.01,
        xanchor='left',
        x=0.01
    ),
    plot_bgcolor='#f7f7f7', # change plot background color
    hoverlabel=dict(
        font_size=16,
        font_family='Arial',
        bgcolor='white',
        bordercolor='black'
    ),

)
trace_markers = go.Scatter(x=data["Year"], y=data["Sea Level"], mode="markers", name="")
trace_lines = go.Scatter(x=data["Year"], y=data["Sea Level"], mode="lines",name="Lines", line=dict(width=3, color="blue"))
fig_line = go.Figure(data=[trace_markers, trace_lines])
fig_line.update_xaxes(range=[1950, max(data["Year"])],  zeroline=False,showgrid=False )
fig_line.update_yaxes( zeroline=False)
fig_line.update_layout(xaxis_title="Year", yaxis_title="Sea Level (mm)", template="plotly_dark",title="Line Chart", title_font=dict(size=24))


external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]


with open("dataset/earth_image1.png", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

#Correlation
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
# Load data from a CSV file
data_temp = pd.read_csv('dataset/avg_dataset.csv')

# Extract the relevant columns
years = data_temp['Year']
temp = data_temp['Average_Land_Temperature (celsius)']
temp1 = data_temp['Average_LandOcean_Temperature (celsius)']
emissions = data_temp['Average_Emissions (MtCO₂e)']
sea=data_temp['Average_Sealevel (mm)']

# Create figure
fig_corr1 = go.Figure()

# Add trace for temperature
fig_corr1.add_trace(go.Scatter(x=years, y=temp,
                         mode='lines+markers',
                         name='Land Temperature',
                         line=dict(color='red', width=2),
                         marker=dict(color='red', size=8)))

# Add trace for emissions
fig_corr1.add_trace(go.Scatter(x=years, y=emissions,
                         mode='lines+markers',
                         name='Carbon Emissions',
                         line=dict(color='blue', width=2),
                         marker=dict(color='blue', size=8),
                         yaxis='y2')) # assign the second y-axis to the emissions trace
# Add trace for emissions
fig_corr1.add_trace(go.Scatter(x=years, y=sea,
                         mode='lines+markers',
                         name='Sea level',
                         line=dict(color='green', width=2),
                         marker=dict(color='green', size=8),
                         yaxis='y3'))

# Update layout with custom styling
fig_corr1.update_layout(
#     plot_bgcolor='#FFFFFF', # set plot area background color
#     paper_bgcolor='#88B0D7', # remove background
    font=dict(family='Arial', size=12, color='black'), # set font and color
    title=dict(text='Correlation between Average Land Temperature, Carbon Emissions and Sea level (1990-2020)', # set title
               xanchor='center', yanchor='top', x=0.5, y=0.95),
    xaxis=dict(title='Year', tickmode='linear', tick0=1990, dtick=5), # set x-axis title and tick values
    yaxis=dict(title='Temperature (°C above pre-industrial levels)', range=[8.6, 10],color='red',title_font=dict(size=16)), # set y-axis title and range for temperature
    yaxis2=dict(title='Carbon Emissions (metric tons per capita)', range=[22500, 37000], overlaying='y', side='right',color='blue',title_font=dict(size=16)),
    yaxis3=dict(title='Sea level(mm)', range=[-25, 69], overlaying='y', side='right',position=.94,color='green',title_font=dict(size=16)), # set y-axis title and range for emissions

    legend=dict(orientation='h', yanchor='bottom', y=-0.2), # move legend to bottom
)


# Create figure
fig_corr3 = go.Figure()

# Add trace for temperature
fig_corr3.add_trace(go.Scatter(x=years, y=temp1,
                         mode='lines+markers',
                         name='Land and Ocean Temperature',
                         line=dict(color='red', width=2,shape='spline'),
                         marker=dict(color='red', size=8)))

# Add trace for emissions
fig_corr3.add_trace(go.Scatter(x=years, y=emissions,
                         mode='lines+markers',
                         name='Carbon Emissions',
                         line=dict(color='blue', width=2,shape='spline'),
                         marker=dict(color='blue', size=8),
                         yaxis='y2')) # assign the second y-axis to the emissions trace
# Add trace for emissions
fig_corr3.add_trace(go.Scatter(x=years, y=sea,
                         mode='lines+markers',
                         name='Sea level',
                         line=dict(color='green', width=2,shape='spline'),
                         marker=dict(color='green', size=8),
                         yaxis='y3'))

# Update layout with custom styling
fig_corr3.update_layout(
#     plot_bgcolor='#FFFFFF', # set plot area background color
#     paper_bgcolor='#88B0D7', # remove background
    font=dict(family='Arial', size=12, color='black'), # set font and color
    title=dict(text='Correlation between Average Land and Ocean Temperature, Carbon Emissions and Sea level (1990-2020)', # set title
               xanchor='center', yanchor='top', x=0.5, y=0.95),
    xaxis=dict(title='Year', tickmode='linear', tick0=1990, dtick=5), # set x-axis title and tick values
    yaxis=dict(title='Temperature (°C above pre-industrial levels)', range=[14, 18],color='red',title_font=dict(size=16)), # set y-axis title and range for temperature
    yaxis2=dict(title='Carbon Emissions (metric tons per capita)', range=[22500, 37000], overlaying='y', side='right',color='blue',title_font=dict(size=16)),
    yaxis3=dict(title='Sea level(mm)', range=[-25, 69], overlaying='y', side='right',position=.94,color='green',title_font=dict(size=16)), # set y-axis title and range for emissions

    legend=dict(orientation='h', yanchor='bottom', y=-0.2), # move legend to bottom
)


data_temp_subset = data_temp[['Year','Average_Land_Temperature (celsius)','Average_Emissions (MtCO₂e)','Average_Sealevel (mm)']]
fig_corr2=px.scatter(data_temp_subset, x='Average_Emissions (MtCO₂e)', y='Average_Land_Temperature (celsius)', color='Year',
                           size='Average_Emissions (MtCO₂e)', hover_data=['Year', 'Average_Land_Temperature (celsius)', 'Average_Emissions (MtCO₂e)', 'Average_Sealevel (mm)']).update_layout(title=dict(text='Correlation between Average Land Temperature, Carbon Emissions and Sea level (1990-2020)', # set title
               xanchor='center', yanchor='top', x=0.5, y=0.95),xaxis=dict(showgrid=False),
              yaxis=dict(showgrid=False))
# fig_corr2.update_layout(
#     plot_bgcolor='#FFFFFF', # set plot area background color
#     paper_bgcolor='#88B0D7')

df_corr = pd.read_csv('dataset/avg_dataset.csv')

fig_corr_temp={
            'data': [
                {'x': df_corr['Year'], 'y': df_corr['Average_Land_Temperature (celsius)'], 'type': 'bar', 'name': 'Average Land Temperature', 'marker': {'color': 'green'}, "width": 0.5, },
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
        title='Carbon Emissions(MTCO2e)',
        title_font_size=18,
        tickfont_size=14,
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=0.1
    ),
    legend=dict(
        title='Variable',
        title_font_size=14,
        font_size=12,
        bgcolor='rgba(0,0,0,0)',
        yanchor='bottom',
        y=0.01,
        xanchor='right',
        x=1.4
    ),
    barmode='stack',
    plot_bgcolor='white',
    hoverlabel=dict(
        font_size=14,
        font_family='Arial',
        bgcolor='white',
        bordercolor='black'
    )
)

#Carbon Emissions

#Temperature card
import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio

pio.renderers.default = 'browser'

india_states = json.load(open("dataset/states_india.geojson", "r"))

us_states=json.load(open("dataset/us-states.json", "r"))

can_states=json.load(open("dataset/canada.geojson", "r"))

china_states=json.load(open("dataset/China_geo.json", "r"))

rus_states=json.load(open("dataset/Russia_geo.json", "r"))

brz_states=json.load(open("dataset/brazil_geo.json", "r"))

#Temperature Maps-1

state_id_map1 = {}
state_id_map2 = {}
state_id_map3 = {}
state_id_map4 = {}
state_id_map5 = {}
state_id_map6 = {}


for feature in brz_states["features"]:
    feature["id"] = feature["id"]
    state_id_map1[feature["properties"]["name"]] = feature["id"]
for feature in rus_states["features"]:
    feature["id"] = feature["properties"]["ID_1"]
    state_id_map2[feature["properties"]["NAME_1"]] = feature["id"]
for feature in india_states["features"]:
    feature["id"] = feature["properties"]["state_code"]
    state_id_map3[feature["properties"]["st_nm"]] = feature["id"]
for feature in china_states["features"]:
    feature["id"] = feature["properties"]["HASC_1"]
    state_id_map4[feature["properties"]["NAME_1"]] = feature["id"]
for feature in can_states["features"]:
    feature["id"] = feature["properties"]["cartodb_id"]
    state_id_map5[feature["properties"]["name"]] = feature["id"]
for feature in us_states["features"]:
    feature["id"] = feature["id"]
    state_id_map6[feature["properties"]["name"]] = feature["id"]


df1 = pd.read_csv("dataset/India_temperatures.csv")
df1["id"] = df1["State"].apply(lambda x: state_id_map3[x])
df2 = pd.read_csv("dataset/China_temperatures.csv")
df2["id"] = df2["State"].apply(lambda x: state_id_map4[x])
df3 = pd.read_csv("dataset/Canada_temperatures.csv")
df3["id"] = df3["State"].apply(lambda x: state_id_map5[x])
df4 = pd.read_csv("dataset/Brazil_temperatures.csv")
df4["id"] = df4["State"].apply(lambda x: state_id_map1[x])
df5 = pd.read_csv("dataset/Russia_temperatures.csv")
df5["id"] = df5["State"].apply(lambda x: state_id_map2[x])
df6 = pd.read_csv("dataset/US_temperatures.csv")
df6["id"] = df6["State"].apply(lambda x: state_id_map6[x])



fig11 = px.choropleth_mapbox(
    df1,
    locations="id",
    geojson=india_states,
    color="AverageTemperature",
    color_continuous_scale='Turbo',
    hover_name="State",
    hover_data=["AverageTemperature"],
    title="Average Temperature INDIA",
    mapbox_style="carto-positron",
    center={"lat": 24, "lon": 78},
    zoom=3.7,
    opacity=0.3,
    width=1400,  # Change width to 800 pixels
    height=800,
)

fig21 = px.choropleth_mapbox(
    df2,
    locations="id",
    geojson=china_states,
    color="AverageTemperature",
    color_continuous_scale='Turbo',
    hover_name="State",
    hover_data=["AverageTemperature"],
    title="Average Temperature CHINA",
    mapbox_style="carto-positron",
    center={"lat": 37, "lon": 104},
 zoom=3,
    opacity=0.5,
    width=1400,  # Change width to 800 pixels
    height=800,
)


fig31 = px.choropleth_mapbox(
    df3,
    locations="id",
    geojson=can_states,
    color="AverageTemperature",
    color_continuous_scale='Turbo',
    hover_name="State",
    hover_data=["AverageTemperature"],
    title="Average Temperature CANADA",
    mapbox_style="carto-positron",
    center={"lat": 72, "lon": -99},
  zoom=1.9,
    opacity=0.5,
    width=1400,  # Change width to 800 pixels
    height=800,
)


fig41 = px.choropleth_mapbox(
    df4,
    locations="id",
    geojson=brz_states,
    color="AverageTemperature",
    color_continuous_scale='Turbo',
    hover_name="State",
    hover_data=["AverageTemperature"],
    title="Average Temperature BRAZIL",
    mapbox_style="carto-positron",
    center={"lat": -12, "lon": -56},
    zoom=3,
    opacity=0.5,
    width=1400,  # Change width to 800 pixels
    height=800,
)

fig51 = px.choropleth_mapbox(
    df5,
    locations="id",
    geojson=rus_states,
    color="AverageTemperature",
    color_continuous_scale='Turbo',
    hover_name="State",
    hover_data=["AverageTemperature"],
    title="Average Temperature RUSSIA",
    mapbox_style="carto-positron",
    center={"lat": 68, "lon": 101},
    zoom=2.1,
    opacity=0.5,
    width=1400,  # Change width to 800 pixels
    height=800,
)
fig61 = px.choropleth_mapbox(
    df6,
    locations="id",
    geojson=us_states,
    color="AverageTemperature",
    color_continuous_scale='Turbo',
    hover_name="State",
    hover_data=["AverageTemperature"],
    title="Average Temperature USA",
    mapbox_style="carto-positron",
    center={"lat": 53, "lon": -113},
    zoom=2.3,
    opacity=0.5,
    width=1400,  # Change width to 800 pixels
    height=800,
)


# Load data from CSV file
data_heatmap = pd.read_csv('dataset/UpdatedMajorCity_temperatures.csv')

# Create heatmap using latitude and longitude values
fig_heat = px.density_map(data_heatmap,
                        lat='Latitude_Float',
                        lon='Longitude_Float',
                        z='AverageTemperature',
                        hover_data=["City"],
                         radius=8,
                         zoom=1,

                        map_style="carto-positron",
                        animation_frame='dt',
                        opacity=0.5,
                        title='Average Temperature Heatmap by Cities')
fig_heat.update_layout(
    updatemenus=[dict(
        type='buttons',

        buttons=list([
            dict(
                label='Play',
                method='animate',
                args=[None, {'frame': {'duration': 500, 'redraw': True},
                             'fromcurrent': True, 'transition': {'duration': 0}}]
            ),
            dict(
                label='Pause',
                method='animate',
                args=[[None], {'frame': {'duration': 0, 'redraw': False},
                               'mode': 'immediate',
                               'transition': {'duration': 0}}]
            )
        ]),
        direction='left',
        pad={'r': 10, 't': 10},
        x=0.1,
        y=0,
        showactive=True,
        active=0
    )])




# Read the file (countries + cities)
countries = pd.read_csv("dataset/GlobalLandTemperaturesByCity.csv")

# Because the file is very big and there are many dates missing (like the last file), we will group by year
# create column year
countries['Date'] = pd.to_datetime(countries['dt'])
countries['year'] = countries['Date'].dt.year

# Group by year
by_year = countries.groupby(by = ['year', 'City', 'Country', 'Latitude', 'Longitude']).mean(numeric_only=True).reset_index()

# Append the continent & iso codes
continent_map = pd.read_csv("dataset/continents2.csv.xls")
continent_map['Country'] = continent_map['name']
continent_map = continent_map[['Country', 'region', 'alpha-2', 'alpha-3']]

# Add information
data_diff = pd.merge(left = by_year, right = continent_map, on = 'Country', how = 'left')

# Filter starting 1825 - because some countries weren't monitored before this year on some periods,
# the mean overall could be quite misleading (example: Americas have an increase from 1821 to 1825 of 5 points in temperature,
# but this happens only because in 1824 data for South America started to be collected)
data_diff = data_diff[data_diff['year'] >= 1825]

# Datasets:

region = data_diff.dropna(axis = 0).groupby(by = ['region', 'year']).mean(numeric_only=True).reset_index()
countries = data_diff.dropna(axis = 0).groupby(by = ['region', 'Country', 'year']).mean(numeric_only=True).reset_index()
cities = data_diff.dropna(axis = 0).groupby(by = ['region', 'Country', 'City', 'year', 'Latitude', 'Longitude']).mean(numeric_only=True).reset_index()



# Perform data manipulation
mean = countries.groupby(['Country', 'region'])['AverageTemperature'].mean().reset_index()
maximum = countries.groupby(['Country', 'region'])['AverageTemperature'].max().reset_index()

difference = pd.merge(left=mean, right=maximum, on=['Country', 'region'])
difference['diff'] = difference['AverageTemperature_y'] - difference['AverageTemperature_x']

sort_diff = difference[['Country', 'region', 'diff']].sort_values(by='diff', ascending=True)


# Define the graph
fig_diff = px.bar(sort_diff, x='diff', y='Country', orientation='h',
             color='diff', color_continuous_scale='RdBu_r',
             height=3500, width=1000)

fig_diff.update_layout(
    title="Countries Rank - from the biggest to smallest increase in temperature since 1825",
    font=dict(family="Courier New, monospace", size = 13, color="#7f7f7f"),
    template="ggplot2"
)

fig_diff.update_xaxes(showline=True, linewidth=1, linecolor='gray')
fig_diff.update_yaxes(showline=True, linewidth=1, linecolor='gray')



# Load data
df = pd.read_csv('dataset/UpdatedMajorCity_temperatures.csv', encoding='utf-8')
df = df.drop_duplicates()

# Convert 'dt' to datetime and extract Year, Month, Day
df['Date'] = pd.to_datetime(df['dt'], errors='coerce')
df = df.dropna(subset=['Date'])
df['Year'] = df['Date'].dt.year.astype(int)
df['Month'] = df['Date'].dt.month.astype(int)
df['Day'] = df['Date'].dt.day.astype(int)

# Add region information
continent_map = pd.read_csv("dataset/continents2.csv.xls")
continent_map.rename(columns={'name': 'Country', 'region': 'Region'}, inplace=True)
df = pd.merge(left=df, right=continent_map[['Country', 'Region']], on='Country', how='left')

df = df[df['Year'] > 1994]
df = df[df['Year'] < 2020]
df = df[df['AverageTemperature'] > -70]
df['AverageTemperature'] = (df['AverageTemperature'] - 32)*(5/9)

fig_lines=px.line(
            df.groupby(['Region', 'Year'])['AverageTemperature'].mean().reset_index(),
            x='Year',
            y='AverageTemperature',
            color='Region',
            title='Average temperatures of Continents over the years 1994 to 2019',
            hover_data={'Year': False, 'AverageTemperature': ':.2f'},
            labels={'AverageTemperature': 'Avg Temp'}
        )

fig_lines.update_traces(mode='markers+lines')
fig_lines.update_layout(hovermode='x', plot_bgcolor= '#FFFFFF',
            paper_bgcolor= '#FFFFFF',)



#Scatter_geo Global Map - Difference between the Mean and Max Temperatures-5


# Read the file (countries + cities)
countries = pd.read_csv("dataset/GlobalLandTemperaturesByCity.csv")

# Because the file is very big and there are many dates missing (like the last file), we will group by year
# create column year
countries['Date'] = pd.to_datetime(countries['dt'])
countries['year'] = countries['Date'].dt.year

# Group by year
by_year = countries.groupby(by = ['year', 'City', 'Country', 'Latitude', 'Longitude']).mean(numeric_only=True).reset_index()

# Append the continent & iso codes
continent_map = pd.read_csv("dataset/continents2.csv.xls")
continent_map['Country'] = continent_map['name']
continent_map = continent_map[['Country', 'region', 'alpha-2', 'alpha-3']]

# Add information
data_maxmin = pd.merge(left = by_year, right = continent_map, on = 'Country', how = 'left')

# Filter starting 1825 - because some countries weren't monitored before this year on some periods,
# the mean overall could be quite misleading (example: Americas have an increase from 1821 to 1825 of 5 points in temperature,
# but this happens only because in 1824 data for South America started to be collected)
data_maxmin = data_maxmin[data_maxmin['year'] >= 1825]

# Datasets:

region = data_maxmin.dropna(axis = 0).groupby(by = ['region', 'year']).mean(numeric_only=True).reset_index()
countries = data_maxmin.dropna(axis = 0).groupby(by = ['region', 'Country', 'year']).mean(numeric_only=True).reset_index()
cities = data_maxmin.dropna(axis = 0).groupby(by = ['region', 'Country', 'City', 'year', 'Latitude', 'Longitude']).mean(numeric_only=True).reset_index()

# Data - we need iso alpha-3 codes
map_countries = data_maxmin.dropna(axis = 0).groupby(by = ['region', 'Country', 'year','alpha-3']).mean(numeric_only=True).reset_index()

# Min temperature is -5.453083, and because the size in a map cannot be negative, we will add 6 to all temperatures
# to "standardize the data"
map_countries['AverageTemperature'] = map_countries['AverageTemperature'] + 6

# Perform data manipulation
mean = map_countries.groupby(['region','Country','alpha-3'])['AverageTemperature'].mean().reset_index()
maximum = map_countries.groupby(['region','Country','alpha-3'])['AverageTemperature'].max().reset_index()
difference = pd.merge(left = mean, right = maximum, on = ['region','Country','alpha-3'])
difference['diff'] = difference['AverageTemperature_y'] - difference['AverageTemperature_x']
difference.rename(columns = {'AverageTemperature_y':'Maximum Average Temperature',
                             'AverageTemperature_x':'Overall Avg Temp'}, inplace = True)
# Define the graph
fig_maxmin = px.scatter_geo(difference, locations="alpha-3", color="Overall Avg Temp",
                     hover_name="Country", size="diff", size_max=15,
                     projection="natural earth", opacity = 0.8,
                     color_continuous_scale=('#283747', '#2874A6', '#3498DB', '#F5B041', '#E67E22', '#A93226'))

fig_maxmin.update_layout(
    title= "Globe Map - Difference in Average temperature from 1825-2018",
    font=dict(family="Courier New, monospace", size = 13, color="#7f7f7f"),
    template="ggplot2"
)



# Load data from CSV file
data_timeline = pd.read_csv('dataset/avg_dataset.csv')

data_timeline_filtered = data_timeline[data_timeline.index % 13 == 0]

# Save the filtered data to a new CSV file
data_timeline_filtered.to_csv('dataset/filtered_data.csv', index=False)

# Create a line chart with Plotly
fig_timeline = px.line(data_timeline, x='Year', y='Average_Land_Temperature (celsius)',  title='Earth Temperature Timeline')

# Customize the layout
fig_timeline.update_layout(
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
        title='Average Temperature (°C)',
        title_font_size=18,
        tickfont_size=14,
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=0.1
    ),
    legend=dict(
        title='Country',
        title_font_size=18,
        font_size=14,
        bgcolor='rgba(0,0,0,0)',
        yanchor='bottom',
        y=0.01,
        xanchor='left',
        x=0.01
    ),
    plot_bgcolor='white',
    hoverlabel=dict(
        font_size=16,
        font_family='Arial',
        bgcolor='white',
        bordercolor='black'
    )
)



# Load data
df_choro = pd.read_csv('dataset/GlobalLandTemperaturesByCountry.csv')

# Preprocess data
df_choro = df_choro.dropna()
df_choro['date'] = pd.to_datetime(df_choro['dt'])
df_choro['Year'] = df_choro['date'].dt.year
df_choro = df_choro.groupby(['Country', 'Year'])['AverageTemperature'].mean().reset_index()

# Create the app

fig_choro=px.choropleth(df_choro,
                             locations='Country',
                             locationmode='country names',
                             color='AverageTemperature',
                             color_continuous_scale='Turbo',
                             animation_frame='Year',
#                              range_color=[-5, 35],
                             title='Choropleth Map - Average Temperatures by Country'
                            )

global_temp_country = pd.read_csv('dataset/GlobalLandTemperaturesByCountry-2.csv')


#Let's remove the duplicated countries (in the analysis, we don't consider the presence of
#colonies at this the countries) and countries for which no information about the temperature

global_temp_country_clear = global_temp_country[~global_temp_country['Country'].isin(
    ['Denmark', 'Antarctica', 'France', 'Europe', 'Netherlands',
     'United Kingdom', 'Africa', 'South America'])]

global_temp_country_clear = global_temp_country_clear.replace(
   ['Denmark (Europe)', 'France (Europe)', 'Netherlands (Europe)', 'United Kingdom (Europe)'],
   ['Denmark', 'France', 'Netherlands', 'United Kingdom'])

#Let's average temperature for each country

countries = np.unique(global_temp_country_clear['Country'])
mean_temp = []
for country in countries:
    mean_temp.append(global_temp_country_clear[global_temp_country_clear['Country'] ==
                                               country]['AverageTemperature'].mean())



data_globe = [ dict(
        type = 'choropleth',
        locations = countries,
        z = mean_temp,
        locationmode = 'country names',
        text = countries,
        marker = dict(
            line = dict(color = 'rgb(0,0,0)', width = 1)),
            colorbar = dict(autotick = True, tickprefix = '',
            title = '# Average\nTemperature,\n°C')
            )
       ]

layout = dict(
    title = 'Average land temperature in countries',
    geo = dict(
        showframe = False,
        showocean = True,
        oceancolor = 'rgb(0,255,255)',
        projection = dict(
        type = 'orthographic',
            rotation = dict(
                    lon = 60,
                    lat = 10),
        ),
        lonaxis =  dict(
                showgrid = False,
                gridcolor = 'rgb(102, 102, 102)'
            ),
        lataxis = dict(
                showgrid = True,
                gridcolor = 'rgb(102, 102, 102)'
                )
            ),
        )

fig_globe = dict(data=data_globe , layout=layout)



fig_CC = pd.read_csv("dataset/UpdatedMajorCity_temperatures.csv")


# Define CSS styles
# styles = {
#     'column': {
#         'display': 'inline-block',
#         'width': '30%',
#         'padding': '0 0 0',
#         'boxSizing': 'border-box',
#         'verticalAlign': 'top'
#     }
# }

# CARBON EMISSIONS

#Scatter PLot

data_carbon_scatter = pd.read_csv('dataset/historical_emissions.csv')
data_carbon_scatter = data_carbon_scatter.melt(id_vars=["Country", "Data source", "Sector", "Gas", "Unit"],
                                             var_name="Year",
                                             value_name="CO2 Emissions")
data_carbon_scatter['Year'] = pd.to_numeric(data_carbon_scatter['Year'])

#barchart

data_carbon_bar = pd.read_csv('dataset/historical_emissions.csv')
data_carbon_bar = data_carbon_bar.melt(id_vars=["Country", "Data source", "Sector", "Gas", "Unit"],
                                       var_name="Year",
                                       value_name="CO2 Emissions")
data_carbon_bar['Year'] = pd.to_numeric(data_carbon_bar['Year'])

# sort the data by CO2 emissions
data_carbon_bar_sorted = data_carbon_bar.sort_values(by='CO2 Emissions', ascending=False)

top5 = data_carbon_bar.groupby('Country')['CO2 Emissions'].sum().nlargest(5).reset_index()
top5_df = data_carbon_bar.loc[data_carbon_bar['Country'].isin(top5['Country'])]

bottom5 = data_carbon_bar.groupby('Country')['CO2 Emissions'].sum().nsmallest(5).reset_index()
bottom5_df = data_carbon_bar.loc[data_carbon_bar['Country'].isin(bottom5['Country'])]

# create the top 5 bar chart using plotly
fig_top_5 = px.bar(top5_df, x='Country', y='CO2 Emissions', color='Year', barmode='group',
                   labels={'Country': 'Country', 'CO2 Emissions': 'Carbon Emissions (MTCO2e)', 'Year': 'Year'},
                   title='Bar Chart - Top five Countries in Carbon Emissions')

# increase the height of the figure
fig_top_5.update_layout(height=400)

# create the bottom 5 bar chart using plotly
fig_bottom_5 = px.bar(bottom5_df, x='Country', y='CO2 Emissions', color='Year', barmode='group',
                      labels={'Country': 'Country', 'CO2 Emissions': 'Carbon Emissions (MTCO2e)', 'Year': 'Year'},
                      title='Bar Chart - Bottom five Countries in Carbon Emissions')

# increase the height of the figure
fig_bottom_5.update_layout(height=400)





#Line chart
data_carbon_line = pd.read_csv('dataset/historical_emissions.csv')
data_carbon_line = data_carbon_line.melt(id_vars=["Country", "Data source", "Sector", "Gas", "Unit"],
                                         var_name="Year",
                                         value_name="CO2 Emissions")
data_carbon_line['Year'] = pd.to_numeric(data_carbon_line['Year'])

# filter the dataset to include only top 5 and bottom 5 countries based on CO2 emissions
top_5_countries = data_carbon_line.groupby('Country')['CO2 Emissions'].sum().nlargest(5).index
bottom_5_countries = data_carbon_line.groupby('Country')['CO2 Emissions'].sum().nsmallest(5).index
filtered_data_carbon_line = data_carbon_line[data_carbon_line['Country'].isin(top_5_countries) | data_carbon_line['Country'].isin(bottom_5_countries)]

# create the line chart for top 5 countries using plotly express
top_5_fig = px.line(filtered_data_carbon_line[filtered_data_carbon_line['Country'].isin(top_5_countries)], x="Year", y="CO2 Emissions", color="Country",
              title="Line Chart - Top five Countries in Carbon Emissions")

# customize the layout of the top 5 line chart
top_5_fig.update_layout(
    xaxis_title="Year",
    yaxis_title="C02 Emissions (MTCO2e)",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="#7f7f7f"
    ))

top_5_fig.update_layout(height = 400)

# create the line chart for bottom 5 countries using plotly express
bottom_5_fig = px.line(filtered_data_carbon_line[filtered_data_carbon_line['Country'].isin(bottom_5_countries)], x="Year", y="CO2 Emissions", color="Country",
              title="Line Chart - Bottom five Countries in Carbon Emissions")

# customize the layout of the bottom 5 line chart
bottom_5_fig.update_layout(
    xaxis_title="Year",
    yaxis_title="C02 Emissions (MTCO2e)",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="#7f7f7f"
    )
)
bottom_5_fig.update_layout(height = 400)


#HEAT MAP
data_heat_carbon = pd.read_csv('dataset/sorted_data_with_lat_lon.csv')

# Create heatmap using latitude and longitude values
fig_heat_carbon = px.density_map(data_heat_carbon,
                        lat='latitude',
                        lon='longitude',
                        z='CO2 Emissions',
                        hover_data=['Country', 'CO2 Emissions', 'Year'],
                         radius=20,
                         zoom=1,
                        map_style="carto-positron",
                        animation_frame='Year',
                        opacity=0.9,
                        title='Heatmap of Average Temperature by Country',
                        color_continuous_scale=px.colors.sequential.Viridis,)
fig_heat_carbon.update_layout(
    updatemenus=[dict(
        type='buttons',

        buttons=list([
            dict(
                label='Play',
                method='animate',
                args=[None, {'frame': {'duration': 500, 'redraw': True},
                             'fromcurrent': True, 'transition': {'duration': 0}}]
            ),
            dict(
                label='Pause',
                method='animate',
                args=[[None], {'frame': {'duration': 0, 'redraw': False},
                               'mode': 'immediate',
                               'transition': {'duration': 0}}]
            )
        ]),
        direction='left',
        pad={'r': 10, 't': 10},
        x=0.1,
        y=0,
        showactive=True,
        active=0
    )])

race = pd.read_csv('dataset/historical_emissions.csv')
race = race.melt(id_vars=["Country", "Data source", "Sector", "Gas", "Unit"],
                 var_name="Year",
                 value_name="CO2 Emissions")
race['Year'] = pd.to_numeric(race['Year'])


# Filter data to years 1990 to 2018
race = race[race['Year'].between(1990, 2018)]

# Calculate total CO2 emissions for each country and year
df_total = race.groupby(['Country', 'Year'])['CO2 Emissions'].sum().reset_index()

# Get top 10 emitting countries for each year
top10_countries = (df_total.groupby('Year')
                   .apply(lambda x: x.nlargest(10, 'CO2 Emissions'), include_groups=False)
                   .reset_index()
                   .drop('level_1', axis=1))

# Add a rank column for each year
top10_countries['Rank'] = top10_countries.groupby('Year')['CO2 Emissions'].rank(ascending=False)

# Add a color column based on the country
top10_countries['Color'] = pd.factorize(top10_countries['Country'])[0]

# Create animation frames
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

# Set layout and add animation frames to the figure
# Set layout and add animation frames to the figure

fig_race = go.Figure(
    data=[go.Bar(        x=top10_countries[top10_countries['Rank'] == 1]['Country'],
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

#bubble map
df_bb = pd.read_csv('dataset/historical_emissions.csv')
df_bb = df_bb.melt(id_vars=["Country", "Data source", "Sector", "Gas", "Unit"],
                   var_name="Year",
                   value_name="CO2 Emissions")
df_bb['Year'] = pd.to_numeric(df_bb['Year'])

# Filter data to years 1990 to 2018
df_bb = df_bb[df_bb['Year'].between(1990, 2018)]

# Calculate total CO2 emissions for each country and year
df_total1 = df_bb.groupby(['Country', 'Year'])['CO2 Emissions'].sum().reset_index()

# Create a dictionary to map countries to regions
country_to_region = {
    'United States': 'North America',
    'China': 'Asia',
    'European Union (28)': 'Europe',
    'India': 'Asia',
    'Russia': 'Europe',
    'Japan': 'Asia',
    'Germany': 'Europe',
    'South Korea': 'Asia',
    'Iran': 'Middle East',
    'Canada': 'North America',
    'Saudi Arabia': 'Middle East',
    'Brazil': 'South America',
    'Indonesia':'Asia'
}

# Map countries to regions
df_total1['Region'] = df_total1['Country'].map(country_to_region)

# Create a figure using Gapminder API
fig_bb = px.scatter(df_total1, x='CO2 Emissions', y='Year', size='CO2 Emissions',
                 color='Region', log_x=True, range_x=[100, 15000],range_y=[1990,2018],
                 hover_name='Country', animation_frame='Year',
                 title='CO2 Emissions by Country and Year')

# Update the layout
fig_bb.update_layout(
    xaxis_title='Total CO2 Emissions (metric tons)',
    yaxis_title='Year',
    legend_title='Region',
    font=dict(size=12)
)

#choropleth map


data_carbon_choro = pd.read_csv("dataset/historical_emissions.csv")
data_carbon_choro = data_carbon_choro.melt(id_vars=["Country", "Data source", "Sector", "Gas", "Unit"],
                                           var_name="Year",
                                           value_name="CO2 Emissions")
data_carbon_choro['Year'] = pd.to_numeric(data_carbon_choro['Year'])
# Sort the DataFrame by ascending year
data_carbon_choro = data_carbon_choro.sort_values(by="Year", ascending=True)

# Create a dropdown menu to select the year
year_options = [{"label": year, "value": year} for year in data_carbon_choro.columns[1:]]

# Create a choropleth map visualization
fig_carbon_choro = px.choropleth(data_carbon_choro,
                    locations="Country",
                    locationmode="country names",
                    color="CO2 Emissions",
                    animation_frame="Year",
                    range_color=[0, 1000],
                    title="Choropleth Map - Average Carbon Emissions by Country"
                   )

# Add the year selection dropdown to the map
fig_carbon_choro.update_layout(updatemenus=[{"type": "buttons",
                                "buttons": [{"label": "Play", "method": "animate", "args": [None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True, "transition": {"duration": 0}}]},
                                            {"label": "Pause", "method": "animate", "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}]}]}],
                  sliders=[{"active": 0, "steps": [{"label": str(year), "method": "animate", "args": [[year], {"frame": {"duration": 0, "redraw": True}, "transition": {"duration": 0}}]} for year in sorted(data_carbon_choro['Year'].unique())]}])

app = Dash(__name__,external_stylesheets =external_stylesheets)
styles = {
    'dropdown': {
        'width': '420px',
       ' padding-left':'20px',
        'display': 'inline-block',
        'font-size': '15px','border-color': '#2A547E','border-width': '2px',

    },
    'container': {
        'display': 'flex',
        'width': '420px',
        ' margin-left':'20px',
    }
}
app.layout = html.Div([
    html.Div(
        [   # Earth's image in the first line
    html.Img(src=f"data:image/jpg;base64,{encoded_image}", style={"height": "300px", "display": "block", "margin": "auto"}, ),

            html.H1("EARTH'S CLIMATE ANALYTICS", style={"text-align": "center","font-family":"PT Sans Narrow",'font-size': '45px' }),
            # Track changes in Earth's temperature, carbon emissions & Sea Levels over time in the third line
            html.H4("Track changes in Earth's temperature, Carbon Emissions & Sea Levels over time", style={"text-align": "center","font-family":"PT Sans Narrow",'font-size': '20px'}),
        ],
        style={"padding-top": "10px", 'padding-bottom': '10px',"background-color": "black", "color": "white", 'box-shadow': '5px 5px 5px grey',"border-radius": "15px",}
    ),
    dcc.Dropdown(
            id="demo-dropdown",
            options=[
                {"label": "Temperature", "value": "temperature"},
                {"label": "Carbon Emissions", "value": "carbon"},
                {"label": "Sea Levels", "value": "sea"},
                {"label": "Correlation", "value": "correlation"}
            ],
            value="",
            placeholder="Select the Desired Visulization",
        style={'width':'450px',"margin-top": "20px", 'margin-bottom': '20px','padding-left': '20px','font-size': '15px','border-color': '#2A547E','border-width': '2px' }
        ),
    html.Div(id='dd-output-container'),

],        style={"background-color": "#CDDEEE", "padding": "10px"}

)


@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    if value == 'temperature':
        return html.Div(
            children=[


                html.Div(
                    children=[
                        html.H1(children='Temperature Change Visualization (Celsius)',
                                style={'font-size': '36px', 'color': 'white'}),
                        html.P(children='This dashboard visualizes global Average Temperature level rise data ',
                               style={'font-size': '20px', 'color': 'white', 'margin-top': '0px'})
                    ],
                    style={'text-align': 'center', 'padding-top': '50px', "display": 'block', "font-family": "PT Sans Narrow"}
                ),
                html.Div(children=[
                    html.H1(
                        children='Monthly Average Temperature (1995-2020)',
                          style={            'font-family': 'Helvetica',
                                              'text-align': 'center',
                                              'margin-top': '20px',
                                              'font-weight': 'bold'        }    ),
                html.Div([
                    html.Div([
                        html.Label('Select a Country'),
                        dcc.Dropdown(id='country-dropdown',
                             options=[{'label': country, 'value': country} for country in sorted(fig_CC['Country'].unique())],
                                value=fig_CC['Country'].iloc[0],
                                style=styles['dropdown']
                            ),
                        ], style=styles['dropdown']),
                        html.Div([
                            html.Label('Select a City'),
                            dcc.Dropdown(id='city-dropdown',
                                options=[{'label': city, 'value': city} for city in sorted(fig_CC['City'].unique())],
                                value=fig_CC['City'].iloc[0],
                                style=styles['dropdown']
                            ),
                        ], style=styles['dropdown']),
                        html.Div([
                            html.Label('Select a Year'),
                            dcc.Dropdown( id='year-dropdown',
                                options=[{'label': year, 'value': year} for year in range(1995, 2021)],
                                value=fig_CC['Year'].iloc[0],
                                style=styles['dropdown']
                            ),
                        ], style=styles['dropdown']),
                    ], style=styles['container']),
                    dcc.Graph(
                        id='monthly-temperature',style={"margin": "10px",'border': '3px solid #2A547E','display': 'block', 'flex-wrap': 'wrap',}
                    ),
                ],),
                html.Div(
                    children=[

                         dcc.Graph(id="Choro", figure=fig_choro,style={"margin-bottom": "10px",'border': '3px solid #2A547E','width': '100%', 'height': '850px'}),
                        html.Div(
                            children=[
                                dcc.Graph(id="timeline", figure=fig_timeline,style={"margin-bottom": "10px",'border': '3px solid #2A547E',}),
                                dcc.Graph(id="Globe", figure=fig_globe,style={"margin-bottom": "10px",'border': '3px solid #2A547E',}),
                            ],
                            style={"display": "flex", "flex-direction": "row", "justify-content": "space-between", "width": "100%",},
                        ),

                        dcc.Graph(id="Heatmap", figure=fig_heat,style={"margin-bottom": "10px",'border': '3px solid #2A547E','width': '100%', 'height': '850px'}),

                        # Define options for the dropdown menu


                        html.Div([
                            dcc.Dropdown(
                                id='choro-dropdown',
                                options = [
                                    {'label': 'INDIA', 'value': 'fig11'},
                                    {'label': 'CHINA', 'value': 'fig21'},
                                    {'label': 'CANADA', 'value': 'fig31'},
                                    {'label': 'BRAZIL', 'value': 'fig41'},
                                    {'label': 'RUSSIA', 'value': 'fig51'},
                                    {'label': 'USA', 'value': 'fig61'}
                                ],
                                value='fig11',
                                style={'width':'450px',"margin-top": "20px", 'margin-bottom': '20px','padding-left': '20px','font-size': '15px','border-color': '#2A547E','border-width': '2px' }
                            ),
                        ]),

                        # Update the Choro graph based on the dropdown selection

                        dcc.Graph(id="choropleth-map11", figure=fig11,style={"margin-bottom": "10px",'border': '3px solid #2A547E',}),
                        dcc.Graph(id="lines", figure=fig_lines,style={"margin-bottom": "10px",'border': '3px solid #2A547E',}),
                        dcc.Graph(id="maxmin", figure=fig_maxmin,style={"margin-bottom": "10px",'border': '3px solid #2A547E',}),
                        dcc.Graph(id="diff", figure=fig_diff,style={"margin-bottom": "10px",'border': '3px solid #2A547E','flex-wrap': 'wrap',}),
                          ], style={ 'margin':'10px', 'display': 'block', 'flex-wrap': 'wrap', },
        )



        ],style={'background-color': '#4482C1'})
    elif value == 'carbon':
        return html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1(children='Carbon Emissions Visualization',
                                style={'font-size': '36px', 'color': 'white'}),
                        html.P(children='This dashboard visualizes Global Carbon Emissions Data over the years (MTCO2e)',
                               style={'font-size': '20px', 'color': 'white', 'margin-top': '0px'})
                    ],
                    style={'text-align': 'center', 'padding-top': '50px', "display": 'block', "font-family": "PT Sans Narrow"}
                ),
                html.Div([

                        html.Div([
                            html.Label("Select countries to display:"),
                            dcc.Dropdown(id="country-dropdown",
                                         options=[{"label": country, "value": country} for country in data_carbon_scatter["Country"].unique()],
                                         value=["United States", "China"],
                                         multi=True)
                        ], style={'width':'700px',"margin-top": "20px", 'margin-bottom': '20px','padding-left': '20px','font-size': '15px','border-color': '#2A547E','border-width': '2px' })
                    ]),

                dcc.Graph(id="carbon-emissions-scatterplot",style={"margin-bottom": "10px",'border': '3px solid #2A547E'}),
                html.H1(children='Top 10 Carbon Emitting Countries - Growth',
                                style={'font-size': '20px', 'color': 'white','padding-left':'10px'}),
                dcc.Graph(id='carbon-emissions-bar', figure=fig_race,style={"margin-bottom": "10px",'border': '3px solid #2A547E'}),
                dcc.Interval(
                    id='interval-component',
                    interval=600,  # 1 second in milliseconds
                    n_intervals=0
                ),
                html.Div(
                            children=[
                                dcc.Graph(id='carbon-emissions-top-5',figure=fig_top_5,style={"margin-bottom": "10px",'border': '3px solid #2A547E',}),
                                dcc.Graph(id='carbon-emissions-bottom-5',figure=fig_bottom_5,style={"margin-bottom": "10px",'border': '3px solid #2A547E'}),
                            ],
                            style={"display": "flex", "flex-direction": "row", "justify-content": "space-between", "width": "100%",},
                        ),
               dcc.Graph(id="carbon-bubble",figure=fig_bb,style={"margin-bottom": "10px",'border': '3px solid #2A547E'}),


                dcc.Graph(id='top-5-chart', figure=top_5_fig,style={"margin-bottom": "10px",'border': '3px solid #2A547E',}),
                dcc.Graph(id='bottom-5-chart', figure=bottom_5_fig,style={"margin-bottom": "10px",'border': '3px solid #2A547E',}),
                dcc.Graph(id='choropleth-carbon-emissions',figure=fig_carbon_choro,style={"margin-bottom": "10px",'border': '3px solid #2A547E','width': '100%', 'height': '850px'}),
                dcc.Graph(id='heatmap-carbon-emissions',figure=fig_heat_carbon,style={"margin-bottom": "10px",'border': '3px solid #2A547E','width': '100%', 'height': '850px'}),

            ],style={'background-color': '#4482C1'}
        )
    elif value == 'sea':
        return html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1(children='Sea Level Change',
                                style={'font-size': '36px', 'color': 'white'}),
                        html.P(children='This dashboard visualizes Global Sea Level rise data '
                                          'collected from tide gauges and satellites.',
                               style={'font-size': '20px', 'color': 'white', 'margin-top': '0px'})
                    ],
                    style={'text-align': 'center', 'padding-top': '50px', "display": 'block', "font-family": "PT Sans Narrow"}
                ),
                html.Div(
                    children=[
                        dcc.Graph(id='sea-level-bar', figure=fig_bar,style={"margin-bottom": "10px",'border': '3px solid #2A547E',}),
                        dcc.Graph(id='sea-level-scatter', figure=scatter_fig,style={"margin-bottom": "10px",'border': '3px solid #2A547E',}),
                        html.Div(
                            children=[
                                dcc.Graph(id='sea-level-box', figure=fig_box, style={"margin-bottom": "10px","margin-right": "5px", "width": "50%",'border': '3px solid #2A547E'}),
                                dcc.Graph(id='sea-level-area', figure=area_fig, style={"margin-bottom": "10px","margin-left": "5px", "width": "50%",'border': '3px solid #2A547E'}),
                            ],
                            style={"display": "flex", "flex-direction": "row", "justify-content": "space-between", "width": "100%",},
                        ),
                        dcc.Graph(id="line-chart", figure=fig_line,style={"margin-bottom": "10px",})
                    ],
                    style={ 'margin':'10px', 'display': 'block', 'flex-wrap': 'wrap', },
                    id='Sea-Levels'
                )
            ],
            style={'background-color': '#4482C1'},

        )
    elif value == 'correlation':
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

                        dcc.Graph(id='corr_line_temp', figure=fig_corr_temp,style={"margin-bottom": "10px",'border': '3px solid #2A547E'}),
                        dcc.Graph(id='corr_line', figure=fig_corr1,style={"margin-bottom": "10px",'border': '3px solid #2A547E',}),
                        dcc.Graph(id='corr_bar_em', figure=fig_emissions,style={"margin-bottom": "10px",'border': '3px solid #2A547E'}),

                        dcc.Graph(id='corr_line_1', figure=fig_corr3,style={"margin-bottom": "10px",'border': '3px solid #2A547E',}),
                        dcc.Graph(id='corr_scatter', figure=fig_corr2,style={"margin-bottom": "10px",'border': '3px solid #2A547E',}),

            ], style={ 'margin':'10px', 'display': 'block', 'flex-wrap': 'wrap', },
        )],style={'background-color': '#4482C1'})
    else:
        return html.Div()



@app.callback(Output("carbon-emissions-scatterplot", "figure"),
              [Input("country-dropdown", "value")])
def update_scatterplot(countries):
    filtered_data_carbon_scatter = data_carbon_scatter[data_carbon_scatter["Country"].isin(countries)]
    fig_carbon_scatter = px.scatter(filtered_data_carbon_scatter,title="Scatter Plot - Average Carbon Emissions by Country", x="Year", y="CO2 Emissions", color="Country", hover_data=["Country"])
    fig_carbon_scatter.update_layout(xaxis_title="Year",
                      yaxis_title="CO2 Emissions (MTCO2e) ",
                      font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"),
                      xaxis=dict(showgrid=False),
                      yaxis=dict(showgrid=False))
    return fig_carbon_scatter


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

# Define callback function to update figure with animation frames
@app.callback(Output('carbon-emissions-bar', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_carbon_emissions_bar(n):
    # Calculate next frame index
    frame_index = n % len(frames)
    current_year = top10_countries['Year'].unique()[frame_index]

    # Update the figure title with the current year
    fig_race.update_layout(title=f'Top 10 Carbon Emitting Countries - {current_year}'),
    # Return next frame
    return frames[frame_index]

@app.callback(
    dash.dependencies.Output('city-dropdown', 'options'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_cities_options(selected_country):
    filtered_fig_df = fig_CC[fig_CC['Country'] == selected_country]
    cities = filtered_fig_df['City'].unique()
    options = [{'label': city, 'value': city} for city in cities]
    return options


@app.callback(
    dash.dependencies.Output('monthly-temperature', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value'),
     dash.dependencies.Input('city-dropdown', 'value'),
     dash.dependencies.Input('year-dropdown', 'value')])
def update_figure(country, city, year):
    df_country_city_year = fig_CC[(fig_CC["Country"] == country) & (fig_CC["City"] == city) & (fig_CC["Year"] == year)]
    df_country_city_year = df_country_city_year[df_country_city_year["AverageTemperature"] != -99]
    df_country_city_year["AverageTemperature"] = (df_country_city_year["AverageTemperature"] - 32) / 1.8
    df_country_city_year["datetime"] = pd.to_datetime(df_country_city_year[["Year", "Month", "Day"]])
    df_country_city_year.set_index("datetime", inplace=True)

    fig = go.Figure(data=go.Heatmap(
        z=df_country_city_year["AverageTemperature"],
        x=df_country_city_year.index.day,
        y=df_country_city_year.index.month,
        colorscale='Jet',
        colorbar=dict(title="Temperature (°C)"),
        zmin=df_country_city_year["AverageTemperature"].min(),
        zmax=df_country_city_year["AverageTemperature"].max(),
        hovertemplate="Day: %{x}<br>Month: %{y}<br>Temperature: %{z:.2f}°C<extra></extra>",
    ))
    fig.update_layout(
        title=f"Monthly Average Temperature in {city}, {country} ({year})",
        xaxis=dict(title="Day"),
        yaxis=dict(title="Month"),
    )

    return fig


if __name__ == '__main__':
    app.run()





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



