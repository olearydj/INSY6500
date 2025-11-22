"""
Core data generation logic for Test 2b
This module contains the functions used to generate the coffee shop dataset.
"""

import pandas as pd
import numpy as np
from datetime import timedelta
import hashlib

# Course identifier for verification hash
COURSE_SALT = "INSY6500-Fall2024"

# =============================================================================
# BANNER ID INPUT AND VALIDATION
# =============================================================================

def print_verification_info(banner_id, verification_hash):
    """Print verification information for student submission"""
    print("\n" + "=" * 70)
    print("DATA VERIFICATION INFORMATION")
    print("=" * 70)
    print(f"banner id:          {banner_id}")
    print(f"verification code:  {verification_hash}")
    print("⚠️  Include those two lines at the top of your notebook submission!")
    print("=" * 70)

def get_banner_id():
    """Prompt for and validate Banner ID"""
    print("=" * 70)
    print("TEST 2B DATA GENERATION")
    print("=" * 70)
    print("\nYou will generate a unique dataset using your Banner ID as the seed.")
    print("This ensures academic integrity while allowing you to verify your work.\n")

    while True:
        # First entry
        banner_id_1 = input("Enter your 9-digit Banner ID: ").strip()

        # Validate format
        if not banner_id_1.isdigit():
            print("❌ Error: Banner ID must contain only digits.\n")
            continue

        if len(banner_id_1) != 9:
            print(f"❌ Error: Banner ID must be exactly 9 digits (you entered {len(banner_id_1)}).\n")
            continue

        # Confirmation entry
        banner_id_2 = input("Re-enter your Banner ID to confirm: ").strip()

        if banner_id_1 != banner_id_2:
            print("❌ Error: Banner IDs do not match. Please try again.\n")
            continue

        # Success
        banner_id = int(banner_id_1)
        print(f"\n✓ Banner ID confirmed: {banner_id}")

        # Generate verification hash
        verification_hash = hashlib.sha256(
            f"{banner_id}-{COURSE_SALT}".encode()
        ).hexdigest()[:12]

        print_verification_info(banner_id, verification_hash)

        return banner_id, verification_hash

# =============================================================================
# PRODUCT CATALOG
# =============================================================================

def create_products():
    """Create the product catalog"""
    products = pd.DataFrame({
        'product_id': range(101, 119),  # 18 products (was 15)
        'name': [
            # Coffee (6) - added Nitro Cold Brew
            'Espresso', 'Cappuccino', 'Latte', 'Americano', 'Cold Brew', 'Nitro Cold Brew',
            # Tea (4) - added Premium Matcha
            'Green Tea', 'Chai Latte', 'Herbal Tea', 'Premium Matcha',
            # Pastry (4)
            'Croissant', 'Muffin', 'Scone', 'Cinnamon Roll',
            # Sandwich (4) - added Steak Panini
            'Turkey Club', 'Veggie Wrap', 'BLT', 'Steak Panini'
        ],
        'category': [
            'Coffee', 'Coffee', 'Coffee', 'Coffee', 'Coffee', 'Coffee',
            'Tea', 'Tea', 'Tea', 'Tea',
            'Pastry', 'Pastry', 'Pastry', 'Pastry',
            'Sandwich', 'Sandwich', 'Sandwich', 'Sandwich'
        ],
        'cost': [
            # Coffee costs - Nitro is premium
            1.20, 1.80, 1.90, 1.00, 1.50, 2.50,
            # Tea costs - Premium Matcha is premium
            0.80, 1.20, 0.70, 2.20,
            # Pastry costs - made in-house, good margins
            1.00, 0.90, 1.10, 1.40,
            # Sandwich costs - Steak Panini is premium
            3.50, 2.80, 3.20, 5.50
        ]
    })
    return products

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_markup(product_name, category, location):
    """Calculate markup based on product, category, and location"""

    # Premium products get higher markup (200% margin = 3x cost)
    if product_name in ['Nitro Cold Brew', 'Premium Matcha', 'Steak Panini']:
        base_markup = 3.5
    # Regular sandwiches have good margins
    elif category == 'Sandwich':
        base_markup = 2.8
    # Pastries made in-house = great margins
    elif category == 'Pastry':
        base_markup = 3.5
    # Tea is competitive (lower margins)
    elif category == 'Tea':
        base_markup = 2.3
    # Coffee is competitive
    else:
        base_markup = 2.5

    # Downtown location can charge more (professional clientele)
    if location == 'Downtown':
        base_markup *= 1.15
    # Campus has to be cheaper (student budgets)
    elif location == 'Campus':
        base_markup *= 0.90

    return base_markup

