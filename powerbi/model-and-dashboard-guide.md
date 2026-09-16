# Power BI Model & Dashboard Guide — Online Retail

## 1. Generate the model files

Run the cleaning/EDA notebook first so `data/processed/online_retail_clean.csv` exists, then run:

```bash
python src/build_powerbi_model.py
```

This creates:

- `data/powerbi/fact_sales.csv`
- `data/powerbi/dim_date.csv`
- `data/powerbi/dim_product.csv`
- `data/powerbi/dim_customer.csv`
- `data/powerbi/dim_country.csv`

## 2. Import into Power BI

Load all five CSV files. Rename the queries/tables:

- `fact_sales` → `FactSales`
- `dim_date` → `DimDate`
- `dim_product` → `DimProduct`
- `dim_customer` → `DimCustomer`
- `dim_country` → `DimCountry`

Set appropriate types for dates, whole numbers, decimal numbers, and text keys.

## 3. Star-schema relationships

Create single-direction, one-to-many relationships from dimensions to the fact table:

```text
DimDate[date_key]       1 ───── * FactSales[date_key]
DimProduct[product_key] 1 ───── * FactSales[product_key]
DimCustomer[customer_key] 1 ─── * FactSales[customer_key]
DimCountry[country_key] 1 ───── * FactSales[country_key]
```

`FactSales` is the center of the model. Avoid dimension-to-dimension relationships and avoid bidirectional filtering unless a specific analytical requirement demands it.

Mark `DimDate` as the model's date table using `DimDate[date]`.

Sort:
- `DimDate[month]` by `DimDate[month_number]`
- `DimDate[month_short]` by `DimDate[month_number]`
- `DimDate[year_month]` by `DimDate[year_month_sort]`

## 4. Dashboard pages

### Page 1 — Executive Overview

**KPI cards**
- Total Revenue
- Total Orders
- Known Customers
- Total Units
- Average Order Value

**Visuals**
- Line chart: Revenue by `year_month`
- Column chart: Orders by `year_month`
- Bar chart: Revenue by Country
- Bar chart: Top 10 Products by Revenue
- Slicers: Date, Country

Use conditional KPI context for month-over-month change rather than treating the cards as isolated totals.

### Page 2 — Product Performance

- KPI cards: Revenue, Units, Products Sold
- Top products by revenue
- Top products by units
- Revenue vs units scatter plot by product
- Product detail table: Product, Revenue, Units, Orders
- Product search/filter

Business question: which products drive revenue, volume, or both?

### Page 3 — Customer Analytics

- KPI cards: Known Customers, Revenue per Customer, Average Order Value
- Top customers by revenue
- Customer revenue distribution
- Orders by customer
- Customer detail matrix with Revenue, Orders, Units, AOV
- Country and date slicers

Remember that the cleaned source retains valid transactions with missing customer IDs. Customer-specific visuals should therefore distinguish known-customer analysis from overall sales analysis.

### Page 4 — Geography

- Revenue by country
- Orders by country
- Customers by country
- Revenue contribution percentage
- Country detail table

Because the retailer is UK-based and UK sales dominate, consider a toggle or separate visual for non-UK markets so smaller countries remain interpretable.

### Page 5 — Time & Shopping Patterns

- Revenue by weekday
- Orders by weekday
- Revenue by hour
- Monthly revenue trend
- Monthly AOV trend
- Date hierarchy drill-down

## 5. Recommended report interactions

- Keep date and country slicers consistent across pages.
- Use drill-through from Product and Customer visuals to detail pages if desired.
- Add report-page tooltips for product/customer context.
- Keep cross-filtering purposeful; disable interactions that make visuals confusing.

## 6. Validation

Before styling the dashboard, validate Power BI totals against the notebook KPI snapshot:

- total revenue
- distinct orders
- known customers
- products
- countries
- units sold
- average order value

Any mismatch should be investigated before presentation work begins.

## 7. Portfolio presentation

Export or capture dashboard screenshots into `reports/` and update the repository README with:

1. business problem,
2. dataset/source,
3. cleaning decisions,
4. model diagram,
5. KPI definitions,
6. dashboard screenshots,
7. key findings,
8. limitations and next steps.

This makes the repository useful not only as a Power BI file store, but as an end-to-end analytics portfolio case study.
