"""
Visualization Module
Creates all charts and figures for the analysis.

Authors: Alan (Xiangyu Wu), Zheng Congyun, He Yu, Ma Shuting
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path
from typing import Optional, List, Tuple


def set_plot_style():
    """Set consistent plot style for all visualizations."""
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams["figure.figsize"] = (12, 6)
    plt.rcParams["font.size"] = 11
    plt.rcParams["axes.titlesize"] = 14
    plt.rcParams["axes.labelsize"] = 12


def plot_energy_structure(
    df: pd.DataFrame,
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Create stacked area chart showing energy structure evolution.

    Parameters
    ----------
    df : pd.DataFrame
        Data with Year, FossilShare, NuclearShare, RenewableShare
    save_path : Optional[str]
        Path to save figure

    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(14, 7))

    ax.stackplot(
        df["Year"],
        df["FossilShare"],
        df["NuclearShare"],
        df["RenewableShare"],
        labels=["Fossil Fuels", "Nuclear", "Renewable"],
        colors=["#d62728", "#ff7f0e", "#2ca02c"],
        alpha=0.8
    )

    ax.set_xlabel("Year")
    ax.set_ylabel("Share of Total Energy (%)")
    ax.set_title("US Energy Structure Evolution (1973-2024)", fontweight="bold")
    ax.legend(loc="upper right")
    ax.set_xlim(df["Year"].min(), df["Year"].max())
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig


def plot_co2_intensity_trend(
    df: pd.DataFrame,
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Create dual-axis chart showing CO2 intensity and fossil share trends.

    Parameters
    ----------
    df : pd.DataFrame
        Data with Year, CO2Intensity, FossilShare
    save_path : Optional[str]
        Path to save figure

    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # CO2 Intensity on primary axis
    color1 = "#1f77b4"
    ax1.plot(df["Year"], df["CO2Intensity"], color=color1, linewidth=2.5, label="CO2 Intensity")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("CO2 Intensity (MMT CO2 / Quad BTU)", color=color1)
    ax1.tick_params(axis="y", labelcolor=color1)

    # Add trend line
    z = np.polyfit(df["Year"], df["CO2Intensity"], 1)
    p = np.poly1d(z)
    ax1.plot(df["Year"], p(df["Year"]), "--", color=color1, alpha=0.7, label="Trend")

    # Fossil share on secondary axis
    ax2 = ax1.twinx()
    color2 = "#d62728"
    ax2.plot(df["Year"], df["FossilShare"], color=color2, linewidth=2, linestyle=":", label="Fossil Share")
    ax2.set_ylabel("Fossil Fuel Share (%)", color=color2)
    ax2.tick_params(axis="y", labelcolor=color2)

    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

    ax1.set_title("CO2 Intensity vs Fossil Fuel Share (1973-2024)", fontweight="bold")
    ax1.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig


def plot_correlation_matrix(
    df: pd.DataFrame,
    columns: List[str],
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Create correlation matrix heatmap.

    Parameters
    ----------
    df : pd.DataFrame
        Data to analyze
    columns : List[str]
        Columns to include in correlation matrix
    save_path : Optional[str]
        Path to save figure

    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    corr_matrix = df[columns].corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

    sns.heatmap(
        corr_matrix,
        mask=mask,
        annot=True,
        fmt=".3f",
        cmap="RdBu_r",
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8}
    )

    ax.set_title("Correlation Matrix: Energy Structure and CO2 Intensity", fontweight="bold")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig


def plot_scatter_with_regression(
    df: pd.DataFrame,
    x_cols: List[str],
    y_col: str,
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Create scatter plots with regression lines.

    Parameters
    ----------
    df : pd.DataFrame
        Data to plot
    x_cols : List[str]
        X-axis columns
    y_col : str
        Y-axis column
    save_path : Optional[str]
        Path to save figure

    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    fig, axes = plt.subplots(1, len(x_cols), figsize=(5 * len(x_cols), 5))

    colors = ["#d62728", "#2ca02c", "#ff7f0e"]
    titles = ["Fossil Fuel Share", "Renewable Energy Share", "Nuclear Energy Share"]

    for i, (col, color, title) in enumerate(zip(x_cols, colors, titles)):
        ax = axes[i] if len(x_cols) > 1 else axes

        # Scatter plot
        ax.scatter(df[col], df[y_col], c=color, alpha=0.6, s=50)

        # Regression line
        z = np.polyfit(df[col], df[y_col], 1)
        p = np.poly1d(z)
        x_line = np.linspace(df[col].min(), df[col].max(), 100)
        ax.plot(x_line, p(x_line), "--", color="black", linewidth=2)

        # Correlation
        r, _ = stats.pearsonr(df[col], df[y_col])

        ax.set_xlabel(f"{title} (%)")
        ax.set_ylabel("CO2 Intensity")
        ax.set_title(f"{title} vs CO2 Intensity\nr = {r:.3f}", fontweight="bold")
        ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig


def plot_distributions(
    df: pd.DataFrame,
    columns: List[str],
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Create distribution plots with histograms and KDE.

    Parameters
    ----------
    df : pd.DataFrame
        Data to plot
    columns : List[str]
        Columns to plot
    save_path : Optional[str]
        Path to save figure

    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    n_cols = len(columns)
    n_rows = (n_cols + 1) // 2

    fig, axes = plt.subplots(n_rows, 2, figsize=(12, 5 * n_rows))
    axes = axes.flatten()

    colors = ["#1f77b4", "#d62728", "#2ca02c", "#ff7f0e"]

    for i, (col, color) in enumerate(zip(columns, colors)):
        ax = axes[i]

        ax.hist(df[col], bins=15, color=color, alpha=0.7, edgecolor="black", density=True)
        df[col].plot(kind="kde", ax=ax, color="black", linewidth=2)

        mean = df[col].mean()
        skew = df[col].skew()

        ax.axvline(mean, color="red", linestyle="--", linewidth=2, label=f"Mean: {mean:.2f}")
        ax.set_xlabel(col)
        ax.set_ylabel("Density")
        ax.set_title(f"{col} Distribution\nSkewness: {skew:.3f}", fontweight="bold")
        ax.legend()

    # Hide unused axes
    for i in range(len(columns), len(axes)):
        axes[i].set_visible(False)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig


def plot_final_summary(
    df: pd.DataFrame,
    y_pred: np.ndarray,
    r2: float,
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Create final summary plot with actual vs predicted and structural break.

    Parameters
    ----------
    df : pd.DataFrame
        Data with Year and CO2Intensity
    y_pred : np.ndarray
        Model predictions
    r2 : float
        R-squared score
    save_path : Optional[str]
        Path to save figure

    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(14, 7))

    ax.plot(df["Year"], df["CO2Intensity"], "b-", linewidth=2.5, marker="o", markersize=4, label="Actual CO2 Intensity")
    ax.plot(df["Year"], y_pred, "g--", linewidth=2, label=f"Model Prediction (R²={r2:.3f})")

    # Highlight structural break period
    ax.axvspan(2014, 2024, alpha=0.2, color="yellow", label="Accelerated Decline Period")
    ax.axvline(2014, color="orange", linestyle=":", linewidth=2)

    ax.set_xlabel("Year")
    ax.set_ylabel("CO2 Intensity (MMT CO2 / Quad BTU)")
    ax.set_title("US CO2 Emission Intensity: 52-Year Trend Analysis (1973-2024)", fontweight="bold")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)
    ax.set_xlim(1973, 2024)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig


def generate_all_figures(df: pd.DataFrame, output_dir: str = "outputs/figures"):
    """
    Generate all figures for the analysis.

    Parameters
    ----------
    df : pd.DataFrame
        Prepared dataset
    output_dir : str
        Directory to save figures
    """
    set_plot_style()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("Generating visualizations...")

    # Fig 1: Energy Structure
    plot_energy_structure(df, output_path / "fig1_energy_structure.png")
    print("  fig1_energy_structure.png")

    # Fig 2: CO2 Intensity Trend
    plot_co2_intensity_trend(df, output_path / "fig2_co2_intensity_trend.png")
    print("  fig2_co2_intensity_trend.png")

    # Fig 4: Correlation Matrix
    corr_cols = ["CO2Intensity", "FossilShare", "RenewableShare", "NuclearShare", "TotalEnergy", "TotalCO2"]
    plot_correlation_matrix(df, corr_cols, output_path / "fig4_correlation_matrix.png")
    print("  fig4_correlation_matrix.png")

    # Fig 5: Scatter plots
    plot_scatter_with_regression(df, ["FossilShare", "RenewableShare", "NuclearShare"], "CO2Intensity",
                                  output_path / "fig5_scatter_shares_vs_intensity.png")
    print("  fig5_scatter_shares_vs_intensity.png")

    # Fig 6: Distributions
    plot_distributions(df, ["CO2Intensity", "FossilShare", "RenewableShare", "NuclearShare"],
                       output_path / "fig6_distributions.png")
    print("  fig6_distributions.png")

    plt.close("all")
    print("All visualizations generated!")


if __name__ == "__main__":
    from data_loader import load_raw_data
    from data_preparation import prepare_full_dataset

    # Load and prepare data
    energy_df, co2_df = load_raw_data()
    df = prepare_full_dataset(energy_df, co2_df)

    # Generate figures
    generate_all_figures(df)
