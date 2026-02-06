#!/usr/bin/env python3
"""
CA6003 Energy and CO2 Analysis - Main Entry Point

Research Question: Does US energy structure change affect CO2 emission intensity?

Authors: Alan (Xiangyu Wu), Zheng Congyun, He Yu, Ma Shuting
Course: CA6003 - Best Practices in Data Governance, Preparation and Analytics
Institution: Nanyang Technological University (NTU)

Usage:
    python main.py [--output-dir OUTPUT_DIR]
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.data_loader import load_raw_data, profile_data
from src.data_preparation import prepare_full_dataset
from src.visualization import generate_all_figures, set_plot_style, plot_final_summary
from src.analysis import run_full_analysis, train_linear_regression


def print_header():
    """Print analysis header."""
    print("=" * 70)
    print("CA6003 ENERGY AND CO2 EMISSION INTENSITY ANALYSIS")
    print("=" * 70)
    print("Research Question: Does US energy structure change affect CO2 intensity?")
    print("Authors: Alan (Xiangyu Wu), Zheng Congyun, He Yu, Ma Shuting")
    print("Institution: Nanyang Technological University (NTU)")
    print("=" * 70)


def main(output_dir: str = "outputs"):
    """
    Run the complete analysis pipeline.

    Parameters
    ----------
    output_dir : str
        Directory for output files
    """
    print_header()

    # Create output directories
    output_path = Path(output_dir)
    figures_path = output_path / "figures"
    data_path = Path("data/processed")

    figures_path.mkdir(parents=True, exist_ok=True)
    data_path.mkdir(parents=True, exist_ok=True)

    # Step 1: Load Data
    print("\n[1/5] Loading raw data...")
    try:
        energy_df, co2_df = load_raw_data("data/raw")
        print(f"  Energy data: {energy_df.shape}")
        print(f"  CO2 data: {co2_df.shape}")
    except FileNotFoundError as e:
        print(f"  ERROR: Data files not found. Please ensure data/raw/ contains:")
        print("    - MER_T01_01.csv (Energy data)")
        print("    - MER_T11_01.csv (CO2 data)")
        return 1

    # Step 2: Profile Data
    print("\n[2/5] Profiling raw data...")
    energy_profile = profile_data(energy_df, "Energy")
    co2_profile = profile_data(co2_df, "CO2")
    print(f"  Energy data issues found: {energy_profile.get('not_available_count', 0)} 'Not Available' values")
    print(f"  CO2 data issues found: {co2_profile.get('not_available_count', 0)} 'Not Available' values")
    print(f"  Mixed granularity: {energy_profile.get('has_mixed_granularity', False)}")

    # Step 3: Prepare Data
    print("\n[3/5] Preparing data...")
    df = prepare_full_dataset(energy_df, co2_df)
    print(f"  Clean dataset: {df.shape[0]} years ({df['Year'].min()}-{df['Year'].max()})")

    # Save clean data
    clean_data_path = data_path / "clean_energy_co2_data.csv"
    df.to_csv(clean_data_path, index=False)
    print(f"  Saved: {clean_data_path}")

    # Step 4: Run Analysis
    print("\n[4/5] Running analysis...")
    results = run_full_analysis(df)

    print("\n" + "-" * 50)
    print("CORRELATION ANALYSIS")
    print("-" * 50)
    for var, corr_data in results["correlations"].items():
        sig = "***" if corr_data["p_value"] < 0.001 else "**" if corr_data["p_value"] < 0.01 else "*" if corr_data["p_value"] < 0.05 else ""
        print(f"  {var}: r = {corr_data['correlation']:+.3f} {sig}")

    print("\n" + "-" * 50)
    print("MODEL PERFORMANCE")
    print("-" * 50)
    print(f"  Full Data Linear Regression: R² = {results['full_model']['metrics']['r2']:.4f}")
    print(f"  Decision Tree: R² = {results['decision_tree']['metrics']['r2']:.4f}")
    print(f"  Time-Split Test: R² = {results['time_split']['r2']:.4f}")

    if results["time_split"]["structural_break"]:
        print("\n  ** STRUCTURAL BREAK DETECTED **")
        print(f"  Training mean: {results['time_split']['train_mean']:.2f}")
        print(f"  Test mean: {results['time_split']['test_mean']:.2f}")
        print("  CO2 intensity declined faster than model predicted after 2014")

    print("\n" + "-" * 50)
    print("MODEL INTERPRETATION")
    print("-" * 50)
    for var, coef in results["full_model"]["coefficients"].items():
        print(f"  1% increase in {var} -> {coef:+.3f} change in CO2 Intensity")

    # Step 5: Generate Visualizations
    print("\n[5/5] Generating visualizations...")
    set_plot_style()
    generate_all_figures(df, str(figures_path))

    # Generate final summary figure
    X = df[["FossilShare", "RenewableShare"]]
    y = df["CO2Intensity"]
    model, y_pred, _ = train_linear_regression(X, y)
    plot_final_summary(df, y_pred, results["full_model"]["metrics"]["r2"],
                       str(figures_path / "fig12_final_summary.png"))
    print("  fig12_final_summary.png")

    # Print summary
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print(f"\nKey Results:")
    print(f"  - Analysis Period: 1973-2024 ({len(df)} years)")
    print(f"  - Fossil Share Change: {df['FossilShare'].iloc[0]:.1f}% -> {df['FossilShare'].iloc[-1]:.1f}%")
    print(f"  - Renewable Share Change: {df['RenewableShare'].iloc[0]:.1f}% -> {df['RenewableShare'].iloc[-1]:.1f}%")
    print(f"  - CO2 Intensity Change: {((df['CO2Intensity'].iloc[-1] / df['CO2Intensity'].iloc[0]) - 1) * 100:.1f}%")
    print(f"  - Model R²: {results['full_model']['metrics']['r2']:.4f}")

    print(f"\nOutput Files:")
    print(f"  - Clean data: {clean_data_path}")
    print(f"  - Figures: {figures_path}/fig*.png")

    print("\n" + "=" * 70)
    print("Research Answer: YES - Energy structure significantly affects CO2 intensity")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CA6003 Energy and CO2 Analysis"
    )
    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Directory for output files (default: outputs)"
    )

    args = parser.parse_args()
    sys.exit(main(args.output_dir))
