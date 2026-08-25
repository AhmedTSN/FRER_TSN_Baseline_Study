# Decoupling Reliability from Timing Stability: An Empirical and Analytical Baseline Study of IEEE 802.1CB FRER in Time-Sensitive Networking


This repository contains the complete simulation models, configuration files, control experiments, raw data, processing scripts, and figure-generation code for the paper:

> **"Decoupling Reliability from Timing Stability: An Empirical and Analytical Baseline Study of IEEE 802.1CB FRER in Time-Sensitive Networking"**  
> *Ahmed M. Mohammed, Emad H. Al-Hemiary*  
> *Submitted to the International Journal of Intelligent Engineering and Systems (IJIES)*

---

## Repository Overview

This artifact provides a **fully reproducible baseline** for IEEE 802.1CB Frame Replication and Elimination for Reliability (FRER) in Time-Sensitive Networking (TSN). It compares **manual** (expert-driven) and **automatic** (orchestrated) FRER configurations under identical topologies, traffic loads, and sequential link-failure scenarios.

To address specific reviewer requests, this repository also includes:

- A **10.2‑second extended simulation** for `Seed 0` to verify the 100% effective Packet Delivery Ratio (PDR).
- A **100‑byte packet control experiment** for `Seed 0` to isolate intrinsic FRER timing jitter from link‑saturation effects.
- All **30 random seeds** (0–29) used for both manual and automatic configurations.
- **Python analysis scripts** for statistical tests (t-test, Mann-Whitney, TOST, Cohen’s d), TSI calculation, and figure generation.

---

## Repository Structure
FRER_TSN_Baseline_Study/
│
├── README.md # This file
├── requirements.txt # Python dependencies for analysis scripts
├── gitignore
├── LICENSE
├── automatic_configuration/ # Automatic FRER (StreamRedundancyConfigurator)
│ ├── automatic_configuration.ned
│ └── automatic_configuration.ini
│ └── automatic_configuration.anf
├── manual_configuration/ # Manual FRER (explicit forwarding/elimination rules)
│ ├── manual_configuration.ned
│ └── manual_configuration.ini
│ └── manual_configuration.anf
├── additional_control_experiments/ # Reviewer-requested control experiments
│ ├── 10.2s_extension_seed0/
│ │ └── omnetpp_seed0_10.2s.ini
│ └── 100byte_packets_seed0/
│ └── omnetpp_seed0_100B.ini
│
├── analysis_scripts/ # Python scripts for data extraction & analysis
│ ├── requirements.txt
│ ├── extract_raw_data.py
│ ├── statistical_analysis.py
│ ├── calculate_TSI.py
│ └── generate_figures.py
│
├── raw_results/ # Raw OMNeT++ output (.sca / .vec) – compressed
│ ├── automatic/ # 30 seeds (0–29)
│ ├── manual/ # 30 seeds (0–29)
│ └── additional_control/ # 10.2s and 100B experiments
│
├── processed_results/ # Summarised data (xlsx) derived from raw results
│ ├── automatic_configuration_results.xlsx
│ ├── automatic_packet_life_time_histogram.xlsx
│ ├── manual_configuration_results.xlsx
│ └── manual_packet_life_time_histogram.xlsx
│ └── manual_packet_life_time_histogram.xlsx
│ └── autoFRER-10.2s-seed0-results.xlsx
│
├── figures/ # Publication‑ready figures (300 dpi)
│ ├── Figure1_topology_landscape.png
│ ├── Figure2_delay_evolution.png
│ ├── Figure3_distribution_analysis.png
│ ├── Figure4_ECDF.png
│ ├── Figure5_jitter_analysis.png
│ └── Figure6_ECDF_comparison.png

## Raw Data Access

Due to their large size (~1.5 GB per configuration, ~6 GB total), the raw OMNeT++ simulation output files (`.sca` and `.vec`) for all 60 independent runs (30 automatic + 30 manual) are **not hosted directly on this GitHub repository**.

Instead, the complete raw dataset is publicly available for download via **Google Drive** at the following link:

