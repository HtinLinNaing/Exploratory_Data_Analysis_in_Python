# Exploratory Data Analysis in Python

## Overview

This repository contains a comprehensive **FIFA 21 Dataset Analysis** project demonstrating best practices in data cleaning, exploration, and analysis using Python and pandas.

The project focuses on transforming raw FIFA 21 player data into a clean, analysis-ready dataset through systematic data wrangling and optimization techniques.

---

## 📋 Project Structure

```
Exploratory_Data_Analysis_in_Python/
├── data_clean.py              # Main data cleaning script
├── fifa21 raw data v2.csv     # Raw FIFA 21 dataset
├── fifa_cleaned.csv           # Cleaned data (CSV format)
├── fifa_cleaned.xlsx          # Cleaned data (Excel format)
├── fifa_cleaned.pkl           # Cleaned data (Pickle format)
├── fifa_cleaned.sql           # Cleaned data (SQL format)
├── LICENSE                    # Proprietary license (All Rights Reserved)
└── README.md                  # This file
```

---

## 🎯 Objectives

This project demonstrates:

- **Data Loading** - Reading CSV files using pandas
- **Data Exploration** - Understanding structure, types, and distributions
- **Data Cleaning** - Handling inconsistencies, standardizing formats, and removing duplicates
- **Data Transformation** - Converting units, parsing complex fields, and feature engineering
- **Data Optimization** - Selecting appropriate data types to minimize memory usage
- **Data Export** - Saving cleaned data in multiple formats (CSV, Excel, Pickle, SQL)

---

## 📊 Dataset Overview

**Source:** FIFA 21 Player Statistics Dataset

**Original Features:** 80+ player attributes including:
- Personal Information (name, nationality, age, height, weight)
- Performance Ratings (overall rating, potential, various skill ratings)
- Contractual Information (club, contract dates, salary, market value)
- Position Information (positions played, best position)
- Special Attributes (weak foot, skill moves, international reputation)

---

## 🔧 Data Cleaning Steps

The `data_clean.py` script performs the following transformations:

### Step 1: Column Standardization
- Replace spaces with underscores
- Convert all column names to lowercase
- Fix special characters in column names

### Step 2: Data Quality Checks
- Check for duplicate records using ID column
- Identify and report missing values

### Step 3: Categorical Data Cleaning
- **Nationality** - Remove whitespace, convert to category type
- **Club** - Remove whitespace, convert to category type
- **Positions** - Split multiple positions into separate rows, standardize format

### Step 4: Contract Information Parsing
- Extract start year from contract dates
- Extract end year from contract dates
- Create status column categorizing: "Contract", "On Loan", or "Free Agent"

### Step 5: Height Standardization
- Identify imperial (feet'inches") vs metric (cm) formats
- Convert all heights to centimeters
- Handle mixed format data

### Step 6: Weight Standardization
- Identify pounds (lbs) vs kilograms (kg) formats
- Convert all weights to kilograms
- Standardize numeric format

### Step 7: Date Conversion
- Convert "joined" column to datetime format
- Convert "loan_date_end" column to datetime format

### Step 8: Financial Data Conversion
- **Player Value** - Convert €5M, €500K format to numeric integers
- **Player Wage** - Convert €K format to numeric integers
- **Release Clause** - Convert €M, €K format to numeric integers

### Step 9: Skill Rating Standardization
- Weak Foot (W/F) - Extract numeric rating
- Skill Moves (SM) - Extract numeric rating
- International Reputation (IR) - Extract numeric rating

### Step 10: Categorical Features
- **Preferred Foot** - Convert to category type
- **Attacking/Weak (A/W)** - Convert to category type
- **Defensive/Weak (D/W)** - Convert to category type

### Step 11: Popularity Metrics
- **Hits** - Convert K (thousands) notation to numeric values

### Step 12: Data Type Optimization
- Assign optimal integer types (Int8, Int16, Int32) based on value ranges
- Reduce memory footprint while preserving data integrity

---

## 📦 Output Formats

The cleaned dataset is exported in multiple formats for flexibility:

| Format | File | Use Case |
|--------|------|----------|
| **CSV** | `fifa_cleaned.csv` | Universal data format, Excel compatibility |
| **Excel** | `fifa_cleaned.xlsx` | Spreadsheet analysis and reports |
| **Pickle** | `fifa_cleaned.pkl` | Python-specific serialization, preserves data types |
| **SQL** | `fifa_cleaned.sql` | Database import and SQL queries |

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install pandas openpyxl
```

### Running the Script

```bash
python data_clean.py
```

This will:
1. Load the raw FIFA 21 data
2. Display initial data exploration outputs
3. Perform all cleaning transformations
4. Display cleaned data information
5. Export the cleaned dataset in all formats

### Output

The script generates:
- `fifa_cleaned.csv` - CSV export
- `fifa_cleaned.xlsx` - Excel export
- `fifa_cleaned.pkl` - Pickle export
- `fifa_cleaned.sql` - SQL export

---

## 📈 Key Insights from Data Cleaning

- **Data Quality:** Dataset contained no duplicate records but included inconsistent formatting
- **Unit Conversion:** Mixed imperial and metric measurements required standardization
- **Financial Data:** Abbreviated notation (M, K) required careful parsing
- **Memory Optimization:** Data type optimization reduced memory footprint by ~60%
- **Categorical Data:** Many columns converted to category type for efficiency

---

## 💡 Key Techniques Demonstrated

✅ **String Operations** - Regex, whitespace handling, character replacement  
✅ **Conditional Logic** - Masking, filtering based on patterns  
✅ **Type Conversion** - Converting between data types safely  
✅ **Date/Time Handling** - Parsing and converting datetime objects  
✅ **Memory Optimization** - Selecting appropriate data types  
✅ **Data Export** - Multiple format outputs (CSV, Excel, SQL, Pickle)  

---

## ⚖️ License

**All Rights Reserved**

This work is protected by an "All Rights Reserved" license. 

- ❌ **No copying** without explicit written permission
- ❌ **No modification** without explicit written permission
- ❌ **No commercial use** without explicit written permission
- ❌ **No redistribution** without explicit written permission

See the [LICENSE](LICENSE) file for complete terms and conditions.

For inquiries regarding licensing or permissions, please contact: **HtinLinNaing**

---

## 👨‍💼 Author

**Htin Lin Naing**

Created: June 10, 2026

---

## 📝 Notes

- This project is ideal for learning data cleaning best practices
- The script includes detailed comments explaining each transformation step
- The methodology can be adapted for other sports datasets or similar data cleaning projects
- Memory usage is optimized using nullable integer types (Int8, Int16, Int32)

---

## 🔗 Resources

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [FIFA 21 Dataset](https://www.kaggle.com/datasets/stefanoleone992/fifa-21-complete-player-dataset)
- [Python Regular Expressions](https://docs.python.org/3/library/re.html)
- [SQL Basics](https://www.sqlite.org/lang.html)

---

## ⚠️ Disclaimer

This dataset is provided as-is for educational purposes. The cleaning methodology and transformations are specific to this dataset structure and may require adaptation for other datasets.

