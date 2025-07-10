import pandas as pd
import numpy as np

# --- Remove duplicates and inconsistent rows ---
def clean_dataframe(df):
    df = df.drop_duplicates()
    df = df.dropna(thresh=int(0.7 * df.shape[1]))
    return df

# --- Detect and mark outliers using Interquartile Range (IQR) ---
def detect_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df['outlier'] = ((df[column] < lower) | (df[column] > upper))
    return df

# --- Apply log transformation to reduce skewness in numeric data ---
def log_transform_column(df, column):
    df[column] = df[column].replace(0, np.nanmin(df[column][df[column] > 0]) / 10)
    df[column] = np.log(df[column])
    return df

# --- Convert categorical columns to numeric using one-hot encoding ---
def convert_categorical_to_numeric(df):
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    df = pd.get_dummies(df, columns=cat_cols, drop_first=True)
    return df

# --- Load and process multiple climate-related datasets ---
def process_all_datasets():
    # Earth Surface Temperature
    temp_df = pd.read_csv("GlobalTemperatures.csv")
    temp_df = clean_dataframe(temp_df)
    temp_df = detect_outliers_iqr(temp_df, "LandAverageTemperature")
    temp_df = log_transform_column(temp_df, "LandAverageTemperature")

    # Climate Insights
    insights_df = pd.read_csv("climate_insights.csv")
    insights_df = clean_dataframe(insights_df)
    insights_df = detect_outliers_iqr(insights_df, "Temperature")
    insights_df = log_transform_column(insights_df, "Temperature")

    # Greenhouse Gas Emissions
    ghg_df = pd.read_csv("greenhouse_gas_emissions.csv")
    ghg_df = clean_dataframe(ghg_df)
    ghg_df = detect_outliers_iqr(ghg_df, "CO2")
    ghg_df = log_transform_column(ghg_df, "CO2")

    # Sea Level Data
    sea_df = pd.read_csv("global_sea_level.csv")
    sea_df = clean_dataframe(sea_df)
    sea_df = detect_outliers_iqr(sea_df, "GMSL")
    sea_df = log_transform_column(sea_df, "GMSL")

    # Crop Production
    crop_df = pd.read_csv("crop_production.csv")
    crop_df = clean_dataframe(crop_df)
    crop_df = detect_outliers_iqr(crop_df, "Value")
    crop_df = log_transform_column(crop_df, "Value")

    # Deforestation
    forest_df = pd.read_csv("deforestation.csv")
    forest_df = clean_dataframe(forest_df)
    forest_df = detect_outliers_iqr(forest_df, "ForestAreaPct")
    forest_df = log_transform_column(forest_df, "ForestAreaPct")

    # Sea Ice Extent
    ice_df = pd.read_csv("sea_ice_extent.csv")
    ice_df = clean_dataframe(ice_df)
    ice_df = detect_outliers_iqr(ice_df, "extent")
    ice_df = log_transform_column(ice_df, "extent")


    temp_df = convert_categorical_to_numeric(temp_df)
    insights_df = convert_categorical_to_numeric(insights_df)
    ghg_df = convert_categorical_to_numeric(ghg_df)
    crop_df = convert_categorical_to_numeric(crop_df)
    forest_df = convert_categorical_to_numeric(forest_df)

    return {
        'temperature': temp_df,
        'insights': insights_df,
        'ghg': ghg_df,
        'sea_level': sea_df,
        'crop': crop_df,
        'forest': forest_df,
        'ice': ice_df
    }

