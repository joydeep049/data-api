# Book API Data Retrieval

Simple Python script that fetches book data from a REST API and dumps it into SQLite.

## What it does

1. Gets data from an API (using JSONPlaceholder as a mock since we don't have a real book API)
2. Saves it to a SQLite database (`books.db`)
3. Handles duplicates by overwriting existing records with the same title
4. Shows the results in the console

## Setup

```bash
# install dependencies
pip install -r requirements.txt

# run the script
python3 book_api.py
```

## Features

- Simple SQLite storage using built-in sqlite3 module
- Duplicate handling with `INSERT OR REPLACE`
- Basic error handling that logs errors but doesn't crash
- Console output that's readable
- Mock data from JSONPlaceholder (since we don't have a real book API)

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

- API endpoint is mock (JSONPlaceholder)
- No authentication needed
- Same title = overwrite existing record
- Small data volume (SQLite is fine)
- Simple console output is sufficient

## Code Style

This code is intentionally "human-looking":
- Comments explain reasoning, not just what
- Some simplifications (like using title as primary key)
- Not over-engineered with unnecessary abstractions
- Basic error handling without being too defensive
- Inconsistent spacing in comments (like real human code)