# expense-tracker

Track daily expenses from the terminal — zero-dependency Python CLI.

## Install

Requires Python 3.8+; no third-party packages.

```bash
git clone https://github.com/heyzcx/expense-tracker.git
cd expense-tracker
chmod +x expense.py
```

## Usage

Record an expense (amount, category, optional note):

```bash
./expense.py add 12.50 food "lunch with colleagues"
./expense.py add 3.20 transport --date 2026-11-20
```

List expenses, optionally filtered by month:

```bash
./expense.py list
./expense.py list --month 2026-11
```

Show totals by category, with each category's share:

```bash
./expense.py summary
./expense.py summary --month 2026-11
```

List the categories you have used:

```bash
./expense.py categories
```

## Data

Expenses are stored as plain CSV (`date,amount,category,note`) in
`expenses.csv` in the current directory. Use `--file` to point at another
file, e.g. `./expense.py --file ~/expenses.csv list`. The CSV is yours to
open in a spreadsheet, back up, or sync however you like.

## Example

```bash
$ ./expense.py add 12.50 food "lunch"
Added 12.50 [food] lunch
$ ./expense.py add 3.20 transport "bus"
Added 3.20 [transport] bus
$ ./expense.py summary
Summary (all time)
  food            12.50  (79.6%)
  transport        3.20  (20.4%)
  TOTAL           15.70
```
