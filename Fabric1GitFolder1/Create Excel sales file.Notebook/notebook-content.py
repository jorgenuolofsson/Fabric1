# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!
# Welcome to your new notebook
# Type here in the cell editor to add code!
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# -----------------------------
# CONFIGURATION
# -----------------------------
NUM_ROWS = 10000
START_ORDER_ID = 100001

salespersons = ["Anna", "Johan", "Sara", "Peter", "Maria"]

# Customer and item ranges
CUSTOMER_MIN = 526580
CUSTOMER_MAX = 615845

ITEM_MIN = 254412
ITEM_MAX = 4585124

# Quantity range
QTY_MIN = 700
QTY_MAX = 1300

# -----------------------------
# SEASONAL DATE GENERATOR
# -----------------------------
def generate_seasonal_date():
    year = random.choice([2025, 2026])

    # Seasonal weighting
    high_season_months = [3, 4, 5, 6, 9, 10, 11]
    low_season_months = [1, 2, 7, 8, 12]

    if random.random() < 0.65:
        month = random.choice(high_season_months)
    else:
        month = random.choice(low_season_months)

    day = random.randint(1, 28)
    return datetime(year, month, day).strftime("%Y-%m-%d")

# -----------------------------
# FIXED PRICE PER ITEM
# -----------------------------
def price_for_item(item_no):
    # Price grows with item number
    return int(50 + (item_no % 500) * 0.8)

# -----------------------------
# DATA GENERATION
# -----------------------------
rows = []
order_id = START_ORDER_ID

while len(rows) < NUM_ROWS:
    num_lines = random.randint(1, 10)
    for line_no in range(1, num_lines + 1):
        if len(rows) >= NUM_ROWS:
            break

        order_line_id = f"{line_no:03d}"
        delivery_date = generate_seasonal_date()
        customer_no = random.randint(CUSTOMER_MIN, CUSTOMER_MAX)
        item_no = random.randint(ITEM_MIN, ITEM_MAX)
        salesperson = random.choice(salespersons)
        quantity = random.randint(QTY_MIN, QTY_MAX)
        price = price_for_item(item_no)
        amount = quantity * price

        rows.append([
            order_id,
            order_line_id,
            delivery_date,
            customer_no,
            item_no,
            salesperson,
            quantity,
            price,
            amount
        ])

    order_id += 1

# -----------------------------
# SAVE TO CSV
# -----------------------------
df = pd.DataFrame(rows, columns=[
    "OrderId",
    "OrderLineId",
    "DeliveryDate",
    "CustomerNo",
    "ItemNo",
    "Salesperson",
    "Quantity",
    "Price",
    "Amount"
])

# df.to_csv("c:\\Users2\\jorgen\\PBI\\sales_2025_2026.csv", sep=";", index=False)
# df.to_csv("/lakehouse/default/Files/sales_2025_2026.csv", sep=";", index=False)
# df.to_csv("sales_2025_2026.csv", sep=";", index=False)
df.to_delta("/lakehouse/default/Tables/sales_2025_2026.csv", sep=";", index=False)

print("CSV file 'sales_2025_2026.csv' created with", len(df), "rows.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
