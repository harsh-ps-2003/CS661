import pandas as pd
import numpy as np

def load_deforestation_data():
    """Load and preprocess deforestation data."""
    df = pd.read_csv('dataset/deforestation.csv')
    
    # Calculate absolute forest loss (negative values mean deforestation)
    df['Forest_Loss'] = df['forests_2020'] - df['forests_2000']
    
    # Create a clean dataset for time series (2000 and 2020 points)
    time_series_data = []
    for _, row in df.iterrows():
        # 2000 data point
        time_series_data.append({
            'Year': 2000,
            'Forest_Cover': row['forests_2000'],
            'Country': row['iso3c']
        })
        # 2020 data point
        time_series_data.append({
            'Year': 2020,
            'Forest_Cover': row['forests_2020'],
            'Country': row['iso3c']
        })
    
    time_series_df = pd.DataFrame(time_series_data)
    
    # Group countries into regions (simplified for visualization)
    region_mapping = {
        'BRA': 'South America', 'COL': 'South America', 'PER': 'South America', 'VEN': 'South America',
        'USA': 'North America', 'CAN': 'North America', 'MEX': 'North America',
        'CHN': 'Asia', 'IND': 'Asia', 'IDN': 'Asia', 'MYS': 'Asia', 'JPN': 'Asia',
        'RUS': 'Europe', 'DEU': 'Europe', 'FRA': 'Europe', 'GBR': 'Europe',
        'AUS': 'Oceania', 'NZL': 'Oceania',
        'NGA': 'Africa', 'COD': 'Africa', 'ZAF': 'Africa', 'KEN': 'Africa'
    }
    
    # Add region to both dataframes
    df['Region'] = df['iso3c'].map(region_mapping)
    time_series_df['Region'] = time_series_df['Country'].map(region_mapping)
    
    # Filter out rows where Region is None (was previously 'Other')
    df = df[df['Region'].notna()]
    time_series_df = time_series_df[time_series_df['Region'].notna()]
    
    return df, time_series_df

def calculate_regional_stats(df):
    """Calculate regional deforestation statistics."""
    # Group by region and calculate statistics
    regional_stats = df.groupby('Region').agg({
        'Forest_Loss': ['sum', 'mean', 'std'],
        'forests_2020': 'mean'  # Current forest cover
    }).round(2)
    
    # Flatten column names
    regional_stats.columns = ['Total_Loss', 'Average_Loss', 'Loss_Std', 'Current_Forest_Cover']
    regional_stats = regional_stats.reset_index()
    
    # Sort by Total_Loss
    regional_stats = regional_stats.sort_values('Total_Loss', ascending=True)
    
    return regional_stats

def get_top_countries(df, n=10):
    """Get top N countries with most forest loss/gain."""
    df_sorted = df.sort_values('Forest_Loss')
    
    # Get top N losses and gains
    top_losses = df_sorted.head(n)
    top_gains = df_sorted.tail(n)
    
    # Combine and sort by Forest_Loss
    top_changes = pd.concat([top_losses, top_gains])
    top_changes = top_changes.sort_values('Forest_Loss')
    
    return top_changes 