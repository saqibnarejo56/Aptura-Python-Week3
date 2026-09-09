# Aptura Python Internship — Week 3

Practical Python assignments completed as part of the Aptura Tech Solutions Python Programming Internship — Week 3.

This repository contains two practical Python projects focused on implementation quality, validation, persistence, testing, usability, documentation, and measurable results.

---

# Task 1 — Object-Oriented Inventory System

A command-line inventory management application built with Python using object-oriented programming principles.

The system uses separate classes for categories, products, inventory operations, and stock transactions.

## Core Features

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

## Additional Features

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

## Run Task 1

From the repository root:

```powershell
cd Task1_Inventory_System
python main.py
```

The application provides 13 menu-driven operations:

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

## Task 1 Testing

Run:

```powershell
python .\tests\test_inventory.py -v
```

Verified result:

```text
Ran 25 tests in 0.143s

OK
```

The test suite covers inventory operations, validation, persistence, stock transactions, filters, thresholds, timestamps, and CSV export.

## Task 1 Documentation

```text
Task1_Inventory_System/documentation/Task1_Documentation.pdf
```

Evidence screenshots are available in:

```text
Task1_Inventory_System/evidence/
```

---

# Task 2 — Automated Data Pipeline

A Python-based automated data pipeline that processes raw CSV and JSON records, validates and cleans data, transforms selected fields, generates summary statistics, and exports structured results.

The sample dataset represents sales records and includes both valid and intentionally invalid data so the validation and error-handling workflow can be demonstrated.

## Pipeline Workflow

```text
Raw CSV / JSON Data
        ↓
Read Records
        ↓
Clean Fields
        ↓
Validate Records
        ↓
Transform Valid Data
        ↓
Separate Valid / Invalid Records
        ↓
Generate Summary Statistics
        ↓
Export Clean Dataset + Error Log + Summary
```

## Input Fields

The pipeline processes:

```text
record_id
customer_name
email
city
order_date
quantity
unit_price
```

## Data Cleaning

The pipeline performs cleaning such as:

- Removing unnecessary whitespace
- Converting customer names to title case
- Converting email addresses to lowercase
- Standardizing city names
- Converting supported date formats to `YYYY-MM-DD`
- Converting quantity values to integers
- Converting price values to numeric values

## Validation

Records are checked for:

- Required fields
- Duplicate record IDs
- Valid email format
- Valid order dates
- Positive whole-number quantity
- Positive unit price

Invalid records are separated from valid records and written to the error log with the reason for rejection.

## Transformations

Valid records are transformed by:

- Standardizing text fields
- Standardizing date format
- Converting numeric values
- Calculating:

```text
total_amount = quantity × unit_price
```

## Summary Statistics

The pipeline generates:

- Total records
- Valid records
- Invalid records
- Valid-record percentage
- Total sales amount
- Average order value
- Minimum order value
- Maximum order value
- Records grouped by city

## Verified Dataset Result

For the included sample dataset:

```text
Total Records        : 12
Valid Records        : 7
Invalid Records      : 5
Valid Rate           : 58.33%
Total Sales Amount   : 38751.50
Average Order Value  : 5535.93
Minimum Order Value  : 4500.00
Maximum Order Value  : 8000.00
```

Records by city:

```text
Hyderabad       : 1
Islamabad       : 1
Karachi         : 3
Lahore          : 2
```

## Run Task 2 — CSV Input

From the repository root:

```powershell
cd Task2_Automated_Data_Pipeline
python main.py
```

The default input is:

```text
data/raw_data.csv
```

## Run Task 2 — JSON Input

```powershell
python main.py .\data\raw_data.json
```

Both CSV and JSON inputs process the same logical dataset and produce the same verified summary.

## Generated Outputs

The pipeline generates:

```text
Task2_Automated_Data_Pipeline/output/
├── cleaned_data.csv
├── error_log.csv
└── summary.json
```

### Clean Dataset

`cleaned_data.csv` contains only valid and transformed records.

### Error Log

`error_log.csv` contains rejected records with validation reasons.

The included invalid cases demonstrate:

```text
Invalid email
Zero quantity
Negative unit price
Duplicate record ID
Missing customer name
```

### Summary

`summary.json` contains the generated measurable statistics.

## Task 2 Testing

Run:

```powershell
python .\tests\test_pipeline.py -v
```

Verified result:

```text
Ran 24 tests in 0.072s

OK
```

The automated tests cover:

- CSV reading
- JSON reading
- Missing input handling
- Unsupported file formats
- JSON structure validation
- Name cleaning
- Email cleaning
- City cleaning
- Date transformation
- Numeric cleaning
- Invalid email rejection
- Zero quantity rejection
- Negative price rejection
- Required-field validation
- Duplicate record ID detection
- Valid-record processing
- Total amount calculation
- Error logging
- Summary statistics
- Clean CSV export
- Error-log export
- Summary JSON export
- Complete CSV pipeline
- Complete JSON pipeline

## Task 2 Documentation

```text
Task2_Automated_Data_Pipeline/documentation/Task2_Documentation.pdf
```

Evidence screenshots are available in:

```text
Task2_Automated_Data_Pipeline/evidence/
```

---

# Project Structure

```text
Aptura-Python-Week3/
│
├── Task1_Inventory_System/
│   ├── data/
│   │   └── inventory.json
│   ├── documentation/
│   │   └── Task1_Documentation.pdf
│   ├── evidence/
│   ├── exports/
│   │   └── inventory_export.csv
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_inventory.py
│   ├── inventory.py
│   ├── main.py
│   └── models.py
│
├── Task2_Automated_Data_Pipeline/
│   ├── data/
│   │   ├── raw_data.csv
│   │   └── raw_data.json
│   ├── documentation/
│   │   └── Task2_Documentation.pdf
│   ├── evidence/
│   │   ├── 01_project_structure.png
│   │   ├── 02_csv_pipeline_summary.png
│   │   ├── 03_json_pipeline_summary.png
│   │   ├── 04_cleaned_dataset.png
│   │   ├── 05_error_log.png
│   │   └── 06_automated_tests_24_passed.png
│   ├── output/
│   │   ├── cleaned_data.csv
│   │   ├── error_log.csv
│   │   └── summary.json
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_pipeline.py
│   ├── main.py
│   └── pipeline.py
│
├── .gitignore
└── README.md
```

---

# Requirements

- Python 3.x

No third-party packages are required.

The projects use Python standard-library modules including:

```text
csv
json
re
pathlib
datetime
collections
uuid
tempfile
unittest
```

---

# Week 3 Status

**Task 1 — Object-Oriented Inventory System:** Completed

**Task 2 — Automated Data Pipeline:** Completed

---

# Key Learning Areas

Week 3 provided practical experience with:

- Object-oriented programming
- File-based persistence
- Data validation
- Data cleaning
- Data transformation
- Error handling
- CSV and JSON processing
- Summary reporting
- Automated testing
- Evidence-based verification
- Project documentation

---

# Possible Future Improvements

## Inventory System

- SQLite database storage
- Graphical or web interface
- Authentication and role-based access control
- Inventory analytics dashboard
- Backup and restore support

## Automated Data Pipeline

- Support for larger datasets
- Configurable validation rules
- Additional input formats
- Database integration
- Logging with Python's `logging` module
- Command-line configuration using `argparse`
