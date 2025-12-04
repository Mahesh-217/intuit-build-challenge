# Intuit SWE 1 - Build Challenge

This repo contains my solutions for the Intuit SWE 1 Build Challenge.
Each assignment lives in its own directory with source code, tests, and a README.

## Assignment 1: Producer Consumer
**Path:** `Assignment1/`  
**Language:** Python 3.10+

Implements a classic producer-consumer pattern using a bounded blocking queue and threads in Python. The focus is on:

- Correct thread synchronization
- A custom bounded blocking queue  
- Explicit use of threading.Lock and threading.Condition (wait() / notify())

### Structure
```
Assignment1/
├── blocking_queue.py         # BoundedBlockingQueue implementation
├── producer_consumer.py      # Producer-consumer pipeline and main file
├── test_blocking_queue.py    # Unit tests for the queue
├── test_producer_consumer.py # Unit tests for the pipeline
└── README.md                 # Detailed design and usage
```

### How to run Assignment 1
From the repo root:
```bash
cd Assignment1
python producer_consumer.py
```

Run all tests:
```bash
cd Assignment1
python -m unittest -v
```

For more details on the design, blocking behavior, and test coverage, see `Assignment1/README.md`.


## Assignment 2: Sales Data Analysis
**Path:** `Assignment2/`  
**Language:** Python 3.10+

Advanced sales data analyzer using functional programming paradigms. Demonstrates stream operations, lambda expressions, and data aggregation with a typed data model. The focus is on:

- Typed data model with immutable dataclasses
- CSV parsing with error handling
- Functional programming analysis (lambdas, stream operations, method chaining)
- Comprehensive data aggregation and business metrics

### Structure
```
Assignment2/
├── sales_analyzer.py         # Main analysis engine with functional methods
├── sales_model.py           # Typed data model for sales records
├── sales_reader.py          # CSV reader with type conversion
├── sales_data.csv           # Sample sales dataset (20 products)
├── test_sales_analyzer.py   # Comprehensive unit tests
├── test_components.py       # Component-level tests
└── README.md               # Detailed design and usage
```

### How to run Assignment 2
From the repo root:
```bash
cd Assignment2
python sales_analyzer.py
```

Run all tests:
```bash
cd Assignment2
python3 -m coverage run --source=. -m unittest tests.test_sales_analyzer tests.test_components
python3 -m coverage report --show-missing
```

For more details on the design, functional programming patterns, and test coverage, see `Assignment2/README.md`.

### Sample Output
For full output and details, see `Assignment2/README.md`.

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

3. REGIONAL ANALYSIS:
   North:
     Total Sales: $4,099.89
     Avg Order Value: $819.98
     Top Category: Electronics
   West:
     Total Sales: $4,599.86
     Avg Order Value: $919.97
     Top Category: Electronics

4. MONTHLY SALES TRENDS:
   2024-01: $11,279.68 revenue, 32 units sold
   2024-02: $1,149.85 revenue, 15 units sold

--------------------------------------------------
Achievement: 94% Overall Code Coverage
20/20 tests passed
--------------------------------------------------
```

## Technical Highlights

### Assignment 1: Concurrency & Synchronization
- **Thread-safe bounded queue** with proper blocking behavior
- **Producer-consumer pattern** with configurable parallelism
- **Comprehensive testing** of race conditions and edge cases

### Assignment 2: Functional Programming & Data Analysis
- **Typed data architecture** with immutable dataclasses
- **Stream operations** using pandas pipe() method chaining
- **Lambda expressions** for dynamic categorization and filtering
- **Higher-order functions** for data transformation and aggregation

## Requirements
- Python 3.10+
- pandas>=2.2.0 (Assignment 2)
- numpy>=1.26.0 (Assignment 2)

## Running All Tests
```bash
# Assignment 1
cd Assignment1 && python -m unittest -v

# Assignment 2  
cd Assignment2 && python -m unittest -v
```
