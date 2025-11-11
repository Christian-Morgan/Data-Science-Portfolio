# Azure Synapse Analytics Scripts

This directory contains SQL scripts for setting up Synapse serverless SQL pool to query data from ADLS Gen2.

## Scripts

### Create external tables.sql
Creates the Synapse database and external tables that point to the Bronze, Silver, and Gold layers in ADLS Gen2.

### Create sales view.sql
Creates an aggregated sales view from the Gold layer data for Power BI reporting.

## Execution Order
1. Run `Create external tables.sql` first
2. Run `Create sales view.sql` second
3. Connect Power BI to the sales view (i.e., vw_Sales) via Azure Synapse Analytics SQL connector