def get_product_probabilities(hour, location, day_of_week):
    """Return product selection probabilities based on time, location, and day"""

    # Base probabilities by time of day
    if 6 <= hour < 10:  # Morning rush
        category_probs = {'Coffee': 0.55, 'Tea': 0.15, 'Pastry': 0.25, 'Sandwich': 0.05}
    elif 10 <= hour < 12:  # Late morning
        category_probs = {'Coffee': 0.40, 'Tea': 0.20, 'Pastry': 0.25, 'Sandwich': 0.15}
    elif 12 <= hour < 14:  # Lunch
        category_probs = {'Coffee': 0.20, 'Tea': 0.10, 'Pastry': 0.10, 'Sandwich': 0.60}
    elif 14 <= hour < 17:  # Afternoon
        category_probs = {'Coffee': 0.35, 'Tea': 0.25, 'Pastry': 0.30, 'Sandwich': 0.10}
    else:  # Evening (17-21)
        category_probs = {'Coffee': 0.30, 'Tea': 0.30, 'Pastry': 0.20, 'Sandwich': 0.20}

    # STRONG location-specific adjustments
    if location == 'Campus':
        # Students: love coffee and pastries, can't afford expensive sandwiches
        category_probs['Coffee'] += 0.15
        category_probs['Pastry'] += 0.05
        category_probs['Sandwich'] -= 0.20  # Major reduction
        # Extreme morning rush
        if 7 <= hour < 10:
            category_probs['Coffee'] += 0.10
            category_probs['Pastry'] -= 0.05
            category_probs['Sandwich'] -= 0.05

    elif location == 'Downtown':
        # Professionals: strong lunch culture, balanced otherwise
        if 12 <= hour < 14:  # LUNCH RUSH
            category_probs['Sandwich'] += 0.25
            category_probs['Coffee'] -= 0.15
            category_probs['Pastry'] -= 0.10
        # Morning meetings = more coffee
        if 8 <= hour < 10:
            category_probs['Coffee'] += 0.10
            category_probs['Tea'] -= 0.05
            category_probs['Pastry'] -= 0.05

    elif location == 'Suburb':
        # Families: much more tea (parents with kids), less coffee
        category_probs['Tea'] += 0.25
        category_probs['Coffee'] -= 0.25
        # After-school pickup time = pastries and tea
        if 15 <= hour < 17:
            category_probs['Tea'] += 0.10
            category_probs['Pastry'] += 0.10
            category_probs['Sandwich'] -= 0.10
            category_probs['Coffee'] -= 0.10

    # Day-of-week patterns
    if day_of_week == 0:  # Monday - highest coffee day (Monday blues)
        category_probs['Coffee'] += 0.05
        category_probs['Tea'] -= 0.05
    elif day_of_week == 4:  # Friday - higher lunch sales
        if 12 <= hour < 14:
            category_probs['Sandwich'] += 0.10
            category_probs['Coffee'] -= 0.05
            category_probs['Pastry'] -= 0.05

    # Ensure no negative values
    category_probs = {k: max(0.01, v) for k, v in category_probs.items()}

    # Normalize to ensure sum = 1.0
    total = sum(category_probs.values())
    category_probs = {k: v/total for k, v in category_probs.items()}

    return category_probs

