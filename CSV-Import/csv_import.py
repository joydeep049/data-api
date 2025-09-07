#!/usr/bin/env python3
import csv
import sqlite3
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CSVImporter:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
        logger.info("Database initialized")
    
    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def import_csv(self, csv_file):
        imported = 0
        skipped = 0
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                for row in reader:
                    name = row.get('name', '').strip()
                    email = row.get('email', '').strip()
                    
                    if not name or not email:
                        skipped += 1
                        continue
                    
                    if not self.is_valid_email(email):
                        skipped += 1
                        continue
                    
                    try:
                        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
                        imported += 1
                    except sqlite3.IntegrityError:
                        skipped += 1
                
                conn.commit()
                conn.close()
                
        except FileNotFoundError:
            logger.error(f"File {csv_file} not found")
            return 0, 0
        except Exception as e:
            logger.error(f"Error importing CSV: {e}")
            return 0, 0
        
        logger.info(f"Imported: {imported}, Skipped: {skipped}")
        return imported, skipped
    
    def get_all_users(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY name")
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return users
    
    def display_users(self):
        users = self.get_all_users()
        if not users:
            print("No users found")
            return
        
        print(f"\n{'='*60}")
        print(f"USERS IN DATABASE ({len(users)} total)")
        print(f"{'='*60}")
        
        for user in users:
            print(f"{user['name']:<30} {user['email']}")
        
        print(f"{'='*60}")

def main():
    importer = CSVImporter()
    
    csv_file = "users.csv"
    imported, skipped = importer.import_csv(csv_file)
    
    print(f"Import complete: {imported} imported, {skipped} skipped")
    importer.display_users()

if __name__ == "__main__":
    main()