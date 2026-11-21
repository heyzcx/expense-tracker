#!/usr/bin/env python3
"""expense-tracker: track daily expenses from the terminal.

Usage:
    expense.py add 12.50 food "lunch with colleagues"
    expense.py add 3.20 transport --date 2026-11-20
    expense.py list
    expense.py list --month 2026-11
    expense.py summary
    expense.py summary --month 2026-11
    expense.py categories

Expenses are stored as CSV (date,amount,category,note) in the file given
by --file (default: expenses.csv in the current directory).
"""

import argparse
import csv
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

HEADERS = ["date", "amount", "category", "note"]


def load_rows(path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r.get("date")]


def save_rows(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS)
        w.writeheader()
        w.writerows(rows)


def valid_month(value):
    try:
        year, month = (int(p) for p in value.split("-"))
        if len(value) != 7 or not 1 <= month <= 12:
            raise ValueError
    except ValueError:
        raise argparse.ArgumentTypeError("month must look like YYYY-MM")
    return value


def cmd_add(args):
    path = Path(args.file)
    rows = load_rows(path)
    rows.append(
        {
            "date": args.date or date.today().isoformat(),
            "amount": f"{args.amount:.2f}",
            "category": args.category,
            "note": args.note or "",
        }
    )
    save_rows(path, rows)
    print(f"Added {args.amount:.2f} [{args.category}] {args.note or ''}".rstrip())


def filter_month(rows, month):
    return rows if month is None else [r for r in rows if r["date"].startswith(month)]


def cmd_list(args):
    rows = filter_month(load_rows(Path(args.file)), args.month)
    if not rows:
        print("No expenses recorded." + (f" for {args.month}." if args.month else ""))
        return
    total = 0.0
    for r in sorted(rows, key=lambda x: x["date"]):
        total += float(r["amount"])
        note = f"  {r['note']}" if r["note"] else ""
        print(f"{r['date']}  {float(r['amount']):>8.2f}  {r['category']:<12}{note}")
    print(f"{'TOTAL':<10}  {total:>8.2f}")


def cmd_summary(args):
    rows = filter_month(load_rows(Path(args.file)), args.month)
    if not rows:
        print("No expenses recorded." + (f" for {args.month}." if args.month else ""))
        return
    by_cat = defaultdict(float)
    for r in rows:
        by_cat[r["category"]] += float(r["amount"])
    total = sum(by_cat.values())
    label = args.month or "all time"
    print(f"Summary ({label})")
    for cat, amount in sorted(by_cat.items(), key=lambda kv: -kv[1]):
        pct = amount / total * 100 if total else 0
        print(f"  {cat:<12} {amount:>8.2f}  ({pct:4.1f}%)")
    print(f"  {'TOTAL':<12} {total:>8.2f}")


def cmd_categories(args):
    rows = load_rows(Path(args.file))
    cats = sorted({r["category"] for r in rows})
    print("\n".join(cats) if cats else "No categories yet.")


def main(argv=None):
    p = argparse.ArgumentParser(description="Track daily expenses from the terminal.")
    p.add_argument("--file", default="expenses.csv", help="CSV file (default: expenses.csv)")
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("add", help="record an expense")
    a.add_argument("amount", type=float, help="amount, e.g. 12.50")
    a.add_argument("category", help="category, e.g. food")
    a.add_argument("note", nargs="?", default="", help="optional note")
    a.add_argument("--date", help="date YYYY-MM-DD (default: today)")
    a.set_defaults(func=cmd_add)

    l = sub.add_parser("list", help="list expenses")
    l.add_argument("--month", type=valid_month, help="filter by month YYYY-MM")
    l.set_defaults(func=cmd_list)

    s = sub.add_parser("summary", help="totals by category")
    s.add_argument("--month", type=valid_month, help="filter by month YYYY-MM")
    s.set_defaults(func=cmd_summary)

    c = sub.add_parser("categories", help="list categories used")
    c.set_defaults(func=cmd_categories)

    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
