"""
===============================================================================
TSN FRER Timing Stability Index (TSI) Calculation and Sensitivity Analysis
Author: Research Team
Description:
    Calculates the Timing Stability Index (TSI) = (P95 - P50) / P50
    for all 30 seeds (manual and automatic configurations).
    Performs sensitivity analysis by comparing TSI with:
    - Coefficient of Variation (CV) based on network jitter.
    - Extreme tail ratio (P99 / P50).
    - Descriptive statistics (min, max, mean, std).
    Outputs CSV files for further review.
===============================================================================
"""

import os
from pathlib import Path
import pandas as pd
import numpy as np

# ============================================================================
# Configuration
# ============================================================================
BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "../processed_results"
OUTPUT_DIR = BASE_DIR / "../processed_results"

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# File paths lookup logic
def resolve_file_path(base_path_str):
    csv_path = INPUT_DIR / f"{base_path_str}.csv"
    xlsx_path = INPUT_DIR / f"{base_path_str}.xlsx"
    if csv_path.exists():
        return csv_path
    elif xlsx_path.exists():
        return xlsx_path
    else:
        raise FileNotFoundError(f"Neither {csv_path.name} nor {xlsx_path.name} exists in {INPUT_DIR}")

MANUAL_FILE = resolve_file_path("manual_configuration_results")
AUTO_FILE = resolve_file_path("automatic_configuration_results")

TSI_PER_SEED_FILE = OUTPUT_DIR / "TSI_per_seed.csv"
TSI_SUMMARY_FILE = OUTPUT_DIR / "TSI_summary.csv"

# ============================================================================
# Helper Functions
# ============================================================================
def load_data(file_path):
    """Load data from CSV or Excel based on file extension."""
    if str(file_path).endswith('.csv'):
        return pd.read_csv(file_path)
    elif str(file_path).endswith('.xlsx'):
        return pd.read_excel(file_path, sheet_name=0)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")

def calculate_tsi_metrics(df, config_name):
    """
    Calculate TSI and related metrics for a given configuration DataFrame.
    """
    rename_map = {
        'Median (P50) (ms)': 'L50',
        '95th Percentile (P95) (ms)': 'L95',
        '99th Percentile (P99) (ms)': 'L99',
        'Network Jitter (StdDev) (ms)': 'Jitter',
        'Average Latency (ms)': 'Mean_Lat'
    }
    df_clean = df.rename(columns=rename_map)
    
    required_cols = ['Seed', 'L50', 'L95', 'L99', 'Jitter', 'Mean_Lat']
    missing = [col for col in required_cols if col not in df_clean.columns]
    if missing:
        print(f"Warning: Missing columns in {config_name}: {missing}")
        return pd.DataFrame()
    
    # Calculate Metrics with zero division protection
    df_clean['TSI'] = np.where(df_clean['L50'] != 0, (df_clean['L95'] - df_clean['L50']) / df_clean['L50'], np.nan)
    df_clean['Tail_Ratio_99'] = np.where(df_clean['L50'] != 0, df_clean['L99'] / df_clean['L50'], np.nan)
    df_clean['CV'] = np.where(df_clean['Mean_Lat'] != 0, df_clean['Jitter'] / df_clean['Mean_Lat'], np.nan)
    
    df_clean['Configuration'] = config_name
    
    return df_clean[['Seed', 'Configuration', 'L50', 'L95', 'L99', 'TSI', 'Tail_Ratio_99', 'CV']]

# ============================================================================
# Main Execution
# ============================================================================
def main():
    print("=" * 80)
    print(" TIMING STABILITY INDEX (TSI) CALCULATION & SENSITIVITY ANALYSIS ")
    print("=" * 80)

    try:
        manual_df = load_data(MANUAL_FILE)
        auto_df = load_data(AUTO_FILE)
    except Exception as e:
        print(f"ERROR: {e}")
        return

    print(f"\n[1] Loaded Manual Configuration: {len(manual_df)} seeds")
    print(f"[2] Loaded Automatic Configuration: {len(auto_df)} seeds")

    manual_tsi = calculate_tsi_metrics(manual_df, "Manual")
    auto_tsi = calculate_tsi_metrics(auto_df, "Automatic")

    combined_tsi = pd.concat([manual_tsi, auto_tsi], ignore_index=True)
    combined_tsi.to_csv(TSI_PER_SEED_FILE, index=False)
    print(f"\n[3] Per-seed TSI values saved to: {TSI_PER_SEED_FILE}")

    summary_list = []
    for config in ['Manual', 'Automatic']:
        subset = combined_tsi[combined_tsi['Configuration'] == config]
        for metric in ['TSI', 'Tail_Ratio_99', 'CV']:
            values = subset[metric].dropna()
            if len(values) > 0:
                summary_list.append({
                    'Configuration': config,
                    'Metric': metric,
                    'Mean': values.mean(),
                    'Std': values.std(ddof=1),
                    'Min': values.min(),
                    'Max': values.max(),
                    'Count': len(values)
                })

    summary_df = pd.DataFrame(summary_list)
    
    overall_tsi_manual = combined_tsi[combined_tsi['Configuration'] == 'Manual']['TSI'].mean()
    overall_tsi_auto = combined_tsi[combined_tsi['Configuration'] == 'Automatic']['TSI'].mean()
    
    print(f"\n[4] Overall Mean TSI (Manual): {overall_tsi_manual:.4f}")
    print(f"[5] Overall Mean TSI (Automatic): {overall_tsi_auto:.4f}")

    summary_df.to_csv(TSI_SUMMARY_FILE, index=False)
    print(f"\n[6] Sensitivity analysis summary saved to: {TSI_SUMMARY_FILE}")

    print("\n" + "-" * 80)
    print(" SENSITIVITY ANALYSIS SUMMARY ")
    print("-" * 80)
    print(summary_df.to_string(index=False))
    print("-" * 80)

    print("\n[SUCCESS] TSI Analysis Complete.")
    print("=" * 80)

if __name__ == "__main__":
    main()