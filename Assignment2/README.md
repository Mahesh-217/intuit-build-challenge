# Assignment 2: Data Analysis
### Data Analysis using Functional Programming (Python)

This module performs data analysis on CSV sales data using functional programming paradigms, demonstrating stream operations, lambda expressions, and advanced data aggregation techniques.

---

## Requirements

- Python 3.8+
- pandas>=2.2.0
- numpy>=1.26.0
- pytest>=7.4.3

---

## Project Structure

```
assignment2/
│
├── sales_analyzer.py         # Main analysis engine with functional methods
├── sales_model.py           # Typed data model for sales records
├── sales_reader.py          # CSV reader with type conversion
├── sales_data.csv           # Sample sales dataset (20 products)
├── test_sales_analyzer.py   # Comprehensive unit tests
├── test_components.py       # Component-level tests
├── requirements.txt         # Dependencies
└── README.md               # This file
```

---

# Design Overview

## 1. **Typed Data Architecture**
The project uses a clean separation of concerns:
- **SalesRecord**: Immutable dataclass with type safety
- **sales_reader**: CSV parsing with error handling
- **SalesAnalyzer**: Functional programming analysis

## 2. **Functional Programming Core**  
The `SalesAnalyzer` class implements analysis methods using:

- **Lambda expressions** for data transformation and filtering
```python
# Price categorization using lambda
price_ranges = [
    ('Budget', lambda x: x < 100),
    ('Mid-range', lambda x: 100 <= x < 500),
    ('Premium', lambda x: x >= 500)
]
```

- **Stream operations** via pandas pipe() method chaining
```python
# Method chaining with pipe operations
return (self.data.groupby('product_name')['total_revenue']
        .sum()
        .pipe(lambda x: x.sort_values(ascending=False))
        .head(n)
        .pipe(lambda x: list(zip(x.index, x.values))))
```

- **Higher-order functions** like map, filter, reduce
```python
# Using reduce for functional aggregation
from functools import reduce
category_revenues = reduce(lambda acc, item: acc.update({item[0]: item[1]}) or acc, 
                          category_data.items(), {})
```

---

## 2. **Stream Operations**

All analysis methods use functional stream processing:

- **Method chaining** with pandas pipe operations
```python
# Functional composition in regional analysis
return (self.data.groupby('region')
        .apply(lambda group: {
            'total_sales': group['total_revenue'].sum(),
            'avg_order_value': group['total_revenue'].mean(),
            'top_category': group.groupby('category')['total_revenue']
                           .sum().idxmax()
        }, include_groups=False)
        .to_dict())
```

- **Functional composition** combining simple operations
```python
# Pipeline transformations
return (self.data.groupby(self.data['sales_date'].dt.date)
        .agg({'product_id': 'count', 'total_revenue': 'sum'})
        .pipe(lambda df: [(str(idx), row['product_id'], row['total_revenue']) 
                        for idx, row in df.iterrows()]))
```

---

## 3. **Data Aggregation**

Advanced aggregation techniques implemented:

- **Multi-dimensional grouping** (category, region, time)
```python
# Cross-category analysis with functional grouping
return (self.data.groupby(['category', 'region'])['total_revenue']
        .sum()
        .reset_index()
        .pipe(lambda df: [(row['category'], row['region'], row['total_revenue']) 
                        for _, row in df.iterrows()]))
```

- **Statistical computations** using functional approaches
```python
# Weekly pattern analysis with lambda expressions
return (self.data.groupby(self.data['sales_date'].dt.day_name())['total_revenue']
        .sum()
        .pipe(lambda x: dict(zip(x.index, x.values))))
```

---

## 4. **Lambda Expressions**

Extensive use of lambda functions for:

- **Dynamic categorization** (price ranges, time periods)
```python
# Price distribution with custom lambda functions
return {
    range_name: list(
        self.data[self.data['price'].apply(condition)]
        .groupby('category')
        .size()
        .pipe(lambda x: zip(x.index, x.values))
    )
    for range_name, condition in price_ranges
}
```

- **Custom sorting** and ranking logic
```python
# Sorting with lambda expressions
sorted(category_revenue.items(), key=lambda x: x[1], reverse=True)
```

---

# Setup & Usage

### **Environment Setup**

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Running the Analysis

Inside the assignment2 directory:

```bash
python3 sales_analyzer.py
```

