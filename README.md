# Aptura Python Internship — Week 3

Practical Python assignments completed as part of the Aptura Tech Solutions Python Programming Internship — Week 3.

This repository focuses on practical implementation, code quality, validation, persistence, testing, usability, documentation, and measurable results.

---

## Task 1 — Object-Oriented Inventory System

A command-line inventory management application built with Python using object-oriented programming principles.

The system uses separate classes for categories, products, inventory operations, and stock transactions.

### Core Features

- Add and manage product categories
- Add products
- Update products
- Remove products
- Search products
- View all inventory records
- Inventory summary reporting
- Input validation and error handling
- Duplicate ID prevention
- JSON-based persistent storage

### Additional Features

- Stock In operations
- Stock Out operations
- Stock transaction history
- Transaction IDs
- Audit timestamps
- Product creation and update timestamps
- Configurable low-stock threshold
- Category filtering
- Low-stock filtering
- Out-of-stock filtering
- CSV inventory export
- Persistent application settings

---

## Project Structure

```text
Aptura-Python-Week3/
│
├── Task1_Inventory_System/
│   ├── data/
│   │   └── inventory.json
│   │
│   ├── documentation/
│   │   └── Task1_Documentation.pdf
│   │
│   ├── evidence/
│   │   ├── 01_project_structure.png
│   │   ├── 02_enhanced_menu.png
│   │   ├── 03_stock_transactions.png
│   │   ├── 04_category_filter.png
│   │   └── 05_automated_tests_25_passed.png
│   │
│   ├── exports/
│   │   └── inventory_export.csv
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_inventory.py
│   │
│   ├── inventory.py
│   ├── main.py
│   └── models.py
│
├── .gitignore
└── README.md
```

---

## Requirements

- Python 3.x

No third-party packages are required.

The project uses Python standard-library modules including:

- `json`
- `csv`
- `pathlib`
- `datetime`
- `uuid`
- `tempfile`
- `unittest`

---

## Run Task 1

Open a terminal in the repository root:

```powershell
cd Task1_Inventory_System
python main.py
```

The application provides the following menu:

```text
1.  Add Category
2.  Add Product
3.  Update Product
4.  Remove Product
5.  Search Products
6.  View All Products
7.  Inventory Summary
8.  Stock In
9.  Stock Out
10. Transaction History
11. Set Low-Stock Threshold
12. Filter Products
13. Export Inventory to CSV
0.  Exit
```

---

## Automated Testing

The project uses Python's built-in `unittest` framework.

Run the test suite from inside `Task1_Inventory_System`:

```powershell
python .\tests\test_inventory.py -v
```

Current verified result:

```text
Ran 25 tests in 0.143s

OK
```

### Test Coverage

The automated test suite covers:

- Category creation
- Product creation
- Duplicate category rejection
- Duplicate product rejection
- Invalid category validation
- Negative price validation
- Negative quantity validation
- Product update
- Product removal
- Product search
- Inventory summary
- JSON persistence
- Stock In
- Stock Out
- Insufficient stock validation
- Invalid stock quantity validation
- Transaction history
- Transaction persistence
- Low-stock threshold configuration
- Invalid threshold validation
- Category filtering
- Low-stock filtering
- Out-of-stock filtering
- CSV export
- Product timestamps

---

## Persistence

Application data is stored in:

```text
Task1_Inventory_System/data/inventory.json
```

The system persists:

- Categories
- Products
- Stock transactions
- Audit timestamps
- Low-stock threshold settings

The saved data is automatically loaded when the application starts.

---

## CSV Export

Inventory data can be exported through the application menu.

Generated file:

```text
Task1_Inventory_System/exports/inventory_export.csv
```

The export contains product information, category information, quantities, prices, and timestamps.

---

## Documentation and Evidence

Detailed Task 1 documentation is available at:

```text
Task1_Inventory_System/documentation/Task1_Documentation.pdf
```

Practical evidence and screenshots are available inside:

```text
Task1_Inventory_System/evidence/
```

---

## Week 3 Progress

**Task 1 — Object-Oriented Inventory System:** Completed

**Task 2 — Automated Data Pipeline:** In Progress

---

## Future Improvements

Possible future enhancements include:

- SQLite database storage
- Graphical or web-based interface
- Authentication and role-based access control
- Inventory analytics dashboards
- Automated backup and restore
