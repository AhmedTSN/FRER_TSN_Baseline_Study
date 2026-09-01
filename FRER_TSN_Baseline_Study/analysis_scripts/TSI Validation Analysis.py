"""
TSI Validation Analysis
=======================

Purpose:
    Validate the added value of the Timing Stability Index (TSI)
    against robust dispersion measures and a deadline-oriented metric.

Metrics:
    - TSI
    - IQR / Median
    - MAD / Median
    - Deadline Violation Ratio (DVR)

Conditions:
    - Seed 0  : Moderate condition
    - Seed 19 : Severely skewed condition

Input:
    automatic_packet_life_time_histogram.xlsx

Output:
    tsi_validation_table.csv

Method:
    Quantiles and MAD are estimated from grouped histogram data
    using linear interpolation within histogram bins.
"""

import pandas as pd
from pathlib import Path


# ============================================================
# USER CONFIGURATION
# ============================================================

INPUT_FILE = Path(
    "automatic_packet_life_time_histogram.xlsx"
)

OUTPUT_FILE = Path(
    "tsi_validation_table.csv"
)

DEADLINE_MS = 5.0

# TSI values from the 30-seed simulation results
TSI_VALUES = {
    0: 1.793,   # Seed 0 (Moderate)
    19: 5.396,  # Seed 19 (Severely Skewed)
}


# ============================================================
# HISTOGRAM LOADING (MODIFIED FOR THE ACTUAL EXCEL FORMAT)
# ============================================================

def load_histogram(file_path, seed_number):
    """
    Load histogram data for a specific seed from
    automatic_packet_life_time_histogram.xlsx.

    The Excel file contains columns:
        Seed, BinStart_ms, BinEnd_ms, Count

    Returns a list of dictionaries:
        [{'lower': float, 'upper': float, 'count': float}, ...]
    """

    df = pd.read_excel(file_path)

    # Filter rows for the specified seed
    seed_df = df[df['Seed'] == seed_number]

    if seed_df.empty:
        raise ValueError(
            f"No data found for Seed = {seed_number}.\n"
            f"Available seeds: {df['Seed'].unique().tolist()}"
        )

    histogram = []

    for _, row in seed_df.iterrows():
        lower = float(row['BinStart_ms'])
        upper = float(row['BinEnd_ms'])
        count = float(row['Count'])

        # Skip empty bins
        if count <= 0:
            continue

        histogram.append({
            "lower": lower,
            "upper": upper,
            "count": count
        })

    # Ensure bins are sorted by lower bound
    histogram.sort(key=lambda x: x["lower"])

    if not histogram:
        raise ValueError(
            f"No valid bins found for Seed = {seed_number}."
        )

    return histogram


# ============================================================
# TOTAL NUMBER OF OBSERVATIONS
# ============================================================

def total_count(histogram):
    return sum(item["count"] for item in histogram)


# ============================================================
# QUANTILE FROM HISTOGRAM (LINEAR INTERPOLATION WITHIN BIN)
# ============================================================

def histogram_quantile(histogram, q):
    """
    Estimate a quantile from grouped histogram data
    using linear interpolation within the containing bin.
    """

    if not 0 <= q <= 1:
        raise ValueError("q must be between 0 and 1.")

    N = total_count(histogram)
    target = q * N

    cumulative = 0.0

    for item in histogram:
        count = item["count"]
        next_cumulative = cumulative + count

        if target <= next_cumulative:
            if count == 0:
                return item["lower"]

            fraction = (target - cumulative) / count

            return (
                item["lower"]
                + fraction * (item["upper"] - item["lower"])
            )

        cumulative = next_cumulative

    # Target is beyond the last bin (should not happen for q <= 1)
    return histogram[-1]["upper"]


# ============================================================
# IQR
# ============================================================

def calculate_iqr(histogram):
    p25 = histogram_quantile(histogram, 0.25)
    p75 = histogram_quantile(histogram, 0.75)
    iqr = p75 - p25
    return p25, p75, iqr


# ============================================================
# MAD (Median Absolute Deviation)
# ============================================================

def calculate_mad(histogram, median):
    """
    Estimate Median Absolute Deviation (MAD):

        MAD = median(|X - median|)

    using the grouped histogram distribution.
    """

    deviation_histogram = []

    for item in histogram:
        lower = item["lower"]
        upper = item["upper"]
        count = item["count"]

        # Bin entirely below median
        if upper <= median:
            dev_lower = abs(upper - median)
            dev_upper = abs(lower - median)

        # Bin entirely above median
        elif lower >= median:
            dev_lower = abs(lower - median)
            dev_upper = abs(upper - median)

        # Bin crosses the median
        else:
            dev_lower = 0.0
            dev_upper = max(abs(lower - median), abs(upper - median))

        deviation_histogram.append({
            "lower": dev_lower,
            "upper": dev_upper,
            "count": count
        })

    deviation_histogram.sort(key=lambda x: x["lower"])

    mad = histogram_quantile(deviation_histogram, 0.50)

    return mad


# ============================================================
# DVR (Deadline Violation Ratio)
# ============================================================

