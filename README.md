# Insurance Risk Analytics

End-to-end pipeline for insurance risk analysis: EDA, hypothesis testing, and predictive modeling.

## Setup

```bash
pip install -r requirements.txt
```

## Structure

| Path | Description |
|------|-------------|
| `data/` | Raw and processed datasets |
| `notebooks/` | Jupyter notebooks for analysis |
| `src/` | Reusable Python modules |
| `reports/` | Final reports and outputs |
| `tests/` | Unit tests |

## Usage

```bash
# Run notebooks
jupyter notebook

# Run tests
pytest tests/
```

## Data Pipeline (DVC)

This project uses [DVC](https://dvc.org) to version and reproduce the data pipeline.

### Reproduce locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Pull tracked datasets from remote storage
dvc pull

# 3. (Optional) Re-run the cleaning step
python src/clean_data.py
```

### Data versions

| File | Description |
|------|-------------|
| `data/insurance_data.csv` | Raw dataset tracked with DVC |
| `data/insurance_data_cleaned.csv` | Cleaned dataset (duplicates removed, nulls dropped) |

### Remote storage

The default DVC remote is a local directory at `C:/Users/ephra/dvc_local_storage`.  
To reconfigure for a different machine:

```bash
dvc remote add -d localstorage /path/to/your/storage
```
