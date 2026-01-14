# Sales Analytics System

## Overview
The **Sales Analytics System** is a Python-based data analytics application designed to process, clean, analyze, and enrich e-commerce sales data.  
It demonstrates core Python concepts including file handling, data validation, data analysis, API integration, and report generation.

This project was developed as part of **Module 3: Python Programming Assignment**.

---

## Project Features
- Reads and cleans messy, non-UTF-8 encoded sales data files
- Handles real-world data quality issues (missing fields, invalid values, formatting errors)
- Validates transactions based on business rules
- Performs comprehensive sales analytics
- Integrates with an external API (DummyJSON) to enrich product data
- Generates a detailed, formatted sales report
- Graceful error handling throughout the workflow

---

## Repository Structure

sales-analytics-system/  
├── README.md  
├── main.py  
├── requirements.txt  
├── utils/  
│ ├── file_handler.py  
│ ├── data_processor.py  
│ └── api_handler.py  
├── data/  
│ ├── sales_data.txt  
│ └── enriched_sales_data.txt  
└── output/  
└── sales_report.txt  

---

## Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher
- Internet connection (for API integration)

### 2. Install Dependencies
**On macOS or Linux:**
```bash
python3 -m pip install -r requirements.txt
```
**On Windows:**
```bash
python -m pip install -r requirements.txt
```
**How to Run the Application**

From the root directory of the project:
```bash
python3 main.py
```
This single command runs the entire pipeline automatically.

Execution Workflow
The program performs the following steps:
1. Reads the sales data file with encoding handling
2. Parses and cleans raw transaction data
3. Validates records and removes invalid transactions
4. Performs sales analysis:
    -Total revenue
    -Region-wise sales
    -Top products and customers
    -Daily sales trends
5. Fetches product data from the DummyJSON API
6. Enriches sales data with API information
7. Saves enriched sales data to a file
8. Generates a comprehensive sales analytics report


Output Files

1. Enriched Sales Data
Location: data/enriched_sales_data.txt
Contains cleaned transaction data enriched with API fields such as category, brand, and rating

2. Sales Analytics Report
Location: output/sales_report.txt
Includes:  
    -Overall summary  
    -Region-wise performance  
    -Top products and customers  
    -Daily sales trends  
    -Product performance analysis  
    -API enrichment summary  

API Used  
    
    -DummyJSON Products API
    -Base URL: https://dummyjson.com/products
The API is used to enrich sales transactions with additional product metadata.
