"""
Quick script to view SQLite database structure and data
"""
import sqlite3
import os

db_path = 'db.sqlite3'

if not os.path.exists(db_path):
    print(f"❌ Database file not found: {db_path}")
    print(f"Current directory: {os.getcwd()}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()

print("=" * 60)
print("📊 LIBRARY MANAGEMENT DATABASE")
print("=" * 60)
print(f"\n📁 Database: {db_path}")
print(f"📋 Total Tables: {len(tables)}\n")

for table in tables:
    table_name = table[0]
    
    # Skip Django internal tables for cleaner output
    if table_name.startswith('django_') or table_name.startswith('auth_') or table_name.startswith('sqlite_'):
        continue
    
    # Get table info
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    # Get row count
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    
    print(f"📌 Table: {table_name}")
    print(f"   Rows: {count}")
    print(f"   Columns: {len(columns)}")
    
    # Show column names
    col_names = [col[1] for col in columns]
    print(f"   Fields: {', '.join(col_names[:5])}", end="")
    if len(col_names) > 5:
        print(f" ... (+{len(col_names)-5} more)")
    else:
        print()
    
    # Show sample data if available
    if count > 0:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
        sample_data = cursor.fetchall()
        print(f"   Sample: {count} record(s) found")
    
    print()

# Show specific counts for important tables
print("=" * 60)
print("📈 QUICK STATS")
print("=" * 60)

important_tables = {
    'books_book': 'Books',
    'books_bookissue': 'Book Issues',
    'books_notification': 'Notifications',
    'books_review': 'Reviews',
    'books_category': 'Categories'
}

for table, label in important_tables.items():
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"   {label}: {count}")
    except sqlite3.OperationalError:
        pass

conn.close()

print("\n✅ Database opened successfully!")
print("💡 Install 'SQLite Viewer' extension to view/edit data in VS Code")
