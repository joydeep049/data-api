# Data API Projects

Two simple Python scripts for data processing and visualization.

## Project 1: Book API Data Retrieval

Simple Python script that fetches book data from a REST API and dumps it into SQLite.

### What it does

1. Gets data from an API (using JSONPlaceholder as a mock since we don't have a real book API)
2. Saves it to a SQLite database (`books.db`)
3. Handles duplicates by overwriting existing records with the same title
4. Shows the results in the console

## Project 2: Student Scores Analysis

Fetches student test scores, calculates statistics, and creates visualizations.

### What it does

1. Gets student data from an API (using JSONPlaceholder users as mock students)
2. Generates random test scores (60-100 range)
3. Calculates average, highest, and lowest scores
4. Creates a text-based bar chart visualization
5. Shows summary statistics

## Project 3: CSV Data Import

Reads CSV files and imports user data into SQLite database with validation.

### What it does

1. Reads CSV files with name and email columns
2. Validates email format using regex
3. Skips invalid emails and empty names
4. Handles duplicate emails (skips duplicates)
5. Stores valid records in SQLite database

## Setup

```bash
# install dependencies
pip install -r requirements.txt

# run the book API script
python3 Book-API/book_api.py

# run the student scores script
python3 StudentScore-API/student_scores_simple.py

# run the CSV import script
cd CSV-Import
python3 csv_import.py

```

## Features

### Book API Project
- Simple SQLite storage using built-in sqlite3 module
- Duplicate handling with `INSERT OR REPLACE`
- Basic error handling that logs errors but doesn't crash
- Console output that's readable
- Mock data from JSONPlaceholder (since we don't have a real book API)

### Student Scores Project
- Fetches student data from API
- Calculates statistics (average, min, max)
- Creates text-based bar chart visualization
- Works without matplotlib (fallback version)
- Mock data generation for testing

### CSV Import Project
- Reads CSV files with UTF-8 encoding
- Email format validation using regex
- Duplicate email handling (skips duplicates)
- SQLite storage with proper schema
- Error handling for invalid data

## Database Schema

```sql
CREATE TABLE books (
    title TEXT PRIMARY KEY,
    author TEXT,
    year INTEGER,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Assumptions Made

### Book API Project
- API endpoint is mock (JSONPlaceholder)
- No authentication needed
- Same title = overwrite existing record
- Small data volume (SQLite is fine)
- Simple console output is sufficient

### Student Scores Project
- API endpoint is mock (JSONPlaceholder users)
- Scores are integers between 60-100 (realistic range)
- Small dataset, all processing in memory
- Text-based visualization is sufficient (matplotlib optional)
- Random score generation for demo purposes

### CSV Import Project
- CSV format has header row
- File is UTF-8 encoded
- Small dataset (<10k rows)
- Email validation is basic regex check
- Duplicate emails are skipped, not overwritten
