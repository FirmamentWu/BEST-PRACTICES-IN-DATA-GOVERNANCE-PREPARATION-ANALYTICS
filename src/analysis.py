"""
Analysis Module
Statistical analysis and machine learning models.

Authors: Alan (Xiangyu Wu), Zheng Congyun, He Yu, Ma Shuting
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple, Any


def calculate_correlations(
    df: pd.DataFrame,
    target: str,
    predictors: List[str]
) -> Dict[str, Dict[str, float]]:
    """
    Calculate Pearson correlations between predictors and target.

    Parameters
    ----------
    df : pd.DataFrame
        Data to analyze
    target : str
        Target variable name
    predictors : List[str]
        List of predictor variable names

    Returns
    -------
    Dict[str, Dict[str, float]]
        Dictionary with correlation coefficient and p-value for each predictor
    """
    results = {}

    for var in predictors:
        r, p_value = stats.pearsonr(df[var], df[target])
        results[var] = {
            "correlation": r,
            "p_value": p_value,
            "significant": p_value < 0.05
        }

    return results


def check_multicollinearity(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Check for multicollinearity among predictor variables.

    Parameters
    ----------
    df : pd.DataFrame
        Data to analyze
    columns : List[str]
        Columns to check

    Returns
    -------
    pd.DataFrame
        Correlation matrix
    """
    return df[columns].corr()


def check_autocorrelation(series: pd.Series, lag: int = 1) -> float:
    """
    Calculate lag autocorrelation for time series.

    Parameters
    ----------
    series : pd.Series
        Time series data
    lag : int
        Lag to calculate

    Returns
    -------
    float
        Autocorrelation coefficient
    """
    return series.autocorr(lag=lag)


def train_linear_regression(
    X: pd.DataFrame,
    y: pd.Series,
    scale: bool = False
) -> Tuple[LinearRegression, np.ndarray, Dict[str, float]]:
    """
    Train a linear regression model.

    Parameters
    ----------
    X : pd.DataFrame
        Feature matrix
    y : pd.Series
        Target variable
    scale : bool
        Whether to scale features

    Returns
    -------
    Tuple[LinearRegression, np.ndarray, Dict[str, float]]
        Model, predictions, and metrics
    """
    if scale:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
    else:
        X_scaled = X.values

    model = LinearRegression()
    model.fit(X_scaled, y)
    y_pred = model.predict(X_scaled)

    metrics = {
        "r2": r2_score(y, y_pred),
        "rmse": np.sqrt(mean_squared_error(y, y_pred)),
        "mae": mean_absolute_error(y, y_pred)
    }

    return model, y_pred, metrics


def train_decision_tree(
    X: pd.DataFrame,
    y: pd.Series,
    max_depth: int = 4
) -> Tuple[DecisionTreeRegressor, np.ndarray, Dict[str, float]]:
    """
    Train a decision tree regressor.

    Parameters
    ----------
    X : pd.DataFrame
        Feature matrix
    y : pd.Series
        Target variable
    max_depth : int
        Maximum tree depth

    Returns
    -------
    Tuple[DecisionTreeRegressor, np.ndarray, Dict[str, float]]
        Model, predictions, and metrics
    """
    model = DecisionTreeRegressor(max_depth=max_depth, random_state=42)
    model.fit(X, y)
    y_pred = model.predict(X)

    metrics = {
        "r2": r2_score(y, y_pred),
        "rmse": np.sqrt(mean_squared_error(y, y_pred)),
        "mae": mean_absolute_error(y, y_pred)
    }

    return model, y_pred, metrics


def evaluate_time_split(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2
) -> Dict[str, Any]:
    """
    Evaluate model with time-based train/test split.

    Parameters
    ----------
    X : pd.DataFrame
        Feature matrix
    y : pd.Series
        Target variable
    test_size : float
        Proportion of data for testing

    Returns
    -------
    Dict[str, Any]
        Split information and metrics
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, shuffle=False, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    results = {
        "train_size": len(X_train),
        "test_size": len(X_test),
        "train_mean": y_train.mean(),
        "test_mean": y_test.mean(),
        "r2": r2_score(y_test, y_pred),
        "rmse": np.sqrt(mean_squared_error(y_test, y_pred)),
        "structural_break": y_train.mean() - y_test.mean() > 5  # Significant difference
    }

    return results


def run_full_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Run complete analysis pipeline.

    Parameters
    ----------
    df : pd.DataFrame
        Prepared dataset

    Returns
    -------
    Dict[str, Any]
        Complete analysis results
    """
    features = ["FossilShare", "RenewableShare"]
    target = "CO2Intensity"

    X = df[features]
    y = df[target]

    results = {}

    # Correlation analysis
    results["correlations"] = calculate_correlations(
        df, target, ["FossilShare", "RenewableShare", "NuclearShare"]
    )

    # Check multicollinearity
    results["multicollinearity"] = check_multicollinearity(
        df, ["FossilShare", "RenewableShare", "NuclearShare"]
    ).to_dict()

    # Full data model
    model, y_pred, metrics = train_linear_regression(X, y)
    results["full_model"] = {
        "metrics": metrics,
        "coefficients": dict(zip(features, model.coef_)),
        "intercept": model.intercept_
    }

    # Decision tree
    dt_model, dt_pred, dt_metrics = train_decision_tree(X, y)
    results["decision_tree"] = {
        "metrics": dt_metrics,
        "feature_importance": dict(zip(features, dt_model.feature_importances_))
    }

    # Time-based split evaluation
    results["time_split"] = evaluate_time_split(X, y)

    return results


if __name__ == "__main__":
    from data_loader import load_raw_data
    from data_preparation import prepare_full_dataset

    # Load and prepare data
    energy_df, co2_df = load_raw_data()
    df = prepare_full_dataset(energy_df, co2_df)

    # Run analysis
    results = run_full_analysis(df)

    print("Analysis Results:")
    print(f"  Full Model R²: {results['full_model']['metrics']['r2']:.4f}")
    print(f"  Decision Tree R²: {results['decision_tree']['metrics']['r2']:.4f}")
    print(f"  Time Split R²: {results['time_split']['r2']:.4f}")
    print(f"  Structural Break Detected: {results['time_split']['structural_break']}")
