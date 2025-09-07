#!/usr/bin/env python3
import os
import csv
from csv_import import CSVImporter

def create_test_csv():
    test_data = [
        {'name': 'Test User 1', 'email': 'test1@example.com'},
        {'name': 'Test User 2', 'email': 'test2@example.com'},
        {'name': 'Invalid Email', 'email': 'not-an-email'},
        {'name': '', 'email': 'empty.name@example.com'},
        {'name': 'Test User 1', 'email': 'test1@example.com'}
    ]
    
    with open('test_users.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'email'])
        writer.writeheader()
        writer.writerows(test_data)
    
    print("Created test_users.csv")

def main():
    if os.path.exists('test_users.db'):
        os.remove('test_users.db')
    
    create_test_csv()
    
    importer = CSVImporter('test_users.db')
    imported, skipped = importer.import_csv('test_users.csv')
    
    print(f"Test results: {imported} imported, {skipped} skipped")
    importer.display_users()
    
    os.remove('test_users.csv')
    os.remove('test_users.db')
    print("Cleaned up test files")

if __name__ == "__main__":
    main()