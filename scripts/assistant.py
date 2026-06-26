#!/usr/bin/env python3
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "retail.db"


def query(sql, params=()):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = [dict(row) for row in conn.execute(sql, params).fetchall()]
    conn.close()
    return rows


def revenue_by_department(limit=5):
    return query(
        """
        SELECT
            COALESCE(NULLIF(department, ''), 'Uncategorized') AS department,
            ROUND(SUM(revenue), 2) AS total_revenue,
            SUM(units_sold) AS total_units
        FROM sales
        GROUP BY COALESCE(NULLIF(department, ''), 'Uncategorized')
        ORDER BY total_revenue DESC
        LIMIT ?;
        """,
        (limit,),
    )


def top_selling_items(limit=5):
    return query(
        """
        SELECT
            scan_code,
            MAX(description) AS sample_description,
            COALESCE(NULLIF(department, ''), 'Uncategorized') AS department,
            SUM(units_sold) AS total_units,
            ROUND(SUM(revenue), 2) AS total_revenue
        FROM sales
        GROUP BY scan_code, COALESCE(NULLIF(department, ''), 'Uncategorized')
        ORDER BY total_units DESC, total_revenue DESC
        LIMIT ?;
        """,
        (limit,),
    )


def daily_sales_trend(limit=5):
    return query(
        """
        SELECT
            date,
            SUM(units_sold) AS total_units,
            ROUND(SUM(revenue), 2) AS total_revenue
        FROM sales
        GROUP BY date
        ORDER BY date
        LIMIT ?;
        """,
        (limit,),
    )


def stockout_risk(limit=5):
    return query(
        """
        SELECT
            i.scan_code,
            i.description,
            i.on_hand,
            SUM(s.units_sold) AS recent_units_sold,
            ROUND(SUM(s.revenue), 2) AS recent_revenue
        FROM inventory i
        JOIN sales s ON s.scan_code = i.scan_code
        WHERE i.on_hand <= 5
        GROUP BY i.scan_code, i.description, i.on_hand
        HAVING SUM(s.units_sold) > 0
        ORDER BY i.on_hand ASC, recent_units_sold DESC
        LIMIT ?;
        """,
        (limit,),
    )


def missing_inventory(limit=10):
    return query(
        """
        SELECT
            s.scan_code,
            MAX(s.description) AS sample_description,
            COALESCE(NULLIF(s.department, ''), 'Uncategorized') AS department,
            SUM(s.units_sold) AS total_units,
            ROUND(SUM(s.revenue), 2) AS total_revenue
        FROM sales s
        LEFT JOIN inventory i ON i.scan_code = s.scan_code
        WHERE i.scan_code IS NULL
        GROUP BY s.scan_code, COALESCE(NULLIF(s.department, ''), 'Uncategorized')
        ORDER BY total_revenue DESC
        LIMIT ?;
        """,
        (limit,),
    )


TOOLS = {
    "revenue_by_department": revenue_by_department,
    "top_selling_items": top_selling_items,
    "daily_sales_trend": daily_sales_trend,
    "stockout_risk": stockout_risk,
    "missing_inventory": missing_inventory,
}

LIMITATIONS = (
    "I cannot answer that from this data. The project has daily item-level sales "
    "and one inventory snapshot, but no customer, receipt, cost, margin, vendor, "
    "promotion, staffing, weather, or hourly fields."
)


def choose_tool(question):
    q = question.lower()
    if any(word in q for word in ["profit", "margin", "customer", "receipt", "basket", "hourly", "vendor", "weather", "promotion", "staff"]):
        return None
    if "missing" in q and "inventory" in q:
        return "missing_inventory"
    if "stockout" in q or ("low" in q and "inventory" in q) or "risk" in q:
        return "stockout_risk"
    if "daily" in q or "trend" in q or "date" in q:
        return "daily_sales_trend"
    if "top" in q or "best" in q or "selling item" in q or "items" in q:
        return "top_selling_items"
    if "department" in q or "revenue" in q or "sales" in q:
        return "revenue_by_department"
    return None


def format_answer(tool_name, rows):
    if not rows:
        return f"Tool used: {tool_name}\nNo matching rows found."
    headers = list(rows[0])
    lines = ["Tool used: " + tool_name, "Result:"]
    lines.append(" | ".join(headers))
    lines.append(" | ".join("---" for _ in headers))
    for row in rows:
        lines.append(" | ".join(str(row[h]) for h in headers))
    return "\n".join(lines)


def answer_question(question):
    if not DB_PATH.exists():
        return "Database not found. Run: python3 scripts/load_sqlite.py"
    tool_name = choose_tool(question)
    if tool_name is None:
        return LIMITATIONS
    return format_answer(tool_name, TOOLS[tool_name]())


def main():
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        question = input("Ask a retail data question: ").strip()
    print(answer_question(question))


if __name__ == "__main__":
    main()
