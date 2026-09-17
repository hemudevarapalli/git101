"""Validation checks for generated Power BI star-schema files."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "data" / "powerbi"

fact = pd.read_csv(DIR / "fact_sales.csv")
date = pd.read_csv(DIR / "dim_date.csv")
product = pd.read_csv(DIR / "dim_product.csv")
customer = pd.read_csv(DIR / "dim_customer.csv")
country = pd.read_csv(DIR / "dim_country.csv")

checks = {
    "fact_has_rows": len(fact) > 0,
    "fact_sales_line_key_unique": fact["sales_line_key"].is_unique,
    "date_key_unique": date["date_key"].is_unique,
    "product_key_unique": product["product_key"].is_unique,
    "customer_key_unique": customer["customer_key"].is_unique,
    "country_key_unique": country["country_key"].is_unique,
    "all_fact_dates_match_dim": fact["date_key"].isin(date["date_key"]).all(),
    "all_fact_products_match_dim": fact["product_key"].isin(product["product_key"]).all(),
    "all_fact_countries_match_dim": fact["country_key"].isin(country["country_key"]).all(),
    "positive_quantities": (fact["quantity"] > 0).all(),
    "positive_unit_prices": (fact["unit_price"] > 0).all(),
    "positive_revenue": (fact["revenue"] > 0).all(),
    "revenue_math_valid": ((fact["quantity"] * fact["unit_price"] - fact["revenue"]).abs() < 1e-6).all(),
}

failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(f"{'PASS' if ok else 'FAIL'}: {name}")

print("\nModel summary")
print(f"Fact rows: {len(fact):,}")
print(f"Dates: {len(date):,}")
print(f"Products: {len(product):,}")
print(f"Known customers: {len(customer):,}")
print(f"Countries: {len(country):,}")
print(f"Revenue: £{fact['revenue'].sum():,.2f}")
print(f"Orders: {fact['invoice_no'].nunique():,}")

if failed:
    raise SystemExit("Validation failed: " + ", ".join(failed))
print("\nAll Power BI model validation checks passed.")
