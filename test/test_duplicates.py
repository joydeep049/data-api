# test_duplicates.py - quick test to see if duplicate handling works

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from book_api import BookAPI

def test_duplicates():
    """
    Test the book_api.py file to see if duplicate handling works.
    """
    print("Testing duplicate handling...")

    book_api = BookAPI("test_books.db")
    
    # create test books
    test_books = [
        {
            'title': 'The Great Book',
            'author': 'John Doe',
            'year': 2020,
            'description': 'Original version'
        },
        {
            'title': 'The Great Book',  # same title!
            'author': 'Jane Smith',     # different author
            'year': 2021,               # different year
            'description': 'Updated version'  # different description
        },
        {
            'title': 'Another Book',
            'author': 'Bob Wilson',
            'year': 2019,
            'description': 'This one is unique'
        }
    ]
    
    # store
    stored_count = book_api.store_books(test_books)
    print(f"Stored {stored_count} books")
    
    # show
    print("\nBooks in database after storing duplicates:")
    book_api.display_books()
    
    # clean up test database
    import os
    if os.path.exists("test_books.db"):
        os.remove("test_books.db")
        print("\nCleaned up test database")

if __name__ == "__main__":
    test_duplicates()