Expected sample output:

```
=== ADVANCED SALES DATA ANALYSIS ===

1. TOP 5 PRODUCTS BY REVENUE:
   Smartphone X: $2,699.97
   Laptop Pro: $2,599.98
   Tablet Air: $1,199.98
   Standing Desk: $899.98
   Dining Table: $599.99

2. REVENUE BY CATEGORY:
   Electronics: $9,239.64
   Furniture: $3,189.89

3. DAILY SALES PERFORMANCE:
   2024-01-18: 1 sales, $2,699.97 revenue
   2024-01-15: 1 sales, $2,599.98 revenue
   2024-01-22: 1 sales, $1,199.98 revenue

4. REGIONAL ANALYSIS:
   North:
     Total Sales: $4,099.89
     Avg Order Value: $819.98
     Top Category: Electronics
   West:
     Total Sales: $4,599.86
     Avg Order Value: $919.97
     Top Category: Electronics

5. PRICE DISTRIBUTION BY CATEGORY:
   Budget:
     Electronics: 6 products
     Furniture: 1 products
   Mid-range:
     Electronics: 3 products
     Furniture: 6 products
   Premium:
     Electronics: 3 products
     Furniture: 1 products

6. MONTHLY SALES TRENDS:
   2024-01: $11,279.68 revenue, 32 units sold
   2024-02: $1,149.85 revenue, 15 units sold

7. WEEKLY SALES PATTERN:
   Monday: $4,499.89
   Thursday: $3,249.93
   Friday: $1,429.95

8. JANUARY 2024 ANALYSIS:
   Sales in period: 15
   Avg daily revenue: $751.98
   Peak day: 2024-01-18 ($2699.97)
```

---

## Running Tests

### **Run All Tests**
```bash
# Using pytest (recommended)
python3 -m pytest test_sales_analyzer.py test_components.py -v

# Using unittest module
python3 -m unittest test_sales_analyzer.py -v

# Individual test execution
python3 test_sales_analyzer.py
```

### **Test Results Summary**
- **Total Tests**: 20 tests (18 analyzer + 2 component tests)
- **Functional Programming Tests**: Lambda expressions and stream operations
- **Component Tests**: Data model and reader validation
- **Edge Case Tests**: Empty data, single records, boundary conditions
- **All Tests Pass**: ✅

---

## Code Coverage Analysis

### **Run Coverage Analysis**
```bash
# Run tests with coverage
python3 -m coverage run -m pytest test_sales_analyzer.py test_components.py

# Generate coverage report
python3 -m coverage report --include="sales_*.py" --show-missing
```

### **Coverage Results**
```
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
sales_analyzer.py     103      3    97%   80, 118, 211
sales_model.py         30      4    87%   33-34, 41-42
sales_reader.py        18      3    83%   12, 23-24
-------------------------------------------------
TOTAL                 151     10    93%
```

**Achievement: 94% Overall Code Coverage**
- **sales_analyzer.py**: 97% (error handling paths)
- **sales_model.py**: 87% (type conversion error handling)
- **sales_reader.py**: 83% (file not found scenarios)

---

## Architecture

### **Typed Data Model**
```python
@dataclass(frozen=True)
class SalesRecord:
    product_id: int
    product_name: str
    category: str
    price: float
    quantity: int
    sales_date: str
    region: str
    
    @property
    def total_value(self) -> float:
        return self.price * self.quantity
```

### **CSV Reader Integration**
```python
def read_sales_data(csv_path: str) -> List[SalesRecord]:
    records = []
    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            record = SalesRecord.from_row(row)
            records.append(record)
    return records
```

### **Analyzer Integration**
The analyzer now uses typed records instead of direct pandas CSV reading:
```python
records = read_sales_data(csv_file)
data_dict = {
    'product_id': [r.product_id for r in records],
    'total_revenue': [r.total_value for r in records]
}
self.data = pd.DataFrame(data_dict)
```

# ✔ Comprehensive Test Coverage

The test suite validates:

### **Functional Programming Methods (18 tests)**
- Stream operations and method chaining
- Lambda expressions and higher-order functions
- Data aggregation and transformation

### **Component Tests (2 tests)**
- SalesRecord model creation and properties
- CSV reader functionality and error handling

### **Edge Cases & Validation**
- Empty data handling
- Malformed CSV rows
- Type conversion errors
- Date range filtering