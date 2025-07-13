import pandas as pd
from functools import lru_cache

@lru_cache(maxsize=1)
def load_air_quality_data():
    """Load, clean, and cache the air quality dataset."""
    try:
        df = pd.read_csv('dataset/global_air_quality_data_10000.csv')
        # Standardize column names
        df.columns = [col.lower().replace(' ', '_').replace('.', '') for col in df.columns]
        df['date'] = pd.to_datetime(df['date'])
    except FileNotFoundError:
        print("Error: The file 'dataset/global_air_quality_data_10000.csv' was not found.")
        return pd.DataFrame()
    except Exception as e:
        print(f"An error occurred while loading the data: {e}")
        return pd.DataFrame()
    return df

def get_countries():
    """Return a sorted list of unique countries."""
    df = load_air_quality_data()
    return sorted(df['country'].unique())

def get_cities(country):
    """Return a sorted list of unique cities for a given country."""
    df = load_air_quality_data()
    return sorted(df[df['country'] == country]['city'].unique())

def get_metrics():
    """Return a list of metrics available for visualization, excluding temperature."""
    return ['pm25', 'pm10', 'no2', 'so2', 'co', 'o3', 'humidity', 'wind_speed'] 