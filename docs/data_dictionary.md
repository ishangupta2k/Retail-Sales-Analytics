# Data Dictionary

This project uses two sanitized CSV files:

- `data/sales.csv`: daily item-level sales totals.
- `data/inventory.csv`: one inventory snapshot from `2026-06-23`.

The data is useful for item, department, sales, and inventory analysis. It is not transaction-level customer data.

## `sales.csv`

One row represents one item sold on one business date.

| Column | Plain English meaning | Notes |
|---|---|---|
| `date` | Sales date. | Covers `2026-05-18` through `2026-06-22`, with 35 distinct dates. |
| `scan_code` | Sanitized item identifier. | Use this to join sales to inventory. Keep it as text because leading zeros matter. |
| `description` | Item name or label. | Sanitized/normalized enough for analysis, but descriptions may differ between sales and inventory. |
| `department` | Product department/category. | 51 rows are blank in the current file. |
| `units_sold` | Number of units sold for that item on that date. | Can be zero in some rows. |
| `revenue` | Sales dollars for that item on that date. | Revenue was sanitized/scaled, so use it for relative analysis, not audited financial reporting. |

## `inventory.csv`

One row represents one item in the inventory snapshot dated `2026-06-23`.

| Column | Plain English meaning | Notes |
|---|---|---|
| `date` | Inventory snapshot date. | All rows currently use `2026-06-23`. |
| `scan_code` | Sanitized item identifier. | Use this to join inventory to sales. Keep it as text because leading zeros matter. |
| `description` | Item name or label. | May not exactly match the sales description for the same scan code. |
| `beg_inv` | Beginning inventory count. | Negative values exist and should be treated as exceptions to investigate. |
| `received` | Units received during the inventory period. | Useful for checking whether low stock was replenished. |
| `sold` | Units sold according to the inventory export. | This is from the inventory snapshot/export, not necessarily the same aggregation as `sales.csv`. |
| `on_hand` | Current inventory count. | Negative and low values are useful for stockout-risk analysis. |
| `over_short` | Difference between expected and actual inventory. | Large positive or negative values are inventory-control exceptions. |

## Business Questions This Data Can Answer

- Which departments generated the most revenue?
- Which items sold the most units?
- How did daily revenue and units sold trend over the sales period?
- Which items have negative or very low on-hand inventory?
- Which selling items are missing from the inventory snapshot?
- Which items look overstocked because inventory is high but recent sales are low?
- Which items have large over/short inventory exceptions?
- Which departments or items should a store manager review first?

## Business Questions This Data Cannot Answer

- Customer behavior, baskets, loyalty, or repeat purchases, because there is no customer or receipt ID.
- Profitability, margin, or cost of goods, because cost and margin fields are not present.
- Vendor performance, because vendor fields are not present in these two CSVs.
- Exact real-world revenue, because revenue has been sanitized/scaled.
- Hourly sales patterns, because `sales.csv` is daily.
- Long-term seasonality, because the current sales file covers about five weeks.
- Full inventory movement over time, because `inventory.csv` is one snapshot date.

## Join Notes

- `scan_code` is the safest join key between files.
- There are currently 32 scan codes in sales that are not in inventory.
- There are currently 12,357 scan codes in inventory that are not in sales.
- Do not join on `description`; names can vary for the same item.

## Data Quality Notes

- Treat `scan_code` as text, not a number.
- Blank departments should be labeled as `Uncategorized` in reports or explicitly filtered.
- Negative inventory and large `over_short` values are not cleanup errors by default. They are operational exceptions worth analyzing.
- Revenue is useful for ranked and directional analysis, but the sanitized scale means it should not be presented as audited financial truth.
