"""
Data Preparation Module
Handles cleaning, transformation, and feature engineering for EIA data.

Authors: Alan (Xiangyu Wu), Zheng Congyun, He Yu, Ma Shuting
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional


# Variable mappings for EIA data
ENERGY_VARIABLES = {
    "TETCBUS": "TotalEnergy",      # Total Primary Energy Consumption
    "FFTCBUS": "FossilEnergy",     # Total Fossil Fuels Consumption
    "RETCBUS": "RenewableEnergy",  # Total Renewable Energy Consumption
    "NUETBUS": "NuclearEnergy"     # Nuclear Electric Power Consumption
}

CO2_VARIABLES = {
    "TETCEUS": "TotalCO2"          # Total Energy CO2 Emissions
}


def filter_annual_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter EIA data to annual records only (month code = 13).

    In EIA Monthly Energy Review format:
    - YYYYMM ending in 01-12 = monthly data
    - YYYYMM ending in 13 = annual total

    Parameters
    ----------
    df : pd.DataFrame
        Raw EIA data

    Returns
    -------
    pd.DataFrame
        Filtered annual data with Year column
    """
    df_clean = df.copy()

    # Convert YYYYMM to string for parsing
    df_clean["YYYYMM"] = df_clean["YYYYMM"].astype(str)

    # Extract year and month code
    df_clean["Year"] = df_clean["YYYYMM"].str[:4].astype(int)
    df_clean["MonthCode"] = df_clean["YYYYMM"].str[-2:]

    # Filter to annual data only
    df_annual = df_clean[df_clean["MonthCode"] == "13"].copy()

    # Drop temporary columns
    df_annual = df_annual.drop(["YYYYMM", "MonthCode"], axis=1)

    if "Column_Order" in df_annual.columns:
        df_annual = df_annual.drop("Column_Order", axis=1)

    return df_annual


def convert_to_numeric(df: pd.DataFrame, column: str = "Value") -> pd.DataFrame:
    """
    Convert string values to numeric, handling 'Not Available' strings.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with string values
    column : str
        Column name to convert

    Returns
    -------
    pd.DataFrame
        DataFrame with numeric values (NaN for non-numeric)
    """
    df_clean = df.copy()
    df_clean[column] = pd.to_numeric(df_clean[column], errors="coerce")
    return df_clean


def pivot_to_wide_format(
    df: pd.DataFrame,
    variable_mapping: Dict[str, str],
    index_col: str = "Year",
    msn_col: str = "MSN",
    value_col: str = "Value"
) -> pd.DataFrame:
    """
    Pivot EIA long-format data to wide format with renamed columns.

    Parameters
    ----------
    df : pd.DataFrame
        Long-format EIA data
    variable_mapping : Dict[str, str]
        Mapping from MSN codes to column names
    index_col : str
        Column to use as index
    msn_col : str
        Column containing MSN codes
    value_col : str
        Column containing values

    Returns
    -------
    pd.DataFrame
        Wide-format DataFrame with renamed columns
    """
    # Filter to required variables
    df_filtered = df[df[msn_col].isin(variable_mapping.keys())]

    # Pivot to wide format
    df_pivot = df_filtered.pivot_table(
        index=index_col,
        columns=msn_col,
        values=value_col,
        aggfunc="first"
    ).reset_index()

    # Rename columns
    df_pivot = df_pivot.rename(columns=variable_mapping)

    return df_pivot


def calculate_energy_shares(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate energy source shares as percentage of total.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with TotalEnergy, FossilEnergy, RenewableEnergy, NuclearEnergy

    Returns
    -------
    pd.DataFrame
        DataFrame with added share columns
    """
    df_result = df.copy()

    required_cols = ["TotalEnergy", "FossilEnergy", "RenewableEnergy", "NuclearEnergy"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    df_result["FossilShare"] = (df_result["FossilEnergy"] / df_result["TotalEnergy"]) * 100
    df_result["RenewableShare"] = (df_result["RenewableEnergy"] / df_result["TotalEnergy"]) * 100
    df_result["NuclearShare"] = (df_result["NuclearEnergy"] / df_result["TotalEnergy"]) * 100

    return df_result


def calculate_co2_intensity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate CO2 emission intensity (CO2 per unit energy).

    CO2 Intensity = Total CO2 Emissions / Total Energy Consumption
    Units: Million Metric Tons CO2 / Quadrillion BTU

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with TotalCO2 and TotalEnergy columns

    Returns
    -------
    pd.DataFrame
        DataFrame with added CO2Intensity column
    """
    df_result = df.copy()

    if "TotalCO2" not in df.columns or "TotalEnergy" not in df.columns:
        raise ValueError("Missing required columns: TotalCO2 and/or TotalEnergy")

    df_result["CO2Intensity"] = df_result["TotalCO2"] / df_result["TotalEnergy"]

    return df_result


def prepare_full_dataset(
    energy_df: pd.DataFrame,
    co2_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Complete data preparation pipeline: clean, merge, and engineer features.

    Parameters
    ----------
    energy_df : pd.DataFrame
        Raw energy data from EIA
    co2_df : pd.DataFrame
        Raw CO2 data from EIA

    Returns
    -------
    pd.DataFrame
        Clean, merged dataset with engineered features
    """
    # Process energy data
    energy_annual = filter_annual_data(energy_df)
    energy_annual = convert_to_numeric(energy_annual)
    energy_pivot = pivot_to_wide_format(energy_annual, ENERGY_VARIABLES)

    # Process CO2 data
    co2_annual = filter_annual_data(co2_df)
    co2_annual = convert_to_numeric(co2_annual)
    co2_pivot = pivot_to_wide_format(co2_annual, CO2_VARIABLES)

    # Merge on Year
    df = pd.merge(energy_pivot, co2_pivot, on="Year", how="inner")

    # Feature engineering
    df = calculate_energy_shares(df)
    df = calculate_co2_intensity(df)

    return df


if __name__ == "__main__":
    from data_loader import load_raw_data

    # Load and prepare data
    energy_df, co2_df = load_raw_data()
    df = prepare_full_dataset(energy_df, co2_df)

    print(f"Prepared dataset: {df.shape}")
    print(f"Year range: {df['Year'].min()} - {df['Year'].max()}")
    print(f"\nColumns: {df.columns.tolist()}")