def select_product(category, location, products):
    """Select specific product from category, with location preferences"""
    category_products = products[products['category'] == category]

    # Weight products within category
    weights = np.ones(len(category_products))

    for idx, product in enumerate(category_products.itertuples()):
        # Premium products are rarer
        if product.name in ['Nitro Cold Brew', 'Premium Matcha', 'Steak Panini']:
            weights[idx] = 0.15
        # BLT is unpopular (will have few sales)
        elif product.name == 'BLT':
            weights[idx] = 0.10
        # Campus avoids expensive items
        elif location == 'Campus':
            if product.name in ['Turkey Club', 'Steak Panini']:
                weights[idx] *= 0.30
            if product.name in ['Nitro Cold Brew', 'Premium Matcha']:
                weights[idx] *= 0.20
        # Downtown loves premium items
        elif location == 'Downtown':
            if product.name in ['Nitro Cold Brew', 'Premium Matcha', 'Steak Panini']:
                weights[idx] *= 2.5

    # Normalize weights
    weights = weights / weights.sum()

    return category_products.sample(n=1, weights=weights).iloc[0]

def generate_transaction(transaction_id, timestamp, location, day_of_week, products):
    """Generate a single transaction with all attributes"""

    hour = timestamp.hour

    # Get product selection probabilities
    category_probs = get_product_probabilities(hour, location, day_of_week)

    # Select category
    category = np.random.choice(
        list(category_probs.keys()),
        p=list(category_probs.values())
    )

    # Select specific product
    product = select_product(category, location, products)

    # Quantity (mostly 1, occasionally 2-3)
    quantity = np.random.choice([1, 1, 1, 1, 2, 2, 3], p=[0.50, 0.25, 0.15, 0.05, 0.03, 0.015, 0.005])

    # Calculate revenue with markup and variation
    markup = get_markup(product['name'], product['category'], location)
    base_price = product['cost'] * markup
    price_variation = np.random.uniform(0.90, 1.10)  # Tighter than before
    unit_price = base_price * price_variation
    revenue = round(unit_price * quantity, 2)

    # Payment method (varies by location)
    if location == 'Campus':
        payment = np.random.choice(['Cash', 'Credit', 'Mobile'], p=[0.10, 0.40, 0.50])
    elif location == 'Downtown':
        payment = np.random.choice(['Cash', 'Credit', 'Mobile'], p=[0.05, 0.55, 0.40])
    else:  # Suburb
        payment = np.random.choice(['Cash', 'Credit', 'Mobile'], p=[0.15, 0.60, 0.25])

    # Loyalty member (higher at Downtown and Suburb, lower at Campus)
    if location == 'Campus':
        loyalty_prob = 0.25
    elif location == 'Downtown':
        loyalty_prob = 0.45
    else:  # Suburb
        loyalty_prob = 0.55

    is_loyalty_member = np.random.random() < loyalty_prob

    return {
        'transaction_id': transaction_id,
        'timestamp': timestamp,
        'location': location,
        'product_id': product['product_id'],
        'quantity': quantity,
        'revenue': revenue,
        'payment_method': payment,
        'loyalty_member': is_loyalty_member
    }

# =============================================================================
# GENERATE TRANSACTIONS
# =============================================================================

