import pyodbc
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('en_US')
Faker.seed(42)

# ============================================
# CONNECTION
# ============================================

# Use Driver 17 instead of 18
connection_string = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER=ecommerce-batch-ingestion.database.windows.net;'
    f'DATABASE=ecommerce-db;'
    f'Authentication=ActiveDirectoryInteractive;'
    f'Encrypt=yes;'
    f'TrustServerCertificate=no;'
)

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()
print("✅ Connected to database\n")

# ============================================
# INCREMENTAL CUSTOMERS (ADD + UPDATE + BAD DATA)
# ============================================

new_customers_count = 20
update_customers_count = 30
bad_data_probability = 0.1  # 10% of customers have bad data

# Max existing customer_id
cursor.execute("SELECT ISNULL(MAX(customer_id),0) FROM dbo.customers")
max_customer_id = cursor.fetchone()[0]

# US locations
us_locations = [
    ('New York', 'NY', '100', ['Manhattan', 'Brooklyn']),
    ('Los Angeles', 'CA', '900', ['Los Angeles', 'Beverly Hills']),
    ('Chicago', 'IL', '606', ['Chicago', 'Oak Park']),
    ('Houston', 'TX', '770', ['Houston', 'Sugar Land']),
]

# --- Add new customers ---
for i in range(1, new_customers_count + 1):
    customer_id = max_customer_id + i
    first_name = fake.first_name()
    last_name = fake.last_name()

    # Email with chance of bad formatting
    if random.random() < bad_data_probability:
        issue_type = random.choice(['uppercase', 'extra_dots', 'spaces', 'null'])
        if issue_type == 'uppercase':
            email = f"{first_name.upper()}.{last_name.upper()}@GMAIL.COM"
        elif issue_type == 'extra_dots':
            email = f"{first_name.lower()}..{last_name.lower()}@gmail.com"
        elif issue_type == 'spaces':
            email = f" {first_name.lower()}.{last_name.lower()}@gmail.com "
        else:  # null
            email = None
    else:
        email = f"{first_name.lower()}.{last_name.lower()}@gmail.com"

    # Phone with chance of bad formatting
    if random.random() < bad_data_probability:
        issue_type = random.choice(['too_short', 'letters', 'null'])
        if issue_type == 'too_short':
            phone = f"{random.randint(100,999)}{random.randint(100,9999)}"  # 7 digits
        elif issue_type == 'letters':
            phone = f"{random.randint(200,999)}-CALL-NOW"
        else:
            phone = None
    else:
        phone = f"{random.randint(200,999)}{random.randint(200,999)}{random.randint(1000,9999)}"

    # Location
    metro_area, state, zip_prefix, cities = random.choice(us_locations)
    city = random.choice(cities)
    zip_code = zip_prefix + str(random.randint(10, 99))
    street_number = fake.building_number()
    street_name = fake.street_name()
    address = f"{street_number} {street_name}"

    cursor.execute("""
        INSERT INTO dbo.customers (
            customer_id, first_name, last_name, email, phone,
            address, city, state, zip, created_date, modified_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE(), GETDATE())
    """, (customer_id, first_name, last_name, email, phone, address, city, state, zip_code))

print(f"✅ Added {new_customers_count} new customers (some with bad data)")

# --- Update existing customers ---
cursor.execute("SELECT customer_id FROM dbo.customers ORDER BY NEWID()")
existing_customer_ids = [row[0] for row in cursor.fetchall()]

