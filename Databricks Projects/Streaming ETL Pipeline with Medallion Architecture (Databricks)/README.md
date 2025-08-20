## Project Overview

This project demonstrates an end-to-end data pipeline implemented in Databricks using the Medallion Architecture (Bronze → Silver → Gold).

The pipeline uses synthetic streaming data generated with Python’s Faker
 library and highlights key data engineering practices:

🔹 Bronze Layer: Streaming ingestion with watermarking to handle late/duplicate data.

🔹 Silver Layer: Data cleansing, anonymization, access control, and data quality validation using expectations.

🔹 Gold Layer: Aggregations and joins for analytics-ready datasets.

This project is designed to showcase both technical implementation and practical data engineering skills for real-world scenarios.
