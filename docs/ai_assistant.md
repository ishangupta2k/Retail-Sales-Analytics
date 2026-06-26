# AI Assistant

This project uses a grounded assistant in `scripts/assistant.py`.

## What It Proves

- Tool/function-calling design: user questions route to approved analysis functions.
- Grounding: answers come from SQLite query results, not made-up text.
- Refusal behavior: unsupported questions return a limitation message.
- Evaluation: `tests/evaluate_assistant.py` checks expected tools and refusals.

## How It Works

The assistant has a registry of approved tools:

```python
TOOLS = {
    "revenue_by_department": revenue_by_department,
    "top_selling_items": top_selling_items,
    "daily_sales_trend": daily_sales_trend,
    "stockout_risk": stockout_risk,
    "missing_inventory": missing_inventory,
}
```

`choose_tool(question)` selects one tool from the question text.

`answer_question(question)` runs the tool and formats the returned rows.

If the question asks for unavailable data, such as profit margin or customer baskets, the assistant refuses instead of guessing.

## Example

```bash
python3 scripts/assistant.py "Which departments have the most revenue?"
```

The answer includes:

```text
Tool used: revenue_by_department
```

That line is important because it tells an interviewer which grounded data function produced the answer.

## Design Choice

The assistant is deterministic by design: questions route to a fixed set of approved, SQL-backed tools rather than to a live large language model. This keeps every answer grounded in query results, reproducible, and runnable with no API key or external dependency.
