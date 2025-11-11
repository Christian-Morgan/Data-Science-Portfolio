# Data Generation
This folder contains the scripts and configuration files used to generate **synthetic (fake) data** for this project.

## Overview
The data in this project is **not real**; it was generated using the [Faker](https://faker.readthedocs.io/) Python library to simulate realistic records such as names, addresses, transactions, timestamps, and other fields relevant to the dataset. Any similarity between points in the data an real life is purely coincidental.
Artificial Intelligence (AI) was used to **script and structure** the data generation logic to ensure that the dataset is both realistic and consistent.

## Purpose
The generated data is used to:
- Simulate real-world data ingestion pipelines  
- Test ETL/ELT workflows and CDC (Change Data Capture) logic  
- Demonstrate data movement through the **Medallion Architecture** (Bronze → Silver → Gold)

## How It Works
1. **`faker_initial.py`** – Generates the **initial dataset**, producing randomized but realistic records such as customers and orders.  
2. **`faker_incremental_load.py`** – Simulates **incremental loads** by generating new customers and orders, as well as applying random updates to existing customers. This mimics the behavior of ongoing system activity over time.

## Reproducibility
You can re-generate the datasets by running:

```bash
python faker_initial.py
```
To simulate new or updated data, run
```
python faker_incremental_load.py
