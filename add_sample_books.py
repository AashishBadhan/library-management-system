"""
Add 29 sample books to the library database
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management.settings')
django.setup()

from books.models import Book, Category
from django.utils import timezone
from datetime import datetime

# Create categories first
categories_data = [
    {'name': 'Fiction', 'description': 'Fictional novels and stories'},
    {'name': 'Science Fiction', 'description': 'Sci-fi and futuristic stories'},
    {'name': 'Mystery', 'description': 'Mystery and thriller books'},
    {'name': 'Romance', 'description': 'Romantic novels'},
    {'name': 'Fantasy', 'description': 'Fantasy and magical worlds'},
    {'name': 'Non-Fiction', 'description': 'Real-life stories and facts'},
    {'name': 'Biography', 'description': 'Life stories of famous people'},
    {'name': 'History', 'description': 'Historical events and periods'},
    {'name': 'Self-Help', 'description': 'Personal development books'},
]

print("📚 Creating Categories...")
categories = {}
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={'description': cat_data['description']}
    )
    categories[cat_data['name']] = category
    if created:
        print(f"   ✅ Created: {category.name}")
    else:
        print(f"   ℹ️  Exists: {category.name}")

# 29 Popular Books Data
books_data = [
    # Fiction
    {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'isbn': '978-0-06-112008-4', 'category': 'Fiction', 'year': 1960, 'quantity': 5, 'description': 'A gripping tale of racial injustice and childhood innocence in the American South.'},
    {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'isbn': '978-0-7432-7356-5', 'category': 'Fiction', 'year': 1925, 'quantity': 4, 'description': 'The story of the mysteriously wealthy Jay Gatsby and his love for Daisy Buchanan.'},
    {'title': '1984', 'author': 'George Orwell', 'isbn': '978-0-452-28423-4', 'category': 'Fiction', 'year': 1949, 'quantity': 6, 'description': 'A dystopian social science fiction novel and cautionary tale.'},
    {'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'isbn': '978-0-14-143951-8', 'category': 'Romance', 'year': 1813, 'quantity': 3, 'description': 'A romantic novel of manners set in Georgian England.'},
    
    # Fantasy
    {'title': 'Harry Potter and the Sorcerer\'s Stone', 'author': 'J.K. Rowling', 'isbn': '978-0-439-70818-8', 'category': 'Fantasy', 'year': 1997, 'quantity': 8, 'description': 'The first novel in the Harry Potter series about a young wizard.'},
    {'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'isbn': '978-0-547-92822-7', 'category': 'Fantasy', 'year': 1937, 'quantity': 5, 'description': 'A fantasy novel about the adventures of hobbit Bilbo Baggins.'},
    {'title': 'The Lord of the Rings', 'author': 'J.R.R. Tolkien', 'isbn': '978-0-544-00341-5', 'category': 'Fantasy', 'year': 1954, 'quantity': 4, 'description': 'An epic high-fantasy novel about the quest to destroy the One Ring.'},
    {'title': 'A Game of Thrones', 'author': 'George R.R. Martin', 'isbn': '978-0-553-10354-0', 'category': 'Fantasy', 'year': 1996, 'quantity': 6, 'description': 'First book in A Song of Ice and Fire series.'},
    
    # Science Fiction
    {'title': 'Dune', 'author': 'Frank Herbert', 'isbn': '978-0-441-17271-9', 'category': 'Science Fiction', 'year': 1965, 'quantity': 5, 'description': 'A science fiction novel about politics, religion, and ecology on desert planet.'},
    {'title': 'The Martian', 'author': 'Andy Weir', 'isbn': '978-0-553-41802-6', 'category': 'Science Fiction', 'year': 2011, 'quantity': 7, 'description': 'Story of an astronaut stranded on Mars and his fight for survival.'},
    {'title': 'Ender\'s Game', 'author': 'Orson Scott Card', 'isbn': '978-0-312-93208-8', 'category': 'Science Fiction', 'year': 1985, 'quantity': 4, 'description': 'A military science fiction novel about a young genius trained for war.'},
    {'title': 'Foundation', 'author': 'Isaac Asimov', 'isbn': '978-0-553-29335-1', 'category': 'Science Fiction', 'year': 1951, 'quantity': 3, 'description': 'A science fiction novel about the fall and rise of civilizations.'},
    
    # Mystery/Thriller
    {'title': 'The Da Vinci Code', 'author': 'Dan Brown', 'isbn': '978-0-307-47927-1', 'category': 'Mystery', 'year': 2003, 'quantity': 5, 'description': 'A mystery thriller novel involving art, symbols, and secret societies.'},
    {'title': 'Gone Girl', 'author': 'Gillian Flynn', 'isbn': '978-0-307-58836-4', 'category': 'Mystery', 'year': 2012, 'quantity': 6, 'description': 'A psychological thriller about a wife who disappears on her anniversary.'},
    {'title': 'The Girl with the Dragon Tattoo', 'author': 'Stieg Larsson', 'isbn': '978-0-307-45454-1', 'category': 'Mystery', 'year': 2005, 'quantity': 4, 'description': 'A crime mystery novel set in Sweden.'},
    {'title': 'And Then There Were None', 'author': 'Agatha Christie', 'isbn': '978-0-06-207348-6', 'category': 'Mystery', 'year': 1939, 'quantity': 5, 'description': 'A mystery novel about ten strangers invited to an island.'},
    
    # Non-Fiction/Self-Help
    {'title': 'Sapiens', 'author': 'Yuval Noah Harari', 'isbn': '978-0-062-31609-7', 'category': 'Non-Fiction', 'year': 2011, 'quantity': 7, 'description': 'A brief history of humankind from Stone Age to modern age.'},
    {'title': 'Atomic Habits', 'author': 'James Clear', 'isbn': '978-0-735-21129-2', 'category': 'Self-Help', 'year': 2018, 'quantity': 8, 'description': 'An easy and proven way to build good habits and break bad ones.'},
    {'title': 'The 7 Habits of Highly Effective People', 'author': 'Stephen Covey', 'isbn': '978-1-982-13709-9', 'category': 'Self-Help', 'year': 1989, 'quantity': 6, 'description': 'A self-help book about achieving personal and professional effectiveness.'},
    {'title': 'Thinking, Fast and Slow', 'author': 'Daniel Kahneman', 'isbn': '978-0-374-53355-7', 'category': 'Non-Fiction', 'year': 2011, 'quantity': 5, 'description': 'A book about the two systems that drive the way we think.'},
    
    # Biography/History
    {'title': 'Steve Jobs', 'author': 'Walter Isaacson', 'isbn': '978-1-451-64853-9', 'category': 'Biography', 'year': 2011, 'quantity': 4, 'description': 'The authorized biography of Apple co-founder Steve Jobs.'},
    {'title': 'The Diary of a Young Girl', 'author': 'Anne Frank', 'isbn': '978-0-375-41398-8', 'category': 'Biography', 'year': 1947, 'quantity': 5, 'description': 'The diary of Anne Frank during the Nazi occupation.'},
    {'title': 'A Brief History of Time', 'author': 'Stephen Hawking', 'isbn': '978-0-553-10953-5', 'category': 'Non-Fiction', 'year': 1988, 'quantity': 4, 'description': 'A landmark volume in science writing about cosmology.'},
    
    # More Popular Books
    {'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger', 'isbn': '978-0-316-76948-0', 'category': 'Fiction', 'year': 1951, 'quantity': 3, 'description': 'A story about teenage rebellion and alienation.'},
    {'title': 'The Alchemist', 'author': 'Paulo Coelho', 'isbn': '978-0-061-12241-5', 'category': 'Fiction', 'year': 1988, 'quantity': 6, 'description': 'A story about following your dreams and finding treasure.'},
    {'title': 'The Hunger Games', 'author': 'Suzanne Collins', 'isbn': '978-0-439-02348-1', 'category': 'Science Fiction', 'year': 2008, 'quantity': 7, 'description': 'A dystopian novel about survival and rebellion.'},
    {'title': 'The Chronicles of Narnia', 'author': 'C.S. Lewis', 'isbn': '978-0-066-23850-4', 'category': 'Fantasy', 'year': 1950, 'quantity': 5, 'description': 'A series of fantasy novels set in the magical land of Narnia.'},
    {'title': 'Brave New World', 'author': 'Aldous Huxley', 'isbn': '978-0-060-85052-4', 'category': 'Science Fiction', 'year': 1932, 'quantity': 4, 'description': 'A dystopian novel set in a futuristic World State.'},
    {'title': 'The Book Thief', 'author': 'Markus Zusak', 'isbn': '978-0-375-84220-7', 'category': 'Fiction', 'year': 2005, 'quantity': 5, 'description': 'A story narrated by Death during Nazi Germany.'},
]

print("\n📖 Adding Books...")
added_count = 0
skipped_count = 0

for book_data in books_data:
    # Check if book already exists
    if Book.objects.filter(isbn=book_data['isbn']).exists():
        print(f"   ⏭️  Skipped: {book_data['title']} (already exists)")
        skipped_count += 1
        continue
    
    # Create book
    book = Book.objects.create(
        title=book_data['title'],
        author=book_data['author'],
        isbn=book_data['isbn'],
        category=categories[book_data['category']],
        publication_date=datetime(book_data['year'], 1, 1),
        quantity=book_data['quantity'],
        available=book_data['quantity'],
        price=299.00,  # Default price
        description=book_data['description']
    )
    print(f"   ✅ Added: {book.title} by {book.author}")
    added_count += 1

print("\n" + "="*60)
print("📊 SUMMARY")
print("="*60)
print(f"✅ Books Added: {added_count}")
print(f"⏭️  Books Skipped: {skipped_count}")
print(f"📚 Total Books in Database: {Book.objects.count()}")
print(f"📂 Total Categories: {Category.objects.count()}")
print("\n🎉 Done! Books successfully added to library!")
print("="*60)
