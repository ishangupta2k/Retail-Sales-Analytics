#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "retail.db"


def load_csv(conn, table, path, columns):
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    conn.executemany(
        f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join('?' for _ in columns)})",
        ([row[col] for col in columns] for row in rows),
    )
    return len(rows)


def main():
    DB_PATH.unlink(missing_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(
        """
        CREATE TABLE sales (
            date TEXT NOT NULL,
            scan_code TEXT NOT NULL,
            description TEXT,
            department TEXT,
            units_sold INTEGER NOT NULL,
            revenue REAL NOT NULL
        );

        CREATE TABLE inventory (
            date TEXT NOT NULL,
            scan_code TEXT NOT NULL,
            description TEXT,
            beg_inv INTEGER NOT NULL,
            received INTEGER NOT NULL,
            sold INTEGER NOT NULL,
            on_hand INTEGER NOT NULL,
            over_short INTEGER NOT NULL
        );
        """
    )
    sales_count = load_csv(conn, "sales", ROOT / "data" / "sales.csv", [
        "date", "scan_code", "description", "department", "units_sold", "revenue"
    ])
    inventory_count = load_csv(conn, "inventory", ROOT / "data" / "inventory.csv", [
        "date", "scan_code", "description", "beg_inv", "received", "sold", "on_hand", "over_short"
    ])
    conn.commit()

    assert conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0] == sales_count
    assert conn.execute("SELECT COUNT(*) FROM inventory").fetchone()[0] == inventory_count
    conn.close()
    print(f"Loaded {sales_count:,} sales rows and {inventory_count:,} inventory rows into {DB_PATH}")


if __name__ == "__main__":
    main()
