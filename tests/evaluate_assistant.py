#!/usr/bin/env python3
import contextlib
import io
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.assistant import answer_question
from scripts.load_sqlite import main as load_sqlite


class AssistantEvaluation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with contextlib.redirect_stdout(io.StringIO()):
            load_sqlite()

    def test_department_revenue_is_grounded(self):
        answer = answer_question("Which departments have the most revenue?")
        self.assertIn("Tool used: revenue_by_department", answer)
        self.assertIn("BEER & WINE", answer)
        self.assertIn("34621.6", answer)

    def test_stockout_risk_uses_inventory_and_sales(self):
        answer = answer_question("What items are stockout risks?")
        self.assertIn("Tool used: stockout_risk", answer)
        self.assertIn("on_hand", answer)
        self.assertIn("recent_units_sold", answer)

    def test_missing_inventory_uses_left_join_tool(self):
        answer = answer_question("Which sold items are missing from inventory?")
        self.assertIn("Tool used: missing_inventory", answer)
        self.assertIn("scan_code", answer)

    def test_refuses_profit_question(self):
        answer = answer_question("What products have the highest profit margin?")
        self.assertIn("I cannot answer that from this data", answer)
        self.assertNotIn("Tool used:", answer)


if __name__ == "__main__":
    unittest.main()
