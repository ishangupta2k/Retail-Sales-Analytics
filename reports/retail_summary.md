# Retail Sales Summary Report

This report is a dashboard-style summary built from `data/retail.db`.

## Key Performance Indicators

| Metric | Value |
|---|---:|
| Sanitized revenue | `146,819.68` |
| Units sold | `47,516` |
| Sales days | `35` |
| Sold scan codes | `2,119` |
| Inventory items | `14,444` |
| Low or negative inventory items | `12,883` |
| Over/short exceptions `>= 10` units | `1,328` |
| Sold scan codes missing from inventory | `32` |

## Dashboard Sections

### Sales Performance

Purpose: show where revenue and units are coming from.

Views:

- Revenue by department
- Top-selling items
- Daily sales trend

### Inventory Risk

Purpose: show where operations should investigate stock and count issues.

Views:

- Low or negative inventory
- Stockout-risk items
- Inventory over/short exceptions

### Master Data Gaps

Purpose: show where sales and inventory files do not line up.

Views:

- Items sold but missing from inventory
- Inventory items with no sales in the sales window

## Sample Insights

- `BEER & WINE` is the highest-revenue department in the current sales file.
- `2026-05-21` is the highest-revenue sales date in the current data.
- There are `32` sold scan codes missing from the inventory snapshot.
- Low or negative inventory is widespread in the snapshot, so inventory exception analysis should be treated as an operational review, not automatic cleanup.

## Source Queries

The metrics and views come from:

- `sql/analysis_queries.sql`
- `scripts/load_sqlite.py`

Run:

```bash
python3 scripts/load_sqlite.py
sqlite3 data/retail.db < sql/analysis_queries.sql
```

## Tableau Public Dashboard

Live: **https://public.tableau.com/views/RetailSalesAnalytics_17825124731470/RetailSalesPerformanceDepartmentRevenueDailyTrend**

Built from `data/sales.csv`, with `scan_code` loaded as text so leading zeros are preserved. The current dashboard contains:

- Bar chart: revenue by department (sorted descending, uncategorized/blank department excluded — Tableau labels it `Null`)
- Line chart: daily sales trend
