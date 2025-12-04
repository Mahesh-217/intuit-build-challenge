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
Assignment2/                  # Sales Data Analysis (Functional Programming)
├── sales_model.py           # Typed data model (SalesRecord)
├── sales_reader.py          # CSV parser with error handling
├── sales_analyzer.py        # Main analysis engine + functional methods
├── sales_data.csv           # Sample dataset (20 products)
├── tests/
│   ├── test_sales_analyzer.py   # Core functionality tests
│   └── test_components.py       # Component-level tests
├── requirements.txt         # Dependencies (pandas, numpy, pytest)
└── README.md               # Assignment 2 details
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
cd Assignment2
python3 sales_analyzer.py
```

 Output:

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
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
sales_analyzer.py                103      3    97%   80, 118, 211
sales_model.py                    30      0   100%
sales_reader.py                   18      2    89%   23-24
tests/test_components.py          28      1    96%   48
tests/test_sales_analyzer.py     173      9    95%   39-40, 45-48, 277-279, 285
------------------------------------------------------------
TOTAL                            352     15    96%
```

**Achievement: 94% Overall Code Coverage**
- **sales_analyzer.py**: 97% (error handling paths)
- **sales_model.py**: 100% (type conversion error handling)
- **sales_reader.py**: 89% (file not found scenarios)

---

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
