#  Genomic & Clinical Data Pipeline: API to Superset

##  Project Overview
An end-to-end data engineering pipeline that extracts genomic transcript data via the Ensembl REST API, processes it using Python (Pandas), and loads it into a relational database for visualization in Apache Superset.

##  Architecture & Tech Stack
* **Data Extraction:** Python, `requests` library (Ensembl API)
* **Data Cleaning & ETL:** Pandas
* **Database:** SQLite / PostgreSQL
* **Business Intelligence:** Apache Superset, Docker

## 📁 Data Directory
```text
data/
├── raw/
│   └── BRCA1_raw_data.json             # Raw Ensembl response; input for the standalone transforms
└── processed/
	├── oncology_panel_transcripts.csv  # Main ETL output; input to the SQL loading step
	└── oncology_clinical.db            # SQLite database produced by src/load_sql.py
```

`src/extract.py` fetches the oncology panel from Ensembl and writes the processed CSV. It only reads a matching JSON from `data/raw/` as a fallback when an API request fails; it does not save successful responses there. `src/load_sql.py` reads the CSV and creates the SQLite database. The standalone `src/transform_pandas.py` and `src/transform_polars.py` scripts also read the BRCA1 JSON and can create separate CSVs in `data/processed/`; those are alternative outputs, not inputs to the main SQL loading step.

## 📊 Dashboard Preview
![Dashboard Preview](link-alla-tua-immagine-o-gif)

## ⚙️ How to Deploy (For technical review)
To replicate this dashboard in your local Superset instance:
1. Run the Python ETL script to populate the database.
2. Import the `dashboard_export.zip` file found in the `/superset_export` folder via the Superset UI.
