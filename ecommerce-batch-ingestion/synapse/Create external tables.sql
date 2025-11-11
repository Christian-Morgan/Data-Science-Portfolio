CREATE DATABASE GoldAnalytics;
GO


USE GoldAnalytics;
GO


CREATE DATABASE SCOPED CREDENTIAL ADLSCredential
WITH IDENTITY = 'Managed Identity';
GO


CREATE EXTERNAL FILE FORMAT DeltaFormat
WITH (
    FORMAT_TYPE = DELTA
)
GO


CREATE EXTERNAL DATA SOURCE ecommercedata
WITH (
    LOCATION = 'abfss://gold@datalakeecommerce.dfs.core.windows.net/',
    CREDENTIAL = ADLSCredential
);
GO


-- Create external tables

CREATE EXTERNAL TABLE customer_orders (
    order_id VARCHAR(100),
    order_date DATE,
    customer_id VARCHAR(100),
    customer_first_name VARCHAR(100),
    customer_last_name VARCHAR(100),
    email VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    product_id VARCHAR(100),
    product_name VARCHAR(255),
    brand VARCHAR(100),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    quantity INT,
    unit_price DECIMAL(10,2),
    order_total DECIMAL(18,2)
)
WITH (
    LOCATION = 'customer_orders/',
    DATA_SOURCE = ecommercedata,
    FILE_FORMAT = DeltaFormat
);
GO

CREATE EXTERNAL TABLE customer_summary (
    customer_id VARCHAR(100),
    customer_first_name VARCHAR(100),
    customer_last_name VARCHAR(100),
    email VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    total_orders INT,
    total_spent DECIMAL(18,2)
)
WITH (
    LOCATION = 'customer_summary/',
    DATA_SOURCE = ecommercedata,
    FILE_FORMAT = DeltaFormat
);
GO


CREATE EXTERNAL TABLE product_summary (
    product_id VARCHAR(100),
    product_name VARCHAR(255),
    brand VARCHAR(100),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    units_sold INT,
    total_revenue DECIMAL(18,2),
    times_ordered INT
)
WITH (
    LOCATION = 'product_summary/',
    DATA_SOURCE = ecommercedata,
    FILE_FORMAT = DeltaFormat
);
GO