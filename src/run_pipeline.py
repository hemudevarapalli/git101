"""End-to-end Online Retail pipeline: download, clean, model, and validate."""
from pathlib import Path
from urllib.request import urlretrieve
import subprocess
import sys
import zipfile
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
RAW.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)
ZIP = RAW / "online_retail.zip"
XLSX = RAW / "Online Retail.xlsx"
CLEAN = PROCESSED / "online_retail_clean.csv"
URL = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"

if not XLSX.exists():
    print("Downloading UCI Online Retail...")
    urlretrieve(URL, ZIP)
    with zipfile.ZipFile(ZIP) as zf:
        zf.extractall(RAW)

raw = pd.read_excel(XLSX)
raw.columns = ["invoice_no", "stock_code", "description", "quantity", "invoice_date", "unit_price", "customer_id", "country"]
for col in ["invoice_no", "stock_code", "description", "country"]:
    raw[col] = raw[col].astype("string").str.strip()
raw["invoice_date"] = pd.to_datetime(raw["invoice_date"], errors="coerce")
raw["customer_id"] = pd.to_numeric(raw["customer_id"], errors="coerce").astype("Int64").astype("string")

clean = raw.drop_duplicates().copy()
clean["is_cancellation"] = clean["invoice_no"].str.startswith("C", na=False)
clean = clean.loc[(~clean["is_cancellation"]) & (clean["quantity"] > 0) & (clean["unit_price"] > 0) & clean["description"].notna() & clean["invoice_date"].notna()].copy()
clean["revenue"] = clean["quantity"] * clean["unit_price"]
clean["date"] = clean["invoice_date"].dt.date
clean["year"] = clean["invoice_date"].dt.year
clean["month"] = clean["invoice_date"].dt.month
clean["month_name"] = clean["invoice_date"].dt.month_name().str[:3]
clean["year_month"] = clean["invoice_date"].dt.to_period("M").astype(str)
clean["day_of_week"] = clean["invoice_date"].dt.day_name()
clean["hour"] = clean["invoice_date"].dt.hour
clean.to_csv(CLEAN, index=False)

print(f"Raw rows: {len(raw):,}")
print(f"Clean sales rows: {len(clean):,}")
print(f"Revenue: £{clean['revenue'].sum():,.2f}")
print(f"Orders: {clean['invoice_no'].nunique():,}")
print(f"Known customers: {clean['customer_id'].nunique():,}")

subprocess.run([sys.executable, str(ROOT / "src" / "build_powerbi_model.py")], check=True)
subprocess.run([sys.executable, str(ROOT / "src" / "validate_powerbi_model.py")], check=True)
