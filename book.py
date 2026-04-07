from fastapi import FastAPI

app = FastAPI()


BOOKS = [
    {
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
        'category': 'Classic Literature',
        'published_year': 1925
    },

    {
        'title': 'To Kill a Mockingbird',
        'author': 'Harper Lee',
        'category': 'Fiction',
        'published_year': 1960
    },

    {
        'title': '1984',
        'author': 'George Orwell',
        'category': 'Dystopian Fiction',
        'published_year': 1948
    },

    {
        'title': 'Pride and Prejudice',
        'author': 'Jane Austen',
        'category': 'Romance',
        'published_year': 1813
    },

    {
        'title': 'The Catcher in the Rye',
        'author': 'J.D. Salinger',
        'category': 'Fiction',
        'published_year': 1951
    }
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_title}")
async def read_book(book_title : str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
    return {'error': 'Book not found'}

@app.get("/books/")
async def read_books_by_query(category : str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/{book_author}")
async def read_author_category(book_author : str, category : str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return