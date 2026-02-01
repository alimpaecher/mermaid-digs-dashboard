# Dashboard Plan

Replace current single-year dashboard with multi-year dashboard powered by ETL pipeline.

---

## Pages

### 1. Overview (Home)
- Year selector (dropdown or tabs)
- Key metrics cards: Total Revenue, Expenses, Net Income, Nights Rented
- Income vs Expenses bar chart
- Nights breakdown pie chart (Rented / Owner / Unoccupied)

### 2. Historical Trends
- Multi-year revenue line chart (2017-2025)
- Multi-year expense line chart
- Year-over-year comparison table
- Average nightly rate trend

### 3. Reservations
- Year filter
- Platform filter (Airbnb, VRBO, Offline, All)
- Reservations table with sorting
- Platform breakdown bar chart
- Monthly booking heatmap

### 4. Expenses
- Year filter
- Expense breakdown pie chart
- Category comparison across years
- Top expense categories table

---

## File Structure

```
app.py                    # Main entry, page routing
pages/
├── __init__.py
├── overview.py           # Overview page
├── trends.py             # Historical trends page
├── reservations.py       # Reservations page
└── expenses.py           # Expenses page
components/
├── __init__.py
├── metrics.py            # Metric card components
├── charts.py             # Chart components
└── filters.py            # Filter components
```

---

## Implementation Steps

### Phase 1: Setup & Overview Page
1. Refactor app.py to use ETL pipeline
2. Create basic page structure with sidebar navigation
3. Build Overview page with year selector and key metrics
4. Add income/expense chart and nights pie chart

### Phase 2: Reservations Page
5. Create reservations page with filters
6. Add reservations table
7. Add platform breakdown chart

### Phase 3: Historical Trends Page
8. Create trends page
9. Add multi-year revenue/expense line charts
10. Add year-over-year comparison table

### Phase 4: Expenses Page
11. Create expenses page
12. Add expense breakdown charts
13. Add category comparison

---

## Data Caching

Use Streamlit's `@st.cache_data` with TTL to cache ETL results:

```python
@st.cache_data(ttl=300)  # 5 minute cache
def load_data():
    return extract_and_transform()
```

---

## Questions

1. Should the dashboard default to current year or show all years?
2. Any specific metrics you want highlighted?
3. Preferred color scheme?
