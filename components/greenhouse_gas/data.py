import pandas as pd
import re
from functools import lru_cache

DATA_PATH = 'dataset/greenhouse_gas_inventory_data_data.csv'

_GAS_MAP_PATTERNS = {
    'CO2': r'carbon_dioxide',
    'CH4': r'methane',
    'N2O': r'nitrous_oxide',
    'HFCs': r'hydrofluorocarbons',
    'PFCs': r'perfluorocarbons',
    'SF6': r'sulphur_hexafluoride',
    'NF3': r'nitrogen_trifluoride',
    'GHG_Total': r'greenhouse_gas_ghgs',
}


def _infer_gas(category: str) -> str:
    for gas, pattern in _GAS_MAP_PATTERNS.items():
        if re.search(pattern, category):
            return gas
    return 'Other'


@lru_cache(maxsize=1)
def load_clean_data() -> pd.DataFrame:
    """Load and tidy the raw greenhouse-gas inventory CSV.

    Returns a DataFrame with columns:
        Country, Year, Gas, Value
    """
    df = pd.read_csv(DATA_PATH)
    # Standardise column names
    df = df.rename(columns={
        'country_or_area': 'Country',
        'year': 'Year',
        'value': 'Value',
        'category': 'Category',
    })
    # Infer gas type from category text
    df['Gas'] = df['Category'].apply(_infer_gas)
    # Keep only recognised gases (drop Other)
    df = df[df['Gas'] != 'Other']
    # Ensure numeric types and drop NA
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    df = df.dropna(subset=['Country', 'Year', 'Gas', 'Value'])
    return df


def available_gases():
    """Return sorted list of distinct gas names."""
    return sorted(load_clean_data()['Gas'].unique())


def latest_year() -> int:
    return int(load_clean_data()['Year'].max())


def top_emitters(gas: str, year: int, n: int = 10):
    """Return top N emitting countries for a given gas and year."""
    df = load_clean_data()
    subset = (
        df[(df['Gas'] == gas) & (df['Year'] == year)]
        .sort_values('Value', ascending=False)
        .head(n)
    )
    return subset[['Country', 'Value']] 