def generate_sales(products):
    """Generate 2 weeks of sales transactions"""
    from datetime import datetime

    transactions = []
    transaction_id = 1000

    # Date range: previous 14 days ending yesterday
    end_date = pd.Timestamp(datetime.now().date()) - timedelta(days=1)
    start_date = end_date - timedelta(days=13)  # 14 days total
    end_date = end_date + timedelta(days=1)  # Make end_date exclusive
    start_date = start_date.replace(hour=6, minute=0, second=0)

    # Activity patterns by hour (base values)
    hourly_activity_base = {
        6: 5, 7: 15, 8: 30, 9: 20, 10: 12,   # Morning peak at 8am
        11: 15, 12: 35, 13: 30, 14: 10,       # Lunch peak at noon
        15: 8, 16: 12, 17: 15, 18: 10,
        19: 8, 20: 5, 21: 3
    }

    # Add slight random variation to activity levels (0.9 to 1.1 multiplier)
    activity_multiplier = np.random.uniform(0.9, 1.1)
    hourly_activity = {k: int(v * activity_multiplier) for k, v in hourly_activity_base.items()}

    # Special promotional day (first Friday in the date range)
    # Find the first Friday
    temp_date = start_date
    while temp_date.dayofweek != 4:  # 4 = Friday
        temp_date += timedelta(days=1)
    promo_date = temp_date.date()

    # Location store
    locations = ['Downtown', 'Campus', 'Suburb']

    current_date = start_date
    while current_date < end_date:
        day_of_week = current_date.dayofweek  # 0=Monday, 6=Sunday
        is_promo_day = current_date.date() == promo_date

        # Weekend adjustment
        if day_of_week >= 5:  # Weekend
            weekend_factor = 0.55  # 45% reduction
        else:
            weekend_factor = 1.0

        # Friday is busier
        if day_of_week == 4:
            weekend_factor = 1.15

        # Promotional day boost
        if is_promo_day:
            weekend_factor = 1.5  # 50% more traffic

        for hour in range(6, 22):
            activity = int(hourly_activity.get(hour, 5) * weekend_factor)

            for _ in range(activity):
                minute = np.random.randint(0, 60)
                timestamp = current_date.replace(hour=hour, minute=minute)

                # Location selection varies by day
                if day_of_week < 5:  # Weekday
                    location = np.random.choice(locations, p=[0.40, 0.45, 0.15])
                else:  # Weekend - Suburb much busier
                    location = np.random.choice(locations, p=[0.25, 0.15, 0.60])

                transaction = generate_transaction(transaction_id, timestamp, location, day_of_week, products)
                transactions.append(transaction)
                transaction_id += 1

        current_date += timedelta(days=1)

    # Create DataFrame
    sales = pd.DataFrame(transactions)
    return sales

# =============================================================================
# DATA QUALITY ISSUES
# =============================================================================

def add_data_quality_issues(sales):
    """Add realistic data quality issues to the sales data"""
    # Issue 1: Multiple orphaned product_ids (more realistic than single ID)
    n_orphaned = np.random.randint(8, 16)  # 8-15 orphaned transactions
    orphan_indices = np.random.choice(sales.index, size=n_orphaned, replace=False)
    orphan_ids = np.random.choice([199, 200, 201], size=n_orphaned)  # 3 different invalid IDs
    sales.loc[orphan_indices, 'product_id'] = orphan_ids

    # Issue 2: Boost sales for an unpopular product at a random location
    n_boost = np.random.randint(3, 9)
    boost_location = np.random.choice(['Downtown', 'Campus', 'Suburb'])
    location_sales = sales[sales['location'] == boost_location]
    if len(location_sales) >= n_boost:
        boost_indices = np.random.choice(location_sales.index, size=n_boost, replace=False)
        sales.loc[boost_indices, 'product_id'] = 117

    # Issue 3: Missing quantity values
    n_missing_qty = np.random.randint(3, 8)  # 3-7 missing quantities
    nan_quantity_indices = np.random.choice(sales.index, size=n_missing_qty, replace=False)
    sales.loc[nan_quantity_indices, 'quantity'] = np.nan

    # Issue 4: Missing revenue values
    n_missing_rev = np.random.randint(2, 6)  # 2-5 missing revenues
    nan_revenue_indices = np.random.choice(sales.index, size=n_missing_rev, replace=False)
    sales.loc[nan_revenue_indices, 'revenue'] = np.nan

    # Issue 5: Duplicate transactions (data entry errors)
    n_duplicates = np.random.randint(2, 6)  # 2-5 duplicates
    duplicate_indices = np.random.choice(sales.index, size=n_duplicates, replace=False)
    for idx in duplicate_indices:
        duplicate_row = sales.loc[idx].copy()
        sales = pd.concat([sales, pd.DataFrame([duplicate_row])], ignore_index=True)

    # Sort by timestamp to mix duplicates in naturally
    sales = sales.sort_values('timestamp').reset_index(drop=True)

    return sales

# =============================================================================
# SAVE DATA
# =============================================================================

def save_data(products, sales):
    """Save products and sales data to CSV files in data/ subdirectory"""
    from pathlib import Path

    # Create data directory if it doesn't exist
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)

    products.to_csv(data_dir / 'products.csv', index=False)
    sales.to_csv(data_dir / 'sales.csv', index=False)
