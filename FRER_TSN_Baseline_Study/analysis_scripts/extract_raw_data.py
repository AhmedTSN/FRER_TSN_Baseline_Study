"""
===============================================================================
TSN FRER Raw Data Extraction Script
Author: Research Team
Description:
    Parses OMNeT++ scalar output files (.sca) for all 30 seed runs
    (manual and automatic configurations) and extracts key performance metrics
    into structured CSV files for further statistical analysis.
===============================================================================
"""

import os
import re
import pandas as pd
import glob

# ============================================================================
# Configuration
# ============================================================================
# Adjust these paths according to your local directory structure
RAW_RESULTS_DIR = "../raw_results/"
OUTPUT_DIR = "../processed_results/"

AUTO_DIR = os.path.join(RAW_RESULTS_DIR, "automatic")
MANUAL_DIR = os.path.join(RAW_RESULTS_DIR, "manual")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# List of scalar names to extract (as they appear in .sca files)
SCALAR_NAMES = [
    "Total Generated Packets",
    "Unique Received Packets",
    "Apparent Delivery Ratio",
    "Actual Delivery Ratio",
    "Dropped at s2a",
    "Dropped at s2b",
    "Dropped at Destination",
    "Total Duplicates",
    "Average Latency (ms)",
    "Median (P50) (ms)",
    "95th Percentile (P95) (ms)",
    "99th Percentile (P99) (ms)",
    "Network Jitter (StdDev) (ms)",
    "Packet Jitter (Jitter) (ns)",
    "Timing Stability Index"
]

# ============================================================================
# Helper Functions
# ============================================================================
def parse_scalar_file(file_path):
    """
    Parse a single .sca file and extract scalar values.
    Returns a dictionary with scalar name -> value.
    """
    scalars = {}
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            # Look for lines like: scalar "name" value
            match = re.search(r'scalar\s+"([^"]+)"\s+([\d\.Ee+-]+)', line)
            if match:
                name = match.group(1)
                value = float(match.group(2))
                scalars[name] = value
    return scalars

def process_configuration(config_dir, config_name):
    """
    Process all .sca files in a given directory (one per seed).
    Returns a DataFrame with one row per seed.
    """
    sca_files = glob.glob(os.path.join(config_dir, "*.sca"))
    if not sca_files:
        print(f"Warning: No .sca files found in {config_dir}")
        return pd.DataFrame()

    # Sort to ensure seeds are in order (seed-0, seed-1, ...)
    sca_files.sort()

    all_data = []
    for file_path in sca_files:
        scalars = parse_scalar_file(file_path)
        # Extract only the metrics we need
        row = {}
        for metric in SCALAR_NAMES:
            row[metric] = scalars.get(metric, float('nan'))
        all_data.append(row)

    df = pd.DataFrame(all_data)
    # Add a Seed column (0 to N-1)
    df.insert(0, 'Seed', range(len(df)))
    return df

# ============================================================================
# Main Execution
# ============================================================================
def main():
    print("=" * 80)
    print(" RAW DATA EXTRACTION FOR TSN FRER SIMULATIONS ")
    print("=" * 80)

    # Process automatic configuration
    print("\n[1] Processing Automatic Configuration...")
    auto_df = process_configuration(AUTO_DIR, "automatic")
    if not auto_df.empty:
        auto_output = os.path.join(OUTPUT_DIR, "automatic_configuration_results.csv")
        auto_df.to_csv(auto_output, index=False)
        print(f"    → Saved {len(auto_df)} seeds to: {auto_output}")
    else:
        print("    → No data found for automatic configuration.")

    # Process manual configuration
    print("\n[2] Processing Manual Configuration...")
    manual_df = process_configuration(MANUAL_DIR, "manual")
    if not manual_df.empty:
        manual_output = os.path.join(OUTPUT_DIR, "manual_configuration_results.csv")
        manual_df.to_csv(manual_output, index=False)
        print(f"    → Saved {len(manual_df)} seeds to: {manual_output}")
    else:
        print("    → No data found for manual configuration.")

    print("\n[SUCCESS] Data extraction complete. Processed results are in:", OUTPUT_DIR)
    print("=" * 80)

if __name__ == "__main__":
    main()