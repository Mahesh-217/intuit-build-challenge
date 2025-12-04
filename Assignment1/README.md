# Assignment 1: Producer Consumer
### Producer–Consumer Pattern with Thread Synchronization (Python)

This module implements a producer-consumer pattern using a bounded
blocking queue and threads in Python, demonstrating thread synchronization and use of wait/notify primitives.

---

## Requirements

- Python 3.11+

No third party libraries are required.
Only the Python standard library is used.

---

## Project Structure

```
Assignment1/
│
├── blocking_queue.py         # Custom bounded blocking queue
├── producer_consumer.py      # Producer, Consumer, run_pipeline()
├── tests/
│   ├── test_blocking_queue.py
│   └── test_producer_consumer.py
└── __init__.py

README.md                     # This file
```

---

# Design Overview

## 1. **BlockingQueue**  
A manually implemented bounded FIFO queue supporting:

- `put(item, timeout=None)`  
- `get(timeout=None)`  
- Proper blocking behavior
- Timeout support  
- A single shared lock for correct monitor-style synchronization

Key correctness guarantees:

- Producers block when the queue is full  
- Consumers block when the queue is empty  
- Both operations wake exactly one corresponding waiter  
- Spurious wakeups are handled using **while-loops**, not **if**

This matches real production monitor patterns.

---

## 2. **Producer Thread**

The `Producer`:

- Iterates over a source iterable  
- Pushes each item into the queue  
- On *any* exception, still sends a **sentinel**  
- Designed so replacing the source with a generator or I/O stream is trivial

---

## 3. **Consumer Thread**

The `Consumer`:

- Continuously pulls from the queue  
- Appends items to a destination container  
- Stops cleanly when it reads the sentinel  
- Never busy-loops  
- Works with arbitrary item types (`Generic[T]`)

---

## 4. **Sentinel-Based Shutdown**

We use a unique `SENTINEL = object()` rather than a shared value like `None`:

- Guaranteed non-collision  
- Identity-checked (`is`) so no ambiguity  
- Clean, minimal shutdown logic  

---

## 5. **Pipeline Orchestration**

`run_pipeline(source, queue_size)` wires everything together:

```
source -> Producer -> BlockingQueue -> Consumer -> destination
```

---

# Setup & Usage

### **Environment Setup**

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install testing dependencies
pip install coverage
```

---

## Running the Pipeline Demo

Inside the repo root:

```bash
python3 Assignment1/producer_consumer.py
```

Expected sample output:

```
Source data: [1, 2, 3, 4, 5]
Result: [1, 2, 3, 4, 5]
Pipeline completed successfully!
```

---

## Running Tests

### **Run All Tests**
```bash
# Using unittest module
python3 -m unittest discover Assignment1/tests/ -v

# Individual test files
python3 Assignment1/tests/test_blocking_queue.py
python3 Assignment1/tests/test_producer_consumer.py
```

### **Test Results Summary**
- **Total Tests**: 20 tests across 2 modules
- **BlockingQueue Tests**: 9 tests (100% pass rate)
- **Producer/Consumer Tests**: 11 tests (100% pass rate)
- **All Tests Pass**: ✅

---

## Code Coverage Analysis

### **Run Coverage Analysis**
```bash
# Install coverage tool
pip install coverage

# Run tests with coverage
python -m coverage run --source=Assignment1 --omit="*/tests/*" -m unittest discover Assignment1/tests/

# Generate coverage report
source .venv/bin/activate && python -m coverage report -m
```

### **Coverage Results**
```
Name                              Stmts   Miss  Cover
-----------------------------------------------------
Assignment1/__init__.py               0      0   100%
Assignment1/blocking_queue.py        58      0   100%
Assignment1/producer_consumer.py     42      0   100%
-----------------------------------------------------
TOTAL                               100      0   100%
```

**Achievement: 100% Code Coverage on Source Files**

---

# ✔ Comprehensive Test Coverage

The test suite provides complete coverage across:

### **BlockingQueue Module (9 tests)**
### **Producer/Consumer Module (11 tests)**
### **Concurrency & Edge Cases**
---
