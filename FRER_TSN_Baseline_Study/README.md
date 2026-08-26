# Decoupling Reliability from Timing Stability: An Empirical and Analytical Baseline Study of IEEE 802.1CB FRER in Time-Sensitive Networking

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22116011.svg)](https://doi.org/10.5281/zenodo.22116011)

This repository contains the simulation models, configuration files, reviewer-requested control experiments, analysis scripts, processed results, and publication-ready figures associated with the following manuscript:

> **"Decoupling Reliability from Timing Stability: An Empirical and Analytical Baseline Study of IEEE 802.1CB FRER in Time-Sensitive Networking"**
> *Ahmed M. Mohammed, Emad H. Al-Hemiary*
> *Submitted to the International Journal of Intelligent Engineering and Systems (IJIES)*

---

## Reproducibility Archive

This repository provides the reproducibility materials associated with the study and is archived on Zenodo as version **v1.1**.

**Zenodo DOI:**
https://doi.org/10.5281/zenodo.22116011

**GitHub Release:**
https://github.com/AhmedTSN/FRER_TSN_Baseline_Study/releases/tag/v1.1

The archived release contains the simulation source code, configuration files, reviewer-requested control experiments, analysis scripts, processed results, and publication-ready figures required to reproduce and verify the reported methodology and analyses.

The complete raw OMNeT++ simulation outputs are provided separately through a public Google Drive archive because of their large storage requirements.

---

## Citation

### Citing the Reproducibility Archive

If you use the simulation code, processed data, analysis scripts, or other materials from this repository, please cite the archived reproducibility package:

> Mohammed, A. M., & Al-Hemiary, E. H. (2026). *FRER_TSN_Baseline_Study: Reproducibility Archive v1.1*. Zenodo. https://doi.org/10.5281/zenodo.22116011

### Citing the Associated Paper

If you use or discuss the scientific findings reported in the associated manuscript, please cite the paper:

```bibtex
@article{mohammed2026frer,
  title={Decoupling Reliability from Timing Stability: An Empirical and Analytical Baseline Study of IEEE 802.1CB FRER in Time-Sensitive Networking},
  author={Mohammed, Ahmed M. and Al-Hemiary, Emad H.},
  journal={International Journal of Intelligent Engineering and Systems},
  year={2026},
  note={Under review}
}
```

---

## Repository Overview

This artifact provides a **fully reproducible baseline** for IEEE 802.1CB Frame Replication and Elimination for Reliability (FRER) in Time-Sensitive Networking (TSN).

The study compares **manual (expert-driven)** and **automatic (orchestrated)** FRER configurations under identical network topologies, traffic conditions, and sequential link-failure scenarios.

The repository was prepared to support independent verification of the experimental methodology, simulation configuration, statistical analysis, and reported figures.

### Included Materials

The GitHub repository contains:

* Manual FRER simulation models and configuration files.
* Automatic FRER simulation models and configuration files.
* Reviewer-requested control experiments.
* Python scripts for data extraction and statistical analysis.
* Processed experimental results.
* Timing Stability Index (TSI) calculation and sensitivity-analysis scripts.
* Publication-ready figures.
* Environment and dependency information required to reproduce the analysis.

### Reviewer-Requested Validation Experiments

To address specific reproducibility and validation requirements, the repository includes:

* A **10.2-second extended simulation for Seed 0** to verify the 100% effective Packet Delivery Ratio (PDR).
* A **100-byte packet control experiment for Seed 0** to isolate intrinsic FRER timing jitter from link-saturation effects.
* Configuration files covering all **30 independent random seeds (0–29)** used for both manual and automatic FRER configurations.
* Python analysis scripts for:

  * t-test
  * Mann-Whitney U test
  * TOST equivalence testing
  * Cohen's d effect size
  * Timing Stability Index (TSI) calculation
  * Sensitivity analysis
  * Figure generation

---

## Repository Structure

```text
FRER_TSN_Baseline_Study/
│
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
│
├── automatic_configuration/
│   ├── automatic_configuration.ned
│   ├── automatic_configuration.ini
│   └── automatic_configuration.anf
│
├── manual_configuration/
│   ├── manual_configuration.ned
│   ├── manual_configuration.ini
│   └── manual_configuration.anf
│
├── additional_control_experiments/
│   ├── 10.2s_extension_seed0/
│   │   └── omnetpp_seed0_10.2s.ini
│   │
│   └── 100byte_packets_seed0/
│       └── omnetpp_seed0_100B.ini
│
├── analysis_scripts/
│   ├── requirements.txt
│   ├── extract_raw_data.py
│   ├── statistical_analysis.py
│   ├── calculate_TSI.py
│   └── generate_figures.py
│
├── processed_results/
│   ├── automatic_configuration_results.xlsx
│   ├── automatic_packet_life_time_histogram.xlsx
│   ├── manual_configuration_results.xlsx
│   ├── manual_packet_life_time_histogram.xlsx
│   └── autoFRER-10.2s-seed0-results.xlsx
│   └── autoFRER-100b-seed0-results.xlsx
└── figures/
    ├── Figure1_topology_landscape.png
    ├── Figure2_delay_evolution.png
    ├── Figure3_distribution_analysis.png
    ├── Figure4_ECDF.png
    ├── Figure5_jitter_analysis.png
    └── Figure6_ECDF_comparison.png
```

> **Important:** The `raw_results/` directory is intentionally not included in this GitHub repository because the complete raw OMNeT++ output files are several gigabytes in size. The raw simulation data are provided through the public Google Drive archive described below.

---

## Raw Simulation Data

The complete raw OMNeT++ simulation outputs are **not hosted directly on GitHub** because of their large size.

The complete raw dataset is publicly available through the following Google Drive archive:

**Download Raw Simulation Results:**
https://drive.google.com/drive/folders/1-os-AjQrKS5Xzm81GCaEWFZj3KN42Rlj?usp=drive_link

### Contents of the Raw Data Archive

The archive contains the raw `.sca` and `.vec` output files generated by the OMNeT++ simulations:

```text
raw_results/
│
├── automatic/
│   ├── Seed 0
│   ├── Seed 1
│   ├── ...
│   └── Seed 29
│
├── manual/
│   ├── Seed 0
│   ├── Seed 1
│   ├── ...
│   └── Seed 29
│
└── additional_control/
    ├── 10.2-second extension — Seed 0
    └── 100-byte packet experiment — Seed 0
```

The archive therefore contains the raw outputs from:

* **30 automatic FRER runs (Seeds 0–29)**
* **30 manual FRER runs (Seeds 0–29)**
* **Reviewer-requested control experiments**

The raw simulation outputs can be processed using the Python scripts provided in the `analysis_scripts/` directory.

They can also be inspected directly using the OMNeT++ IDE Analysis Tool.

> **Note for Reviewers:** The Google Drive archive is publicly accessible and does not require sign-in or special permissions.

---

## Requirements

### Simulation Environment

* **OMNeT++:** 6.2.0 or later
* **INET Framework:** 4.4.0
* **Python:** 3.8 or later

The experiments reported in the manuscript were conducted using **OMNeT++ 6.2.0 and INET 4.4.0**.

### Python Dependencies

The analysis scripts require:

* `numpy`
* `pandas`
* `matplotlib`
* `seaborn`
* `scipy`

The required dependencies are listed in:

```text
analysis_scripts/requirements.txt
```

---

# Setup and Installation

## 1. Install OMNeT++ and INET

Install **OMNeT++ 6.2.0** or a compatible later version.

The exact INET version used for the reported experiments is **INET 4.4.0**.

Using `opp_env`:

```bash
opp_env install --init -w inet-workspace --build-modes=release inet-4.4.0
cd inet-workspace
opp_env shell
```

Alternatively, INET 4.4.0 can be imported manually into the OMNeT++ IDE.

---

## 2. Clone This Repository

```bash
git clone https://github.com/AhmedTSN/FRER_TSN_Baseline_Study.git
cd FRER_TSN_Baseline_Study
```

---

## 3. Import the Project into OMNeT++

1. Open the OMNeT++ IDE.
2. Import this repository as an existing project.
3. Import the INET 4.4.0 project.
4. Ensure that the simulation project references the INET project.
5. Verify that all required NED types are correctly resolved.

---

## 4. Install Python Dependencies

From the repository root:

```bash
pip install -r analysis_scripts/requirements.txt
```

---

# Reproducing the Experiments

## Main Experiments: Manual and Automatic FRER

The main experiments consist of **30 independent runs for each configuration**:

* Automatic FRER: Seeds **0–29**
* Manual FRER: Seeds **0–29**

The corresponding configuration files are located in:

```text
automatic_configuration/
manual_configuration/
```

### Random Seeds

Each independent run uses a distinct random seed through:

```text
seed-set = 0 ... 29
```

To reproduce an individual run, set the corresponding value in the `.ini` configuration file.

For example:

```text
seed-set = 0
```

for Seed 0.

For paired comparisons, the same seed should be used for both the manual and automatic configurations.

---

# Reviewer-Requested Control Experiments

## 1. 10.2-Second Extended Simulation

Location:

```text
additional_control_experiments/10.2s_extension_seed0/
```

Configuration:

```text
omnetpp_seed0_10.2s.ini
```

This experiment uses:

```text
seed-set = 0
```

and extends the simulation duration to **10.2 seconds**.

The purpose is to provide additional verification of the effective Packet Delivery Ratio (PDR).

---

## 2. 100-Byte Packet Control Experiment

Location:

```text
additional_control_experiments/100byte_packets_seed0/
```

Configuration:

```text
omnetpp_seed0_100B.ini
```

This experiment uses:

```text
seed-set = 0
```

with a packet size of **100 bytes**.

The purpose is to help isolate intrinsic FRER timing jitter from timing effects associated with link saturation.

---

# Reproducing the Statistical Analysis

All analysis scripts are located in:

```text
analysis_scripts/
```

The recommended execution order is:

## Step 1 — Extract Raw Simulation Data

After downloading and extracting the raw simulation outputs from the Google Drive archive:

```bash
cd analysis_scripts
python extract_raw_data.py
```

This script extracts the relevant information from the OMNeT++ `.sca` and `.vec` output files and converts the simulation results into structured data for subsequent analysis.

---

## Step 2 — Perform Statistical Analysis

```bash
python statistical_analysis.py
```

This script performs the statistical analyses used in the study, including:

* t-test
* Mann-Whitney U test
* TOST equivalence testing
* Cohen's d effect size

---

## Step 3 — Calculate the Timing Stability Index

```bash
python calculate_TSI.py
```

This script calculates the Timing Stability Index (TSI) and performs the associated sensitivity analysis.

---

## Step 4 — Generate Figures

```bash
python generate_figures.py
```

The generated publication-ready figures are saved in:

```text
figures/
```

---

# Processed Results

Processed and summarized experimental results are included directly in the GitHub repository under:

```text
processed_results/
```

The directory contains:

```text
automatic_configuration_results.xlsx
automatic_packet_life_time_histogram.xlsx
manual_configuration_results.xlsx
manual_packet_life_time_histogram.xlsx
autoFRER-10.2s-seed0-results.xlsx
autoFRER-100b-seed0-results.xls
```

These files contain processed results derived from the raw OMNeT++ simulation outputs.

For complete verification, the corresponding raw `.sca` and `.vec` files are available through the public Google Drive archive.

---

# Figures

The repository provides publication-ready figures generated from the experimental and analytical results:

* **Figure 1:** Network topology
* **Figure 2:** Delay evolution
* **Figure 3:** Distribution analysis
* **Figure 4:** Empirical Cumulative Distribution Function (ECDF)
* **Figure 5:** Jitter analysis
* **Figure 6:** ECDF comparison

All figures are available in the `figures/` directory.

---

# Reproducibility Workflow

The overall workflow is:

```text
GitHub Repository
       │
       ├── Simulation Models
       ├── Configuration Files
       ├── Control Experiments
       └── Analysis Scripts
                │
                │
                ▼
       Public Raw Data Archive
            (Google Drive)
                │
                ▼
          OMNeT++ / INET
                │
                ▼
          Raw .sca / .vec
                │
                ▼
       Python Data Extraction
                │
                ▼
       Statistical Analysis
                │
                ├── Hypothesis Tests
                ├── Equivalence Tests
                ├── Effect Sizes
                └── TSI Analysis
                │
                ▼
       Publication-Ready Figures
```

The combination of the GitHub repository, Zenodo archive, and public raw-data archive provides the materials required for independent verification and reproduction of the reported simulation results.

---

# Version and Archival Information

**Reproducibility Archive Version:** v1.1

**Zenodo DOI:**
https://doi.org/10.5281/zenodo.22116011

**GitHub Release:**
https://github.com/AhmedTSN/FRER_TSN_Baseline_Study/releases/tag/v1.1

The DOI identifies the archived **v1.1** reproducibility package.

The raw simulation data associated with this release are distributed separately through the public Google Drive archive due to their large storage requirements.

---

# License

This project is released under the **MIT License** to encourage reproducibility, verification, and reuse.

See the `LICENSE` file for the complete license text.

---

# Contact

For questions, issues, or collaboration opportunities, please contact:

**Ahmed M. Mohammed**
College of Information Engineering
Al-Nahrain University
Baghdad, Iraq

Email: `ahmed.mit23@ced.nahrainuniv.edu.iq`
