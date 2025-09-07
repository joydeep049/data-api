# book_api.py - fetches books from API and dumps them into sqlite

import sqlite3
import requests
import json
import logging
from typing import List, Dict

# logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BookAPI:
    # this class does the heavy lifting for book stuff
    
    def __init__(self, db_path="books.db", api_url=None):
        self.db_path = db_path
        # using jsonplaceholder since we don't have a real book API
        self.api_url = api_url or "https://jsonplaceholder.typicode.com/posts"
        self.init_database()
    
    def init_database(self):
        # create the books table - basic schema
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # using title as primary key so we can easily handle duplicates
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    title TEXT PRIMARY KEY,
                    author TEXT,
                    year INTEGER,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            raise
    
    def fetch_books_from_api(self):
        # get books from the API - this is the main function
        try:
            logger.info(f"Fetching data from {self.api_url}")
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            
            raw_data = response.json()
            
            books = []
            #only take first 10 to keep it manageable
            for item in raw_data[:10]:
                book = {
                    'title': item.get('title', 'Unknown Title'),
                    'author': f"Author {item.get('userId', 'Unknown')}",  # making up authors
                    'year': 2020 + (item.get('id', 1) % 4),  # random years
                    'description': item.get('body', 'No description available')
                }
                books.append(book)
            
            logger.info(f"Successfully fetched {len(books)} books")
            return books
            
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return []
    
    def store_books(self, books):
        # save books to database
        if not books:
            logger.warning("No books to store")
            return 0
        
        stored_count = 0
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for book in books:
                try:
                    # INSERT OR REPLACE is perfect for handling duplicates
                    cursor.execute("""
                        INSERT OR REPLACE INTO books (title, author, year, description)
                        VALUES (?, ?, ?, ?)
                    """, (
                        book.get('title', ''),
                        book.get('author', ''),
                        book.get('year', None),
                        book.get('description', '')
                    ))
                    stored_count += 1
                except sqlite3.Error as e:
                    logger.error(f"Failed to store book '{book.get('title', 'Unknown')}': {e}")
            
            conn.commit()
            conn.close()
            logger.info(f"Successfully stored {stored_count} books")
            
        except sqlite3.Error as e:
            logger.error(f"Database error during storage: {e}")
            raise
        
        return stored_count
    
    def get_all_books(self):
        # get all books from the database
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  #this makes it easier to work with
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM books ORDER BY title")
            rows = cursor.fetchall()
            
            books = []
            for row in rows:
                books.append(dict(row))
            
            conn.close()
            logger.info(f"Retrieved {len(books)} books from database")
            return books
            
        except sqlite3.Error as e:
            logger.error(f"Database error during retrieval: {e}")
            return []
    
    def display_books(self, books=None):
        # print books to console in a nice format
        if books is None:
            books = self.get_all_books()
        
        if not books:
            print("No books found.")
            return
        
        print(f"\n{'='*60}")
        print(f"BOOKS IN DATABASE ({len(books)} total)")
        print(f"{'='*60}")
        
        for i, book in enumerate(books, 1):
            print(f"\n{i}. {book.get('title', 'Unknown Title')}")
            print(f"   Author: {book.get('author', 'Unknown')}")
            print(f"   Year: {book.get('year', 'Unknown')}")
            #truncate description so it doesn't take up too much space
            desc = book.get('description', 'No description')
            if len(desc) > 100:
                desc = desc[:100] + "..."
            print(f"   Description: {desc}")
            print(f"   Added: {book.get('created_at', 'Unknown')}")
        
        print(f"\n{'='*60}")


def main():
    print("Starting book API data retrieval...")
    
    book_api = BookAPI()
 
    books = book_api.fetch_books_from_api()
    
    if books:
        # save them to database
        stored_count = book_api.store_books(books)
        print(f"Stored {stored_count} books in database")

        book_api.display_books()
    else:
        print("No books fetched from API")
    
    print("\nDone!")


if __name__ == "__main__":
    main()