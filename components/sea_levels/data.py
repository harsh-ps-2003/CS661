import pandas as pd
import numpy as np
from datetime import datetime
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_sea_level_data():
    """Load and process sea level data with error handling."""
    try:
        logger.info("Loading sea level data...")
        data = pd.read_csv('dataset/Global_sea_level_rise.csv')
        data.rename(columns={
            'year': 'Year',
            'mmfrom1993-2008average': 'Sea Level'
        }, inplace=True)
        
        # Ensure data types
        data['Year'] = pd.to_numeric(data['Year'], errors='coerce')
        data['Sea Level'] = pd.to_numeric(data['Sea Level'], errors='coerce')
        
        # Drop any rows with NaN values
        data = data.dropna()
        logger.info(f"Successfully loaded sea level data with {len(data)} rows")
        return data
    except Exception as e:
        logger.error(f"Error loading sea level data: {e}")
        return pd.DataFrame(columns=['Year', 'Sea Level'])

def load_sea_ice_data():
    """Load and process sea ice data with robust error handling."""
    try:
        logger.info("Loading sea ice data...")
        # Manually define column names to handle whitespace issues
        col_names = ['Year', 'Month', 'Day', 'Extent', 'Missing', 'Source Data', 'hemisphere']
        # Use a more robust parser engine and specify names
        df = pd.read_csv('dataset/seaice.csv', header=0, names=col_names, skipinitialspace=True, engine='python', on_bad_lines='skip')

        logger.info(f"Successfully read seaice.csv, columns are: {df.columns.tolist()}")

        # Clean column names just in case
        df.columns = [col.strip() for col in df.columns]

        # Convert date from Year, Month, Day columns
        df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']].astype(int))
        
        # Extract additional date features
        df['DayOfYear'] = df['Date'].dt.dayofyear
        
        # Ensure Extent is numeric and handle any spaces
        df['Extent'] = pd.to_numeric(df['Extent'], errors='coerce')
        
        # Drop any rows with NaN values in critical columns
        df = df.dropna(subset=['Date', 'Extent'])
        
        logger.info(f"Successfully processed sea ice data with {len(df)} rows")
        return df
    except Exception as e:
        logger.error(f"Error loading sea ice data: {e}", exc_info=True)
        return pd.DataFrame(columns=['Date', 'Year', 'Month', 'DayOfYear', 'Extent'])

def calculate_seasonal_cycle(df):
    """Calculate seasonal cycle statistics by day of year."""
    try:
        if df.empty:
            logger.warning("Empty dataframe provided for seasonal cycle calculation")
            return pd.DataFrame(columns=['DayOfYear', 'Mean_Extent', 'Std_Extent', 'Min_Extent', 'Max_Extent'])
            
        seasonal_stats = df.groupby('DayOfYear').agg({
            'Extent': ['mean', 'std', 'min', 'max']
        }).round(3)
        
        seasonal_stats.columns = ['Mean_Extent', 'Std_Extent', 'Min_Extent', 'Max_Extent']
        seasonal_stats = seasonal_stats.reset_index()
        
        logger.info(f"Calculated seasonal cycle stats for {len(seasonal_stats)} days")
        return seasonal_stats
    except Exception as e:
        logger.error(f"Error calculating seasonal cycle: {e}")
        return pd.DataFrame(columns=['DayOfYear', 'Mean_Extent', 'Std_Extent', 'Min_Extent', 'Max_Extent'])

def calculate_monthly_trends(df):
    """Calculate monthly trends over time."""
    try:
        if df.empty:
            logger.warning("Empty dataframe provided for monthly trends calculation")
            return pd.DataFrame(), pd.DataFrame(columns=['Month', 'Trend'])
            
        monthly_avg = df.groupby(['Year', 'Month'])['Extent'].mean().reset_index()
        
        # Calculate trends for each month
        trends = []
        for month in range(1, 13):
            month_data = monthly_avg[monthly_avg['Month'] == month]
            
            if len(month_data) > 1:  # Need at least 2 points for trend
                # Simple linear regression
                X = month_data['Year'].values.reshape(-1, 1)
                y = month_data['Extent'].values
                
                # Calculate trend (slope)
                slope = np.polyfit(X.flatten(), y, 1)[0]
                
                trends.append({
                    'Month': month,
                    'Trend': slope
                })
        
        trends_df = pd.DataFrame(trends)
        logger.info(f"Calculated trends for {len(trends_df)} months")
        return monthly_avg, trends_df
    except Exception as e:
        logger.error(f"Error calculating monthly trends: {e}")
        return pd.DataFrame(), pd.DataFrame(columns=['Month', 'Trend'])
