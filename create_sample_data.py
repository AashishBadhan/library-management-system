import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management.settings')
django.setup()

from django.contrib.auth import get_user_model
from books.models import Book, Category
from datetime import date

User = get_user_model()

# Create admin user
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@library.com',
        password='admin123',
        role='admin'
    )
    print("✅ Admin user created: admin / admin123")
else:
    print("ℹ️  Admin user already exists")

# Create sample categories
categories = [
    {'name': 'Fiction', 'description': 'Fictional stories and novels'},
    {'name': 'Science', 'description': 'Science and technology books'},
    {'name': 'History', 'description': 'Historical books'},
    {'name': 'Programming', 'description': 'Programming and computer science'},
]

for cat_data in categories:
    cat, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={'description': cat_data['description']}
    )
    if created:
        print(f"✅ Category created: {cat.name}")

# Create sample books
fiction = Category.objects.get(name='Fiction')
science = Category.objects.get(name='Science')
programming = Category.objects.get(name='Programming')

books = [
    {
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
        'isbn': '9780743273565',
        'category': fiction,
        'quantity': 5,
        'available': 5,
        'price': 15.99,
        'publication_date': date(1925, 4, 10),
        'description': 'A classic American novel set in the Jazz Age'
    },
    {
        'title': 'To Kill a Mockingbird',
        'author': 'Harper Lee',
        'isbn': '9780061120084',
        'category': fiction,
        'quantity': 4,
        'available': 4,
        'price': 18.99,
        'publication_date': date(1960, 7, 11),
        'description': 'A story of racial injustice and childhood innocence'
    },
    {
        'title': 'A Brief History of Time',
        'author': 'Stephen Hawking',
        'isbn': '9780553380163',
        'category': science,
        'quantity': 3,
        'available': 3,
        'price': 24.99,
        'publication_date': date(1988, 4, 1),
        'description': 'From the Big Bang to Black Holes'
    },
    {
        'title': 'Python Crash Course',
        'author': 'Eric Matthes',
        'isbn': '9781593279288',
        'category': programming,
        'quantity': 6,
        'available': 6,
        'price': 39.99,
        'publication_date': date(2019, 5, 3),
        'description': 'A Hands-On, Project-Based Introduction to Programming'
    },
    {
        'title': 'Clean Code',
        'author': 'Robert C. Martin',
        'isbn': '9780132350884',
        'category': programming,
        'quantity': 4,
        'available': 4,
        'price': 44.99,
        'publication_date': date(2008, 8, 1),
        'description': 'A Handbook of Agile Software Craftsmanship'
    },
]

for book_data in books:
    book, created = Book.objects.get_or_create(
        isbn=book_data['isbn'],
        defaults=book_data
    )
    if created:
        print(f"✅ Book created: {book.title}")

# Create a student user
if not User.objects.filter(username='student').exists():
    User.objects.create_user(
        username='student',
        email='student@library.com',
        password='student123',
        role='student',
        phone_number='1234567890'
    )
    print("✅ Student user created: student / student123")
else:
    print("ℹ️  Student user already exists")

print("\n✅ Sample data created successfully!")
print("\nLogin credentials:")
print("  Admin: admin / admin123")
print("  Student: student / student123")
print("\nBackend: http://localhost:8000")
print("Frontend: http://localhost:3000")