🔗 **[Download Raw Simulation Results (Google Drive)](https://drive.google.com/drive/folders/1-os-AjQrKS5Xzm81GCaEWFZj3KN42Rlj?usp=drive_link)**

The archive contains the following:
- **`automatic/`**: 30 `.sca` and `.vec` files (Seeds 0–29) for the automatic FRER configuration.
- **`manual/`**: 30 `.sca` and `.vec` files (Seeds 0–29) for the manual FRER configuration.
- **`additional_control/`**: Raw outputs from the reviewer-requested control experiments (10.2s extension for Seed 0, and 100-byte packet experiment for Seed 0).

These files are essential for full reproducibility. To process them, use the provided Python scripts in the `analysis_scripts/` folder, or import them directly into the OMNeT++ IDE Analysis Tool.

> **Note for Reviewers**: The Google Drive link is publicly accessible and does not require any sign-in or special permissions.

---

## Requirements

### Software
- **OMNeT++** 6.2.0 (or later)
- **INET Framework** 4.4.0 (methodology follows the official INET 4.6 documentation)
- **Python** 3.8+ (for analysis scripts)

### Python Dependencies (see `analysis_scripts/requirements.txt`)
- `numpy`
- `pandas`
- `matplotlib`
- `seaborn`
- `scipy`

---

## Setup and Installation

### 1. Install OMNeT++ and INET
Follow the official OMNeT++ installation guide. To install the exact INET version used in this work, you can use `opp_env`:

```bash
opp_env install --init -w inet-workspace --build-modes=release inet-4.4.0
cd inet-workspace
opp_env shell
Alternatively, import the INET project manually into the OMNeT++ IDE.

2. Clone this Repository
bash
git clone https://github.com/yourusername/FRER_TSN_Baseline_Study.git
cd FRER_TSN_Baseline_Study
3. Import into OMNeT++ IDE
Open the OMNeT++ IDE.

Import this project as an existing project.

Ensure the INET project is also imported and referenced.

4. Install Python Dependencies
bash
pip install -r analysis_scripts/requirements.txt
Reproducing the Experiments
Main Experiments (Manual & Automatic, 30 Seeds)
Each configuration uses seed-set = 0 to 29. To run a single seed:

Open the respective .ini file (automatic_configuration/automatic_configuration.ini or manual_configuration/manual_configuration.ini).

Set seed-set = <0..29>.

Run the simulation.

To run all 30 seeds sequentially, you can use a batch script or modify the .ini file with a loop.

Control Experiments (Reviewer-Requested)
10.2‑second extension: Located in additional_control_experiments/10.2s_extension_seed0/. Run omnetpp_seed0_10.2s.ini with seed-set = 0.

100‑byte packet experiment: Located in additional_control_experiments/100byte_packets_seed0/. Run omnetpp_seed0_100B.ini with seed-set = 0.

Reproducing the Analysis and Figures
All analysis scripts are in the analysis_scripts/ folder. Execute them in the following order:

bash
cd analysis_scripts

# 1. Extract raw .sca/.vec files into structured CSV tables
python extract_raw_data.py

# 2. Perform statistical tests (t-test, Mann-Whitney, TOST, Cohen's d)
python statistical_analysis.py

# 3. Calculate the Timing Stability Index (TSI) for all runs and sensitivity analysis
python calculate_TSI.py

# 4. Generate all publication‑ready figures (Figure 1 – Figure 6)
python generate_figures.py
The generated figures will be saved in the figures/ directory, and the processed results (CSV files) will be saved in processed_results/.

Citing This Work
If you use this repository or its contents in your research, please cite the associated paper:

bibtex
@article{mohammed2026frer,
  title={Decoupling Reliability from Timing Stability: An Empirical and Analytical Baseline Study of IEEE 802.1CB FRER in Time-Sensitive Networking},
  author={Mohammed, Ahmed M. and Al-Hemiary, Emad H.},
  journal={International Journal of Intelligent Engineering and Systems},
  year={2026},
  note={Under review}
}
License
This project is released under the MIT License to encourage reproducibility and reuse. See the LICENSE file for details.

Contact
For questions, issues, or collaboration opportunities, please contact the corresponding author:

Ahmed M. Mohammed
College of Information Engineering, Al-Nahrain University, Baghdad, Iraq
Email: ahmed.mit23@ced.nahrainuniv.edu.iq