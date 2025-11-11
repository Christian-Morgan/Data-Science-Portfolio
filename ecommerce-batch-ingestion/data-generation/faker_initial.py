# ============================================
# REALISTIC FAKER WITH REALISTIC ISSUES
# Real cities, real states, real ZIPs
# ============================================

import pyodbc
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('en_US')
Faker.seed(42)

# ============================================
# CONNECTION
# ============================================

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
# REAL US LOCATIONS (ACCURATE MAPPINGS)
# ============================================

# Real cities with correct state/ZIP combinations
us_locations = [
    # (City, State, ZIP_prefix, Major cities for variety)
    ('New York', 'NY', '100', ['Manhattan', 'Brooklyn', 'Queens', 'Bronx']),
    ('Los Angeles', 'CA', '900', ['Los Angeles', 'Beverly Hills', 'Santa Monica', 'Pasadena']),
    ('Chicago', 'IL', '606', ['Chicago', 'Evanston', 'Oak Park', 'Naperville']),
    ('Houston', 'TX', '770', ['Houston', 'Pearland', 'Sugar Land', 'The Woodlands']),
    ('Phoenix', 'AZ', '850', ['Phoenix', 'Scottsdale', 'Tempe', 'Mesa']),
    ('Philadelphia', 'PA', '191', ['Philadelphia', 'Bala Cynwyd', 'Ardmore', 'Chester']),
    ('San Antonio', 'TX', '782', ['San Antonio', 'Alamo Heights', 'Leon Valley', 'Converse']),
    ('San Diego', 'CA', '921', ['San Diego', 'La Jolla', 'Coronado', 'Chula Vista']),
    ('Dallas', 'TX', '752', ['Dallas', 'Irving', 'Plano', 'Garland']),
    ('San Jose', 'CA', '951', ['San Jose', 'Sunnyvale', 'Santa Clara', 'Milpitas']),
    ('Austin', 'TX', '787', ['Austin', 'Round Rock', 'Cedar Park', 'Pflugerville']),
    ('Jacksonville', 'FL', '322', ['Jacksonville', 'Jacksonville Beach', 'Atlantic Beach', 'Neptune Beach']),
    ('Indianapolis', 'IN', '462', ['Indianapolis', 'Carmel', 'Fishers', 'Greenwood']),
    ('Columbus', 'OH', '432', ['Columbus', 'Dublin', 'Westerville', 'Grove City']),
    ('Charlotte', 'NC', '282', ['Charlotte', 'Matthews', 'Concord', 'Huntersville']),
    ('Seattle', 'WA', '981', ['Seattle', 'Bellevue', 'Redmond', 'Tacoma']),
    ('Denver', 'CO', '802', ['Denver', 'Aurora', 'Lakewood', 'Arvada']),
    ('Boston', 'MA', '021', ['Boston', 'Cambridge', 'Somerville', 'Brookline']),
    ('Nashville', 'TN', '372', ['Nashville', 'Franklin', 'Brentwood', 'Murfreesboro']),
    ('Detroit', 'MI', '482', ['Detroit', 'Dearborn', 'Livonia', 'Warren']),
    ('Portland', 'OR', '972', ['Portland', 'Beaverton', 'Hillsboro', 'Gresham']),
    ('Las Vegas', 'NV', '891', ['Las Vegas', 'Henderson', 'North Las Vegas', 'Paradise']),
    ('Miami', 'FL', '331', ['Miami', 'Miami Beach', 'Coral Gables', 'Hialeah']),
    ('Atlanta', 'GA', '303', ['Atlanta', 'Decatur', 'Sandy Springs', 'Marietta']),
    ('Minneapolis', 'MN', '554', ['Minneapolis', 'St Paul', 'Bloomington', 'Eden Prairie']),
]

# ============================================
# GENERATE PRODUCTS (100% CLEAN)
# ============================================

print("=" * 60)
print("GENERATING PRODUCTS (100% CLEAN)")
print("=" * 60)

products_data = [
    # (category, subcategory, products, cost_range)
    ('Electronics', 'Laptop', ['MacBook Pro', 'Dell XPS 15', 'HP Spectre', 'Lenovo ThinkPad', 'ASUS ZenBook'], (600, 1500)),
    ('Electronics', 'Smartphone', ['iPhone 14 Pro', 'Samsung Galaxy S23', 'Google Pixel 7', 'OnePlus 11'], (400, 1000)),
    ('Electronics', 'Headphones', ['Sony WH-1000XM5', 'Bose QC45', 'AirPods Pro', 'Beats Studio'], (150, 400)),
    ('Clothing', 'Shirt', ['Cotton T-Shirt', 'Polo Shirt', 'Oxford Shirt', 'Flannel Shirt'], (20, 60)),
    ('Clothing', 'Pants', ['Levi\'s Jeans', 'Chinos', 'Dress Pants', 'Cargo Pants'], (40, 100)),
    ('Clothing', 'Shoes', ['Nike Air Max', 'Adidas Ultraboost', 'New Balance 990', 'Vans Old Skool'], (60, 180)),
    ('Home', 'Furniture', ['IKEA Sofa', 'West Elm Table', 'Crate & Barrel Chair', 'CB2 Desk'], (300, 1200)),
    ('Home', 'Decor', ['Table Lamp', 'Floor Lamp', 'Area Rug', 'Wall Art'], (50, 300)),
]