def calculate_dvr(histogram, deadline_ms):
    """
    Calculate Deadline Violation Ratio.

        DVR = N(X >= D) / N * 100

    If the deadline falls inside a histogram bin,
    linear interpolation assuming uniform distribution
    inside the bin is used.
    """

    N = total_count(histogram)
    violations = 0.0

    for item in histogram:
        lower = item["lower"]
        upper = item["upper"]
        count = item["count"]

        # Entire bin is at or above deadline
        if lower >= deadline_ms:
            violations += count

        # Entire bin is below deadline
        elif upper <= deadline_ms:
            continue

        # Deadline lies inside the bin
        else:
            fraction_above = (upper - deadline_ms) / (upper - lower)
            violations += count * fraction_above

    dvr = (violations / N) * 100

    return violations, dvr


# ============================================================
# ALL VALIDATION METRICS
# ============================================================

def calculate_metrics(histogram, tsi, deadline_ms):

    N = total_count(histogram)

    # Median (P50)
    median = histogram_quantile(histogram, 0.50)

    # IQR
    p25, p75, iqr = calculate_iqr(histogram)
    iqr_norm = iqr / median

    # MAD
    mad = calculate_mad(histogram, median)
    mad_norm = mad / median

    # DVR
    violations, dvr = calculate_dvr(histogram, deadline_ms)

    return {
        "N": N,
        "P25_ms": p25,
        "Median_ms": median,
        "P75_ms": p75,
        "IQR_ms": iqr,
        "IQR_Median": iqr_norm,
        "MAD_ms": mad,
        "MAD_Median": mad_norm,
        "Deadline_Violations": violations,
        "DVR_percent": dvr,
        "TSI": tsi,
    }


# ============================================================
# PERCENTAGE CHANGE
# ============================================================

def percent_change(old_value, new_value):
    return ((new_value - old_value) / old_value) * 100


# ============================================================
# MAIN ANALYSIS
# ============================================================

def main():

    print("=" * 70)
    print("TSI VALIDATION ANALYSIS")
    print("=" * 70)

    print(f"\nInput file: {INPUT_FILE.resolve()}")
    print(f"Deadline: {DEADLINE_MS} ms")

    # --------------------------------------------------------
    # Load histograms for Seed 0 and Seed 19
    # --------------------------------------------------------

    hist_seed0 = load_histogram(INPUT_FILE, 0)
    hist_seed19 = load_histogram(INPUT_FILE, 19)

    print(f"\nSeed 0: {total_count(hist_seed0):,.0f} observations")
    print(f"Seed 19: {total_count(hist_seed19):,.0f} observations")

    # --------------------------------------------------------
    # Calculate metrics
    # --------------------------------------------------------

    seed0 = calculate_metrics(
        hist_seed0,
        TSI_VALUES[0],
        DEADLINE_MS
    )

    seed19 = calculate_metrics(
        hist_seed19,
        TSI_VALUES[19],
        DEADLINE_MS
    )

    # ========================================================
    # PRINT DETAILED RESULTS
    # ========================================================

    for name, result in [
        ("Seed 0 (Moderate)", seed0),
        ("Seed 19 (Severely Skewed)", seed19)
    ]:
        print("\n" + "-" * 70)
        print(name)
        print("-" * 70)
        print(f"N              : {result['N']:,.0f}")
        print(f"P25            : {result['P25_ms']:.5f} ms")
        print(f"Median (P50)   : {result['Median_ms']:.5f} ms")
        print(f"P75            : {result['P75_ms']:.5f} ms")
        print(f"IQR            : {result['IQR_ms']:.5f} ms")
        print(f"IQR / Median   : {result['IQR_Median']:.3f}")
        print(f"MAD            : {result['MAD_ms']:.5f} ms")
        print(f"MAD / Median   : {result['MAD_Median']:.3f}")
        print(f"DVR            : {result['DVR_percent']:.2f}%")
        print(f"TSI            : {result['TSI']:.3f}")

    # ========================================================
    # PERCENTAGE CHANGES
    # ========================================================

    tsi_change = percent_change(seed0["TSI"], seed19["TSI"])
    iqr_change = percent_change(seed0["IQR_Median"], seed19["IQR_Median"])
    mad_change = percent_change(seed0["MAD_Median"], seed19["MAD_Median"])
    dvr_change = percent_change(seed0["DVR_percent"], seed19["DVR_percent"])

    # ========================================================
    # FINAL TABLE (EXACTLY AS IN THE MANUSCRIPT)
    # ========================================================

    final_table = pd.DataFrame({

        "Metric": [
            "TSI",
            "IQR / Median",
            "MAD / Median",
            "DVR (D=5 ms)"
        ],

        "Seed 0 (Moderate)": [
            seed0["TSI"],
            seed0["IQR_Median"],
            seed0["MAD_Median"],
            seed0["DVR_percent"]
        ],

        "Seed 19 (Severely Skewed)": [
            seed19["TSI"],
            seed19["IQR_Median"],
            seed19["MAD_Median"],
            seed19["DVR_percent"]
        ],

        "Change (%)": [
            tsi_change,
            iqr_change,
            mad_change,
            dvr_change
        ]
    })

    print("\n")
    print("=" * 70)
    print("FINAL TABLE FOR MANUSCRIPT")
    print("=" * 70)

    print(
        final_table.to_string(
            index=False,
            formatters={
                "Seed 0 (Moderate)": lambda x: f"{x:.3f}",
                "Seed 19 (Severely Skewed)": lambda x: f"{x:.3f}",
                "Change (%)": lambda x: f"{x:+.1f}%"
            }
        )
    )

    # ========================================================
    # SAVE CSV
    # ========================================================

    final_table.to_csv(OUTPUT_FILE, index=False)

    print(f"\nResults saved to: {OUTPUT_FILE.resolve()}")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()