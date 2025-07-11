import pandas as pd

def load_historical_emissions_data():
    data = pd.read_csv('dataset/historical_emissions.csv')
    data = data.melt(id_vars=["Country", "Data source", "Sector", "Gas", "Unit"],
                     var_name="Year",
                     value_name="CO2 Emissions")
    data['Year'] = pd.to_numeric(data['Year'])
    return data

def load_sorted_emissions_data():
    return pd.read_csv('dataset/sorted_data_with_lat_lon.csv')