brands = ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE']

product_id = 1
for category, subcategory, products, (min_cost, max_cost) in products_data:
    for product_name in products:
        brand = random.choice(brands)
        cost = round(random.uniform(min_cost * 0.6, max_cost * 0.7), 2)
        unit_price = round(cost * random.uniform(1.5, 2.3), 2)
        
        full_name = f"{brand} {product_name}"
        
        cursor.execute("""
            INSERT INTO dbo.products (
                product_id, product_name, category, subcategory, 
                brand, unit_price, cost, created_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, GETDATE())
        """, (product_id, full_name, category, subcategory, brand, unit_price, cost))
        
        product_id += 1
        if product_id > 100:
            break
    if product_id > 100:
        break

conn.commit()
print(f"✅ Inserted {product_id - 1} products\n")

# ============================================
# GENERATE CUSTOMERS
# ============================================

print("=" * 60)
print("GENERATING CUSTOMERS")
print("=" * 60)
print("Mix:")
print("  85% - Perfect data")
print("  10% - Formatting issues (fixable)")
print("   5% - Missing/invalid data (quarantine)")
print("=" * 60)

stats = {'perfect': 0, 'formatting': 0, 'missing': 0}

for customer_id in range(1, 1001):
    # Determine data quality tier
    rand = random.random()
    if rand < 0.85:
        quality_tier = 'perfect'
        stats['perfect'] += 1
    elif rand < 0.95:
        quality_tier = 'formatting'
        stats['formatting'] += 1
    else:
        quality_tier = 'missing'
        stats['missing'] += 1
    
    # Generate name
    first_name = fake.first_name()
    last_name = fake.last_name()
    
    # ============================================
    # EMAIL GENERATION
    # ============================================
    email_domain = random.choice(['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'icloud.com'])
    
    if quality_tier == 'perfect':
        # Clean email
        email = f"{first_name.lower()}.{last_name.lower()}@{email_domain}"
    
    elif quality_tier == 'formatting':
        # Formatting issues (but fixable)
        issue = random.choice(['uppercase', 'mixed_case', 'spaces', 'extra_dots'])
        if issue == 'uppercase':
            email = f"{first_name.upper()}.{last_name.upper()}@{email_domain.upper()}"
        elif issue == 'mixed_case':
            email = f"{first_name.lower()}.{last_name.upper()}@{email_domain}"
        elif issue == 'spaces':
            email = f" {first_name.lower()}.{last_name.lower()}@{email_domain} "  # Leading/trailing spaces
        elif issue == 'extra_dots':
            email = f"{first_name.lower()}..{last_name.lower()}@{email_domain}"  # Double dots
    
    else:  # missing
        # Invalid/missing email
        issue = random.choice(['null', 'no_at', 'no_domain'])
        if issue == 'null':
            email = None
        elif issue == 'no_at':
            email = f"{first_name.lower()}.{last_name.lower()}.{email_domain}"
        elif issue == 'no_domain':
            email = f"{first_name.lower()}.{last_name.lower()}@"
    
    # ============================================
    # LOCATION GENERATION (ALWAYS REAL/MATCHING)
    # ============================================
    metro_area, state, zip_prefix, cities = random.choice(us_locations)
    city = random.choice(cities)  # Pick a real city in that metro
    zip_code = zip_prefix + str(random.randint(10, 99))
    
    # Address generation
    street_number = fake.building_number()
    street_name = fake.street_name()
    apt_number = f" Apt. {random.randint(1, 999)}" if random.random() < 0.25 else ""
    
    if quality_tier == 'perfect':
        address = f"{street_number} {street_name}{apt_number}"
    elif quality_tier == 'formatting':
        # Formatting issues
        issue = random.choice(['lowercase', 'uppercase', 'extra_spaces'])
        if issue == 'lowercase':
            address = f"{street_number} {street_name}{apt_number}".lower()
        elif issue == 'uppercase':
            address = f"{street_number} {street_name}{apt_number}".upper()
        elif issue == 'extra_spaces':
            address = f"{street_number}   {street_name}{apt_number}"  # Extra spaces
    else:  # missing
        if random.random() < 0.5:
            address = None
        else:
            address = street_number  # Incomplete address (just number)
    
    # ============================================
    # PHONE GENERATION
    # ============================================
    area_code = random.randint(200, 999)
    exchange = random.randint(200, 999)
    number = random.randint(1000, 9999)
    
    if quality_tier == 'perfect':
        # Clean 10-digit phone
        phone = f"{area_code}{exchange}{number}"
    
    elif quality_tier == 'formatting':
        # Different formatting (but valid data)
        format_style = random.choice(['dashes', 'dots', 'parens', 'spaces', 'mixed'])
        if format_style == 'dashes':
            phone = f"{area_code}-{exchange}-{number}"
        elif format_style == 'dots':
            phone = f"{area_code}.{exchange}.{number}"
        elif format_style == 'parens':
            phone = f"({area_code}) {exchange}-{number}"
        elif format_style == 'spaces':
            phone = f"{area_code} {exchange} {number}"
        elif format_style == 'mixed':
            phone = f"{area_code}-{exchange}.{number}"
    
    else:  # missing
        # Invalid/missing phone
        issue = random.choice(['null', 'too_short', 'letters'])
        if issue == 'null':
            phone = None
        elif issue == 'too_short':
            phone = f"{random.randint(100,999)}{random.randint(1000,9999)}"  # 7 digits
        elif issue == 'letters':
            phone = f"{area_code}-CALL-NOW"
    
    # ============================================
    # INSERT TO DATABASE
    # ============================================
    try:
        cursor.execute("""
            INSERT INTO dbo.customers (
                customer_id, first_name, last_name, email, phone,
                address, city, state, zip, created_date, modified_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE(), GETDATE())
        """, (customer_id, first_name, last_name, email, phone, address, city, state, zip_code))
        
        if customer_id % 100 == 0:
            print(f"  Progress: {customer_id}/1000 customers...")
            
    except Exception as e:
        print(f"  Error on customer {customer_id}: {e}")

conn.commit()

print(f"\n✅ Inserted 1000 customers")
print(f"   Perfect data:        {stats['perfect']} ({stats['perfect']/10}%)")
print(f"   Formatting issues:   {stats['formatting']} ({stats['formatting']/10}%)")
print(f"   Missing/invalid:     {stats['missing']} ({stats['missing']/10}%)")
print()

# ============================================
# UPDATE CUSTOMERS (FOR CDC)
# ============================================

print("=" * 60)
print("UPDATING CUSTOMERS (FOR CDC)")
print("=" * 60)

for _ in range(50):
    customer_id = random.randint(1, 1000)
    first_name = fake.first_name()
    last_name = fake.last_name()
    new_email = f"{first_name.lower()}.{last_name.lower()}@gmail.com"
    new_phone = f"{random.randint(200,999)}{random.randint(200,999)}{random.randint(1000,9999)}"
    
    cursor.execute("""
        UPDATE dbo.customers
        SET email = ?, phone = ?, modified_date = GETDATE()
        WHERE customer_id = ?
    """, (new_email, new_phone, customer_id))

conn.commit()
print("✅ Updated 50 customers\n")

# ============================================
# GENERATE ORDERS (98% CLEAN)
# ============================================

print("=" * 60)
print("GENERATING ORDERS")
print("=" * 60)

# Clear existing orders first
print("  Clearing existing orders...")
cursor.execute("DELETE FROM dbo.orders")
conn.commit()
print("  ✅ Existing orders cleared")

# Query the database to get actual product count
cursor.execute("SELECT COUNT(*) FROM dbo.products")
total_products = cursor.fetchone()[0]
print(f"  Found {total_products} products in database")

if total_products == 0:
    print("  ❌ ERROR: No products found! Cannot generate orders.")
else:
    orders_inserted = 0
    for i in range(1, 2001):
        order_id = i
        customer_id = random.randint(1, 1000)
        selected_product_id = random.randint(1, total_products)  # Random product from available products
        
        # 2% chance of bad data
        if random.random() < 0.02:
            # Realistic errors
            error_type = random.choice(['future_date', 'zero_qty', 'negative_discount'])
            
            if error_type == 'future_date':
                order_date = fake.date_between(start_date='today', end_date='+60d')
                quantity = random.randint(1, 5)
                discount = random.choice([0.00, 0.05, 0.10])
            elif error_type == 'zero_qty':
                order_date = fake.date_between(start_date='-365d', end_date='today')
                quantity = 0
                discount = 0.00
            elif error_type == 'negative_discount':
                order_date = fake.date_between(start_date='-365d', end_date='today')
                quantity = random.randint(1, 5)
                discount = -0.05
        else:
            # Good order
            order_date = fake.date_between(start_date='-365d', end_date='today')
            quantity = random.randint(1, 5)
            discount = random.choice([0.00, 0.00, 0.00, 0.05, 0.10, 0.15, 0.20])
        
        # Get the unit price for the selected product
        cursor.execute("SELECT unit_price FROM dbo.products WHERE product_id = ?", selected_product_id)
        result = cursor.fetchone()
        unit_price = result[0] if result else 50.0
        
        try:
            cursor.execute("""
                INSERT INTO dbo.orders (
                    order_id, customer_id, product_id, order_date,
                    quantity, unit_price, discount, created_date, modified_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, GETDATE(), GETDATE())
            """, (order_id, customer_id, selected_product_id, order_date, quantity, unit_price, discount))
            
            orders_inserted += 1
            
            if orders_inserted % 200 == 0:
                print(f"  Progress: {orders_inserted}/2000 orders...")
        
        except Exception as e:
            print(f"  Error inserting order {order_id}: {e}")
    
    conn.commit()
    print(f"✅ Inserted {orders_inserted} orders\n")