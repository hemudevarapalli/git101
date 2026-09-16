"""Build Power BI-ready star-schema CSVs from the cleaned Online Retail dataset."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "processed" / "online_retail_clean.csv"
OUTPUT = ROOT / "data" / "powerbi"
OUTPUT.mkdir(parents=True, exist_ok=True)

sales = pd.read_csv(INPUT, parse_dates=["invoice_date"])
sales["date"] = sales["invoice_date"].dt.normalize()

# Dimensions
products = (sales[["stock_code", "description"]]
            .dropna(subset=["stock_code"])
            .sort_values(["stock_code", "description"])
            .drop_duplicates("stock_code", keep="last")
            .rename(columns={"stock_code": "product_key", "description": "product_name"}))

customers = (sales[["customer_id"]]
             .dropna()
             .drop_duplicates()
             .rename(columns={"customer_id": "customer_key"}))

countries = pd.DataFrame({"country": sorted(sales["country"].dropna().unique())})
countries.insert(0, "country_key", range(1, len(countries) + 1))

min_date = sales["date"].min()
max_date = sales["date"].max()
dates = pd.DataFrame({"date": pd.date_range(min_date, max_date, freq="D")})
dates["date_key"] = dates["date"].dt.strftime("%Y%m%d").astype(int)
dates["year"] = dates["date"].dt.year
dates["quarter"] = "Q" + dates["date"].dt.quarter.astype(str)
dates["month_number"] = dates["date"].dt.month
dates["month"] = dates["date"].dt.month_name()
dates["month_short"] = dates["date"].dt.month_name().str[:3]
dates["year_month"] = dates["date"].dt.strftime("%Y-%m")
dates["year_month_sort"] = dates["date"].dt.year * 100 + dates["date"].dt.month
dates["day"] = dates["date"].dt.day
dates["day_of_week_number"] = dates["date"].dt.dayofweek + 1
dates["day_of_week"] = dates["date"].dt.day_name()
dates["is_weekend"] = dates["date"].dt.dayofweek >= 5

# Fact table
fact = sales[["invoice_no", "invoice_date", "date", "stock_code", "customer_id",
              "country", "quantity", "unit_price", "revenue"]].copy()
fact["date_key"] = fact["date"].dt.strftime("%Y%m%d").astype(int)
fact = fact.merge(countries, on="country", how="left")
fact = fact.rename(columns={"stock_code": "product_key", "customer_id": "customer_key"})
fact.insert(0, "sales_line_key", range(1, len(fact) + 1))
fact = fact[["sales_line_key", "invoice_no", "invoice_date", "date_key", "product_key",
             "customer_key", "country_key", "quantity", "unit_price", "revenue"]]

# Export
fact.to_csv(OUTPUT / "fact_sales.csv", index=False)
products.to_csv(OUTPUT / "dim_product.csv", index=False)
customers.to_csv(OUTPUT / "dim_customer.csv", index=False)
countries.to_csv(OUTPUT / "dim_country.csv", index=False)
dates.to_csv(OUTPUT / "dim_date.csv", index=False)

print("Power BI star schema exported to", OUTPUT)
for path in sorted(OUTPUT.glob("*.csv")):
    print(f"  {path.name}: {path.stat().st_size / 1024:.1f} KB")
