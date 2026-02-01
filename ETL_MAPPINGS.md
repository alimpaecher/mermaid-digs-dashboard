# Transformation Rules

## Platform Normalization

| Raw Value | Platform | Notes |
|-----------|----------|-------|
| `Airbnb` | `airbnb` | |
| `AirBnB` | `airbnb` | Case variation |
| `VRBO` | `vrbo` | |
| `HomeAway` | `vrbo` | Same company |
| `Self` | `owner` | Owner use |
| `Friend` | `owner` | Friends/family stay |
| `Offline` | `offline` | Direct booking |

### Rental Classification

```
is_rental = True if:
  - platform in [airbnb, vrbo, offline]
  - guest_name does NOT contain "Blocked"
```

---

## Column Mappings

### 2024-2025

| Index | Field |
|-------|-------|
| 0 | platform |
| 1 | check_in |
| 2 | check_out |
| 3 | nights |
| 4 | guest_name |
| 5 | guest_count |
| 13 | total_revenue |
| 14 | cleaning_fee |

### 2022-2023

| Index | Field |
|-------|-------|
| 0 | platform |
| 1 | check_in |
| 2 | check_out |
| 3 | nights |
| 4 | guest_name |
| 5 | guest_count |
| 12 | total_revenue |
| 14 | cleaning_fee |

### 2021

| Index | Field |
|-------|-------|
| 0 | platform |
| 1 | check_in |
| 2 | check_out |
| 3 | nights |
| 4 | guest_name |
| 5 | guest_count |
| 10 | total_revenue |
| 12 | cleaning_fee |

### 2019-2020

| Index | Field |
|-------|-------|
| 0 | platform |
| 1 | check_in |
| 2 | check_out |
| 3 | nights |
| 4 | guest_name |
| 5 | guest_count |
| 12 | total_revenue |
| 14 | cleaning_fee |

### 2018

Note: Headers are in row 2, data starts row 3.

| Index | Field |
|-------|-------|
| 1 | platform |
| 2 | check_in |
| 3 | check_out |
| 4 | nights |
| 5 | guest_name |
| 6 | guest_count |
| 11 | total_revenue |
| - | cleaning_fee (not available) |

### 2017

Note: Headers are in row 2, data starts row 3. No platform column.

| Index | Field |
|-------|-------|
| - | platform (default to `offline`) |
| 0 | check_in |
| 1 | check_out |
| 2 | nights |
| 3 | guest_name |
| - | guest_count (not available) |
| 11 | total_revenue |
| - | cleaning_fee (not available) |

---

## Date Formats

Observed formats in source data:

- `1-Jan-25` → `2025-01-01`
- `1-Jan-2025` → `2025-01-01`
- `15-Feb-24` → `2024-02-15`
- `9/Jun/17` → `2017-06-09` (2017 format)

---

## Currency Parsing

| Input | Output |
|-------|--------|
| `$1,234.56` | `1234.56` |
| `$1,234` | `1234.0` |
| `-$500` | `-500.0` |
| `$0` | `0.0` |
| `` (empty) | `0.0` |

---

## Expense Category Normalization

| Raw Values | Normalized |
|------------|------------|
| `Wifi & cable`, `Internet & Wifi` | `internet` |
| `Association`, `Assocation` | `association` |
| `Outdoors`, `Yard`, `Garden` | `outdoor` |
| `Heat/AC system`, `HVAC`, `Heat (oil)`, `Heat & hot water` | `heating` |
| `Appliance`, `Appliances` | `appliances` |
| `Furniture`, `Furniture & household` | `furniture` |
| `Cleaning `, `Cleaning` | `cleaning` |
| `Outdoors ` | `outdoor` |
| `Rental taxes (MA)`, `Taxes` | `taxes` |

Categories that stay as-is:
- `Mortgage & taxes`
- `Electric`
- `Renting`
- `Plumbing`
- `Water`
- `Windows`
- `Linens`
- `Floors`
- `Insulation`
- `Pest control`
- `Bathroom`
- `Painting`, `Interior painting`
- `Trash & recycling`
- `Kitchen`
- `Basement`
- `Septic pumping`
- `Decor`
- `Fireplace`
- `Chimney`
- `Tools`
- `Garage`
- `Bedding & towels`
- `HomeAway/VRBO`
- `Repairs`
- `Other`

---

## Data Integrity Expectations

| Year | Est. Rows | Est. Revenue |
|------|-----------|--------------|
| 2025 | ~33 | ~$45,000 |
| 2024 | ~38 | ~$61,400 |
| 2023 | ~36 | ~$59,200 |
| 2022 | ~37 | ~$64,500 |
| 2021 | ~43 | ~$61,400 |
| 2020 | ~20 | ~$14,000 |
| 2019 | ~42 | ~$40,000 |
| 2018 | ~30 | TBD |
| 2017 | ~22 | TBD |
