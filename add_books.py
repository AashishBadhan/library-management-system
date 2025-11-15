import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management.settings')
django.setup()

from books.models import Book

books_data = [
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "isbn": "978-0061120084", "category": "Fiction", "quantity": 5, "description": "A classic of modern American literature that has won many hearts."},
    {"title": "1984", "author": "George Orwell", "isbn": "978-0451524935", "category": "Fiction", "quantity": 4, "description": "A dystopian social science fiction novel and cautionary tale."},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "isbn": "978-0141439518", "category": "Romance", "quantity": 6, "description": "A romantic novel of manners written by Jane Austen."},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "isbn": "978-0743273565", "category": "Fiction", "quantity": 5, "description": "A 1925 novel written by American author F. Scott Fitzgerald."},
    {"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "isbn": "978-0590353427", "category": "Fantasy", "quantity": 8, "description": "The first novel in the Harry Potter series."},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "isbn": "978-0547928227", "category": "Fantasy", "quantity": 5, "description": "A fantasy novel and children's book by J. R. R. Tolkien."},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "isbn": "978-0316769174", "category": "Fiction", "quantity": 4, "description": "A novel by J. D. Salinger, partially published in serial form."},
    {"title": "Lord of the Flies", "author": "William Golding", "isbn": "978-0399501487", "category": "Fiction", "quantity": 5, "description": "A 1954 novel by Nobel Prize-winning British author William Golding."},
    {"title": "Animal Farm", "author": "George Orwell", "isbn": "978-0451526342", "category": "Fiction", "quantity": 6, "description": "An allegorical novella by George Orwell."},
    {"title": "The Chronicles of Narnia", "author": "C.S. Lewis", "isbn": "978-0066238500", "category": "Fantasy", "quantity": 7, "description": "A series of seven fantasy novels by C. S. Lewis."},
    {"title": "Brave New World", "author": "Aldous Huxley", "isbn": "978-0060850524", "category": "Science Fiction", "quantity": 4, "description": "A dystopian novel written in 1931 by English author Aldous Huxley."},
    {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "isbn": "978-0544003415", "category": "Fantasy", "quantity": 5, "description": "An epic high-fantasy novel by English author J. R. R. Tolkien."},
    {"title": "Jane Eyre", "author": "Charlotte Bronte", "isbn": "978-0141441146", "category": "Romance", "quantity": 5, "description": "A novel by English writer Charlotte Brontë."},
    {"title": "Wuthering Heights", "author": "Emily Bronte", "isbn": "978-0141439556", "category": "Romance", "quantity": 4, "description": "An 1847 novel by Emily Brontë."},
    {"title": "The Alchemist", "author": "Paulo Coelho", "isbn": "978-0062315007", "category": "Fiction", "quantity": 6, "description": "A novel by Brazilian author Paulo Coelho."},
    {"title": "One Hundred Years of Solitude", "author": "Gabriel Garcia Marquez", "isbn": "978-0060883287", "category": "Fiction", "quantity": 4, "description": "A landmark 1967 novel by Colombian author Gabriel García Márquez."},
    {"title": "The Picture of Dorian Gray", "author": "Oscar Wilde", "isbn": "978-0141439570", "category": "Fiction", "quantity": 5, "description": "A philosophical novel by Irish writer Oscar Wilde."},
    {"title": "Frankenstein", "author": "Mary Shelley", "isbn": "978-0486282114", "category": "Horror", "quantity": 5, "description": "An 1818 novel written by English author Mary Shelley."},
    {"title": "Dracula", "author": "Bram Stoker", "isbn": "978-0486411095", "category": "Horror", "quantity": 5, "description": "An 1897 Gothic horror novel by Irish author Bram Stoker."},
    {"title": "The Odyssey", "author": "Homer", "isbn": "978-0140268867", "category": "Classics", "quantity": 4, "description": "One of two major ancient Greek epic poems attributed to Homer."},
    {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "isbn": "978-0486415871", "category": "Fiction", "quantity": 4, "description": "A novel by the Russian author Fyodor Dostoevsky."},
    {"title": "War and Peace", "author": "Leo Tolstoy", "isbn": "978-0199232765", "category": "Fiction", "quantity": 3, "description": "A literary work mixed with chapters on history and philosophy by Leo Tolstoy."},
    {"title": "The Divine Comedy", "author": "Dante Alighieri", "isbn": "978-0142437223", "category": "Classics", "quantity": 4, "description": "An Italian narrative poem by Dante Alighieri."},
    {"title": "Moby-Dick", "author": "Herman Melville", "isbn": "978-0142437247", "category": "Fiction", "quantity": 4, "description": "An 1851 novel by American writer Herman Melville."},
    {"title": "The Adventures of Huckleberry Finn", "author": "Mark Twain", "isbn": "978-0486280615", "category": "Fiction", "quantity": 5, "description": "A novel by Mark Twain, first published in 1884."},
    {"title": "A Tale of Two Cities", "author": "Charles Dickens", "isbn": "978-0486406510", "category": "Fiction", "quantity": 5, "description": "An 1859 historical novel by Charles Dickens."},
    {"title": "Great Expectations", "author": "Charles Dickens", "isbn": "978-0141439563", "category": "Fiction", "quantity": 5, "description": "The thirteenth novel by Charles Dickens."},
    {"title": "The Count of Monte Cristo", "author": "Alexandre Dumas", "isbn": "978-0140449266", "category": "Adventure", "quantity": 4, "description": "An adventure novel by French author Alexandre Dumas."},
    {"title": "Don Quixote", "author": "Miguel de Cervantes", "isbn": "978-0060934347", "category": "Classics", "quantity": 4, "description": "A Spanish novel by Miguel de Cervantes."},
    {"title": "Les Misérables", "author": "Victor Hugo", "isbn": "978-0451419439", "category": "Fiction", "quantity": 4, "description": "A French historical novel by Victor Hugo."},
    {"title": "The Three Musketeers", "author": "Alexandre Dumas", "isbn": "978-0140443882", "category": "Adventure", "quantity": 5, "description": "A historical adventure novel written by Alexandre Dumas."},
    {"title": "Anna Karenina", "author": "Leo Tolstoy", "isbn": "978-0143035008", "category": "Romance", "quantity": 4, "description": "A novel by the Russian author Leo Tolstoy."},
    {"title": "The Brothers Karamazov", "author": "Fyodor Dostoevsky", "isbn": "978-0374528379", "category": "Fiction", "quantity": 3, "description": "The final novel by the Russian author Fyodor Dostoevsky."},
    {"title": "Madame Bovary", "author": "Gustave Flaubert", "isbn": "978-0140449129", "category": "Fiction", "quantity": 4, "description": "A novel by Gustave Flaubert."},
    {"title": "The Iliad", "author": "Homer", "isbn": "978-0140275360", "category": "Classics", "quantity": 4, "description": "An ancient Greek epic poem attributed to Homer."},
    {"title": "Catch-22", "author": "Joseph Heller", "isbn": "978-1451626650", "category": "Fiction", "quantity": 5, "description": "A satirical novel by American author Joseph Heller."},
    {"title": "The Old Man and the Sea", "author": "Ernest Hemingway", "isbn": "978-0684801223", "category": "Fiction", "quantity": 5, "description": "A short novel written by Ernest Hemingway."},
    {"title": "Fahrenheit 451", "author": "Ray Bradbury", "isbn": "978-1451673319", "category": "Science Fiction", "quantity": 5, "description": "A dystopian novel by American writer Ray Bradbury."},
    {"title": "The Hunger Games", "author": "Suzanne Collins", "isbn": "978-0439023481", "category": "Science Fiction", "quantity": 7, "description": "A dystopian novel by Suzanne Collins."},
    {"title": "The Da Vinci Code", "author": "Dan Brown", "isbn": "978-0307474278", "category": "Mystery", "quantity": 6, "description": "A mystery thriller novel by Dan Brown."},
]

print("Adding books to database...")
added_count = 0
skipped_count = 0

for book_info in books_data:
    # Check if book already exists
    if Book.objects.filter(isbn=book_info['isbn']).exists():
        print(f"⚠ Skipped: {book_info['title']} (already exists)")
        skipped_count += 1
    else:
        Book.objects.create(**book_info)
        print(f"✓ Added: {book_info['title']}")
        added_count += 1

print(f"\n{'='*60}")
print(f"Summary:")
print(f"  • Books added: {added_count}")
print(f"  • Books skipped: {skipped_count}")
print(f"  • Total books in database: {Book.objects.count()}")
print(f"{'='*60}")
