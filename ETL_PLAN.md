# ETL Pipeline Plan

Extract and transform rental data from Google Sheets (2017-2025) into a normalized format.

**Data is pulled live** - no files stored. Transform happens on-the-fly when dashboard loads.

---

## Output Schema

### Reservation

| Field | Type | Description |
|-------|------|-------------|
| `year` | int | Calendar year |
| `platform` | str | `airbnb`, `vrbo`, `owner`, `offline` |
| `platform_raw` | str | Original value |
| `check_in` | date | Check-in date |
| `check_out` | date | Check-out date |
| `nights` | int | Number of nights |
| `guest_name` | str | Guest name |
| `guest_count` | int | Number of guests |
| `total_revenue` | float | Total received (USD) |
| `cleaning_fee` | float | Cleaning fee (USD) |
| `is_rental` | bool | True if rental, False if owner use |

### Expense

| Field | Type | Description |
|-------|------|-------------|
| `year` | int | Calendar year |
| `expense_type` | str | Category |
| `amount` | float | Amount (USD) |

---

## Project Structure

```
etl/
├── __init__.py
├── config/
│   ├── __init__.py
│   ├── spreadsheets.py      # Spreadsheet IDs and sheet names
│   ├── columns.py           # Column index mappings per year
│   ├── platforms.py         # Platform normalization rules
│   └── expenses.py          # Expense category normalization
├── extract/
│   ├── __init__.py
│   ├── client.py            # Google Sheets client
│   ├── rentals.py           # Extract rentals data
│   └── expenses.py          # Extract expenses data
├── transform/
│   ├── __init__.py
│   ├── reservation.py       # Transform single reservation
│   ├── parsers.py           # Currency, date parsing
│   └── normalize.py         # Platform normalization
├── models/
│   ├── __init__.py
│   ├── reservation.py       # Reservation Pydantic model
│   └── expense.py           # Expense Pydantic model
└── pipeline.py              # Orchestration (returns transformed data)

tests/
├── conftest.py              # Fixtures
├── transform/
│   ├── test_parsers.py
│   ├── test_normalize.py
│   └── test_reservation.py
├── test_models.py
└── test_data_integrity.py
```

---

## Implementation Phases

### Phase 1: Config files
- `config/spreadsheets.py`
- `config/columns.py`
- `config/platforms.py`

### Phase 2: Models
- `models/reservation.py`
- `models/expense.py`

### Phase 3: Extract
- `extract/client.py`
- `extract/rentals.py`
- `extract/expenses.py`

### Phase 4: Transform
- `transform/parsers.py`
- `transform/normalize.py`
- `transform/reservation.py`

### Phase 5: Pipeline
- `pipeline.py`

### Phase 6: Tests
- Unit tests for parsers and normalization
- Model validation tests
- Data integrity/snapshot tests

