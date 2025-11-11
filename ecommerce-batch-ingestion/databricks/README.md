# Notebook Summaries

1. `00_setup_environment` – Mount Azure Data Lake Storage and configure authentication (credentials are placeholders).  
2. `01_ingest_to_bronze` – Ingest raw data from Azure SQL Database into the Bronze layer and add ingestion timestamps.  
3. `02_ingest_to_silver` – Clean and transform Bronze data into Silver tables and quarantine bad records.  
4. `03_ingest_to_gold` – Create curated Gold-layer tables (`customer_orders`, `customer_summary`, `product_summary`) for business analytics.
