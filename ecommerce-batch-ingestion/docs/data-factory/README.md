# Azure Data Factory Pipeline
## Linked Services
### Azure SQL Database
![Azure SQL Database Linked Service](../data-factory/Linked-service-sql-db-setup.png)

Connects to the ecommerce-db database where CDC is enabled. Uses system-assigned managed identity for authentication.
### Azure Databricks
![Azure Databricks Linked Service](../data-factory/Linked-service-databricks-setup.png)

Connects to the Databricks workspace that runs transformation notebooks and writes data to ADLS (Bronze, Silver, Gold layers).

## Pipeline: `ingest_transform`
### Trigger Configuration
![Pipeline Trigger](../data-factory/batch-ingestion-trigger-adf.png)

Scheduled to run daily at 12:05 AM Eastern Time. Checks for new data and processes it through the medallion architecture.
### Lookup Activity
![Lookup Activity](../data-factory/find-data-lookup-activity.png)

Queries the database to find the latest timestamp from customers and orders tables. This determines if new data exists to process.
### If Condition & Pipeline Flow
![Lookup Activity](../data-factory/if_condition_setup_adf.png)

If new data is detected (timestamp within last 24 hours), the pipeline runs three Databricks notebooks in sequence:

- `01_ingest_to_bronze` - Raw data ingestion

- `02_ingest_to_silver` - Data cleansing and transformation

- `03_ingest_to_gold` - Business-level aggregations