for _ in range(update_customers_count):
    customer_id = random.choice(existing_customer_ids)
    first_name = fake.first_name()
    last_name = fake.last_name()

    # Email with chance of bad formatting
    if random.random() < bad_data_probability:
        issue_type = random.choice(['uppercase', 'extra_dots', 'spaces', 'null'])
        if issue_type == 'uppercase':
            email = f"{first_name.upper()}.{last_name.upper()}@GMAIL.COM"
        elif issue_type == 'extra_dots':
            email = f"{first_name.lower()}..{last_name.lower()}@gmail.com"
        elif issue_type == 'spaces':
            email = f" {first_name.lower()}.{last_name.lower()}@gmail.com "
        else:  # null
            email = None
    else:
        email = f"{first_name.lower()}.{last_name.lower()}@gmail.com"

    # Phone with chance of bad formatting
    if random.random() < bad_data_probability:
        issue_type = random.choice(['too_short', 'letters', 'null'])
        if issue_type == 'too_short':
            phone = f"{random.randint(100,999)}{random.randint(100,9999)}"  # 7 digits
        elif issue_type == 'letters':
            phone = f"{random.randint(200,999)}-CALL-NOW"
        else:
            phone = None
    else:
        phone = f"{random.randint(200,999)}{random.randint(200,999)}{random.randint(1000,9999)}"

    cursor.execute("""
        UPDATE dbo.customers
        SET email = ?, phone = ?, modified_date = GETDATE()
        WHERE customer_id = ?
    """, (email, phone, customer_id))

print(f"✅ Updated {update_customers_count} existing customers (some with bad data)\n")

# ============================================
# INCREMENTAL ORDERS (ADD + UPDATE + BAD DATA)
# ============================================

new_orders_count = 50
cursor.execute("SELECT COUNT(*) FROM dbo.products")
total_products = cursor.fetchone()[0]

cursor.execute("SELECT ISNULL(MAX(order_id),0) FROM dbo.orders")
max_order_id = cursor.fetchone()[0]

for i in range(1, new_orders_count + 1):
    order_id = max_order_id + i
    customer_id = random.randint(1, max_customer_id + new_customers_count)
    product_id = random.randint(1, total_products)

    # 2% chance of bad order data
    if random.random() < 0.02:
        error_type = random.choice(['future_date', 'zero_qty', 'negative_discount'])
        if error_type == 'future_date':
            order_date = fake.date_between(start_date='today', end_date='+60d')
            quantity = random.randint(1,5)
            discount = random.choice([0.00, 0.05, 0.10])
        elif error_type == 'zero_qty':
            order_date = fake.date_between(start_date='-30d', end_date='today')
            quantity = 0
            discount = 0.00
        elif error_type == 'negative_discount':
            order_date = fake.date_between(start_date='-30d', end_date='today')
            quantity = random.randint(1,5)
            discount = -0.05
    else:
        order_date = fake.date_between(start_date='-30d', end_date='today')
        quantity = random.randint(1,5)
        discount = random.choice([0.00, 0.05, 0.10, 0.15, 0.20])

    cursor.execute("SELECT unit_price FROM dbo.products WHERE product_id = ?", product_id)
    result = cursor.fetchone()
    unit_price = result[0] if result else 50.0

    cursor.execute("""
        INSERT INTO dbo.orders (
            order_id, customer_id, product_id, order_date,
            quantity, unit_price, discount, created_date, modified_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, GETDATE(), GETDATE())
    """, (order_id, customer_id, product_id, order_date, quantity, unit_price, discount))

print(f"✅ Added {new_orders_count} new orders (some with bad data)")

# Update a few existing orders
update_orders_count = 20
cursor.execute("SELECT order_id FROM dbo.orders ORDER BY NEWID()")
existing_order_ids = [row[0] for row in cursor.fetchall()]

for _ in range(update_orders_count):
    order_id = random.choice(existing_order_ids)
    new_quantity = random.randint(1,5)
    new_discount = random.choice([0.00, 0.05, 0.10, 0.15, 0.20])
    cursor.execute("""
        UPDATE dbo.orders
        SET quantity = ?, discount = ?, modified_date = GETDATE()
        WHERE order_id = ?
    """, (new_quantity, new_discount, order_id))

print(f"✅ Updated {update_orders_count} existing orders\n")

conn.commit()
print("✅ CDC run completed successfully")

# Close connection
cursor.close()
conn.close()