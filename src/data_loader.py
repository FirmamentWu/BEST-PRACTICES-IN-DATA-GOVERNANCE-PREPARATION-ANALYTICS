"""
Data Loading Module
Handles loading and initial validation of EIA energy and CO2 data.

Authors: Alan (Xiangyu Wu), Zheng Congyun, He Yu, Ma Shuting
"""

import pandas as pd
from pathlib import Path
from typing import Tuple, Dict, Any


def load_raw_data(data_dir: str = "data/raw") -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load raw energy and CO2 data from EIA CSV files.

    Parameters
    ----------
    data_dir : str
        Path to directory containing raw data files

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame]
        Energy data and CO2 data DataFrames

    Example
    -------
    >>> energy_df, co2_df = load_raw_data("data/raw")
    """
    data_path = Path(data_dir)

    energy_df = pd.read_csv(data_path / "MER_T01_01.csv")
    co2_df = pd.read_csv(data_path / "MER_T11_01.csv")

    return energy_df, co2_df


def profile_data(df: pd.DataFrame, name: str = "Data") -> Dict[str, Any]:
    """
    Profile a DataFrame to identify data quality issues.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to profile
    name : str
        Name for logging purposes

    Returns
    -------
    Dict[str, Any]
        Dictionary containing profiling results
    """
    profile = {
        "name": name,
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "not_available_count": (df == "Not Available").sum().sum() if df.dtypes.apply(lambda x: x == object).any() else 0,
    }

    # Check for YYYYMM format
    if "YYYYMM" in df.columns:
        df_temp = df.copy()
        df_temp["YYYYMM"] = df_temp["YYYYMM"].astype(str)
        df_temp["MonthCode"] = df_temp["YYYYMM"].str[-2:]
        profile["month_codes"] = df_temp["MonthCode"].value_counts().to_dict()
        profile["has_mixed_granularity"] = len(df_temp["MonthCode"].unique()) > 1

    return profile


def get_available_variables(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get list of available variables (MSN codes) in the dataset.

    Parameters
    ----------
    df : pd.DataFrame
        EIA data with MSN column

    Returns
    -------
    pd.DataFrame
        DataFrame with MSN codes and descriptions
    """
    if "MSN" not in df.columns or "Description" not in df.columns:
        raise ValueError("DataFrame must contain 'MSN' and 'Description' columns")

    return df.groupby("MSN")["Description"].first().reset_index()


if __name__ == "__main__":
    # Test loading
    energy_df, co2_df = load_raw_data()
    print(f"Energy data: {energy_df.shape}")
    print(f"CO2 data: {co2_df.shape}")

    # Profile data
    energy_profile = profile_data(energy_df, "Energy")
    print(f"\nEnergy profile: {energy_profile}")
