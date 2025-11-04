# Wine Quality Dataset Versioning with DVC

## Overview
This project demonstrates **data versioning** using **DVC (Data Version Control)** with **Google Cloud Storage** as remote storage. The project tracks the evolution of a wine quality dataset through three distinct versions: raw data, cleaned data, and feature-engineered data.
  
**Repository:** https://github.com/RishzG/wine_quality_dvc_lab

---

## Dataset Information

**Source:** [UCI Machine Learning Repository - Wine Quality Dataset](https://archive.ics.uci.edu/ml/datasets/wine+quality)

**Description:** This dataset contains physicochemical properties and quality ratings of red wine samples. It is commonly used for regression and classification tasks in machine learning.

**Original Dataset:**
- **Samples:** 1,599 red wine instances
- **Features:** 11 physicochemical properties + 1 quality rating (0-10)
- **Target Variable:** Quality (score between 3 and 8)

**Features:**
1. Fixed acidity
2. Volatile acidity
3. Citric acid
4. Residual sugar
5. Chlorides
6. Free sulfur dioxide
7. Total sulfur dioxide
8. Density
9. pH
10. Sulphates
11. Alcohol
12. Quality (target)

---

## Dataset Versions

### v1.0 - Raw Data
**Description:** Original dataset downloaded from UCI repository with no modifications.

**Characteristics:**
- **Samples:** 1,599
- **Features:** 12
- **Size:** ~92 KB
- **Issues:** Contains duplicates and outliers

**Git Tag:** `v1.0`

---

### v2.0 - Cleaned Data
**Description:** Preprocessed dataset with quality improvements applied.

**Data Cleaning Steps:**
1. **Duplicate Removal:** Removed 240 duplicate entries
2. **Outlier Detection:** Applied IQR (Interquartile Range) method to detect and remove outliers
3. **Feature Normalization:** Standardized all features using StandardScaler (zero mean, unit variance)

**Characteristics:**
- **Samples:** 985 (38.4% reduction from v1.0)
- **Features:** 12 (same as v1.0)
- **Size:** ~63 KB
- **Quality:** Clean data, no duplicates, normalized features

**Git Tag:** `v2.0`

---

### v3.0 - Feature-Engineered Data
**Description:** Enhanced dataset with derived features for improved model performance.

**New Features Created:**
1. **total_acidity:** Sum of fixed and volatile acidity
2. **alcohol_to_density:** Ratio of alcohol content to wine density
3. **sulphates_to_alcohol:** Ratio of sulphates to alcohol
4. **acidity_ratio:** Ratio of fixed to volatile acidity
5. **free_to_total_sulfur:** Ratio of free to total sulfur dioxide
6. **is_good_quality:** Binary classification (1 if quality ≥ 7, else 0)

**Characteristics:**
- **Samples:** 985 (same as v2.0)
- **Features:** 18 (6 new features added, 50% increase)
- **Size:** ~303KB
- **Target Distribution:** 125 good quality wines (12.7%), 860 regular quality wines (87.3%)

**Git Tag:** `v3.0`

---

## Project Structure

```
wine-quality-dvc/
├── data/
│   ├── raw/
│   │   ├── .gitignore
│   │   └── wine_quality.csv.dvc          # v1.0 metadata
│   ├── processed/
│   │   ├── .gitignore
│   │   └── wine_quality_clean.csv.dvc    # v2.0 metadata
│   └── features/
│       ├── .gitignore
│       └── wine_quality_featured.csv.dvc # v3.0 metadata
├── scripts/
│   ├── download_data.py                  # Download raw dataset
│   ├── preprocess.py                     # Data cleaning and normalization
│   ├── feature_engineering.py            # Create derived features
│   ├── analyze_versions.py               # Statistical analysis
│   └── visualize_evolution.py            # Generate comparison plots
├── reports/
│   ├── dataset_stats.json                # Version statistics
│   ├── version_comparison.png            # Comparison charts
│   └── quality_distribution.png          # Quality distribution plots
├── .dvc/
│   └── config                            # DVC configuration
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Setup Instructions

### Prerequisites
- Python 3.7+
- Git
- Google Cloud Platform account
- Google Cloud Storage bucket

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/RishzG/wine_quality_dvc_lab.git
cd wine_quality_dvc_lab
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Initialize DVC:**
```bash
dvc init
```

4. **Configure Google Cloud Storage remote:**
```bash
# Replace with your bucket name
dvc remote add -d myremote gs://your-bucket-name

# Configure credentials
dvc remote modify myremote credentialpath path/to/credentials.json
```

5. **Pull data from remote storage:**
```bash
dvc pull
```

This will download all dataset versions from Google Cloud Storage to your local machine.

---

## Usage

### Reproducing the Complete Pipeline

**Step 1: Download Raw Data (v1.0)**
```bash
python scripts/download_data.py
dvc add data/raw/wine_quality.csv
git add data/raw/wine_quality.csv.dvc data/raw/.gitignore
git commit -m "v1.0: Add raw wine quality dataset"
git tag -a v1.0 -m "Version 1.0: Raw data"
dvc push
```

**Step 2: Create Cleaned Data (v2.0)**
```bash
python scripts/preprocess.py
dvc add data/processed/wine_quality_clean.csv
git add data/processed/wine_quality_clean.csv.dvc data/processed/.gitignore scripts/preprocess.py
git commit -m "v2.0: Add cleaned and normalized dataset"
git tag -a v2.0 -m "Version 2.0: Cleaned data"
dvc push
```

**Step 3: Create Feature-Engineered Data (v3.0)**
```bash
python scripts/feature_engineering.py
dvc add data/features/wine_quality_featured.csv
git add data/features/wine_quality_featured.csv.dvc data/features/.gitignore scripts/feature_engineering.py
git commit -m "v3.0: Add feature-engineered dataset"
git tag -a v3.0 -m "Version 3.0: Feature-engineered data"
dvc push
```

**Step 4: Generate Analysis and Visualizations**
```bash
python scripts/analyze_versions.py
python scripts/visualize_evolution.py
git add scripts/ reports/
git commit -m "Add analysis and visualization scripts"
git push origin main
```

---

### Switching Between Dataset Versions

DVC makes it easy to switch between different versions of your data:

**Switch to v1.0 (Raw Data):**
```bash
git checkout v1.0
dvc checkout
```

**Switch to v2.0 (Cleaned Data):**
```bash
git checkout v2.0
dvc checkout
```

**Switch to v3.0 (Feature-Engineered Data):**
```bash
git checkout v3.0
dvc checkout
```

**Return to latest version:**
```bash
git checkout main
dvc checkout
```

---

## Results

### Dataset Evolution Summary

| Version | Samples | Features | Size (KB) | Description |
|---------|---------|----------|-----------|-------------|
| v1.0    | 1,599   | 12       | 91.41     | Raw data from UCI |
| v2.0    | 985     | 12       | 211.21    | Cleaned and normalized |
| v3.0    | 985     | 18       | 303.25    | With engineered features |

### Key Improvements

**Data Quality (v1.0 → v2.0):**
-  Removed 240 duplicate samples
-  Removed 142 outlier samples using IQR method
-  Normalized all features (zero mean, unit variance)
-  **38.4% reduction in samples** while improving data quality

**Feature Engineering (v2.0 → v3.0):**
-  Added 6 domain-specific derived features
-  **50% increase in features** for better model performance
-  Created binary classification target (is_good_quality)
-  Maintained data quality from v2.0

### Visualizations

The project includes comprehensive visualizations showing:
1. **Sample count comparison** across versions
2. **Feature count evolution** over versions
3. **File size changes** through the pipeline
4. **Quality distribution** for each version

See `reports/` folder for generated charts.

---

## Technologies Used

- **DVC (Data Version Control):** Data versioning and pipeline management
- **Google Cloud Storage:** Remote data storage
- **Git/GitHub:** Code version control and collaboration
- **Python:** Data processing and analysis
- **Pandas:** Data manipulation
- **Scikit-learn:** Data preprocessing (StandardScaler)
- **Matplotlib:** Data visualization
- **JSON:** Structured reporting

---

## Requirements

```
dvc[gs]>=2.0.0
pandas>=1.3.0
scikit-learn>=0.24.0
matplotlib>=3.3.0
numpy>=1.19.0
```

See `requirements.txt` for complete list.

---

## Google Cloud Storage Setup

This project uses Google Cloud Storage as the DVC remote. To set up:

1. Create a GCS bucket in `us-east1` region
2. Create a service account with Storage Admin permissions
3. Download service account credentials (JSON)
4. Configure DVC with credentials:
   ```bash
   dvc remote modify myremote credentialpath path/to/credentials.json
   ```

---

**Last Updated:** November 2024
