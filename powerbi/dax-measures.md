# Power BI DAX Measures — Online Retail

Create a dedicated measures table in Power BI and add the following measures.

```DAX
Total Revenue =
SUM ( FactSales[revenue] )

Total Units =
SUM ( FactSales[quantity] )

Total Orders =
DISTINCTCOUNT ( FactSales[invoice_no] )

Known Customers =
DISTINCTCOUNT ( FactSales[customer_key] )

Products Sold =
DISTINCTCOUNT ( FactSales[product_key] )

Average Order Value =
DIVIDE ( [Total Revenue], [Total Orders] )

Revenue per Customer =
DIVIDE ( [Total Revenue], [Known Customers] )

Average Units per Order =
DIVIDE ( [Total Units], [Total Orders] )

Revenue Previous Month =
CALCULATE ( [Total Revenue], DATEADD ( DimDate[date], -1, MONTH ) )

Revenue MoM Change =
[Total Revenue] - [Revenue Previous Month]

Revenue MoM % =
DIVIDE ( [Revenue MoM Change], [Revenue Previous Month] )

Revenue Previous Year =
CALCULATE ( [Total Revenue], DATEADD ( DimDate[date], -1, YEAR ) )

Revenue YoY Change =
[Total Revenue] - [Revenue Previous Year]

Revenue YoY % =
DIVIDE ( [Revenue YoY Change], [Revenue Previous Year] )

Revenue YTD =
TOTALYTD ( [Total Revenue], DimDate[date] )

Orders YTD =
TOTALYTD ( [Total Orders], DimDate[date] )

Customer Rank by Revenue =
RANKX ( ALL ( DimCustomer[customer_key] ), [Total Revenue], , DESC, DENSE )

Product Rank by Revenue =
RANKX ( ALL ( DimProduct[product_key] ), [Total Revenue], , DESC, DENSE )

Revenue % of Total =
DIVIDE (
    [Total Revenue],
    CALCULATE ( [Total Revenue], REMOVEFILTERS ( DimProduct ) )
)
```

## Formatting

- Revenue measures: Currency, 2 decimals.
- Percentage measures: Percentage, 1–2 decimals.
- Units/orders/customers/products: Whole number.

## Notes

The source dataset covers roughly one year, so year-over-year comparisons will only be meaningful where matching prior-year dates exist. Month-over-month analysis is more broadly applicable to this dataset.
