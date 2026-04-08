from fastapi import Body, FastAPI

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

# Get all books
@app.get("/books")
async def read_all_books():
    return BOOKS


# Get book by title (path)
@app.get("/books/title/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
    return {'error': 'Book not found'}


# Get books by category (query)
@app.get("/books/by-category/")
async def read_books_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


# Get books by author (query)
@app.get("/books/by-author/")
async def read_books_by_author(author_name: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author_name.casefold():
            books_to_return.append(book)
    return books_to_return


# Get books by author + category (path + query)
@app.get("/books/author-category/{book_author}")
async def read_author_category(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if (
            book.get('author').casefold() == book_author.casefold()
            and book.get('category').casefold() == category.casefold()
        ):
            books_to_return.append(book)
    return books_to_return


# Create book
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    return BOOKS


# Update book
@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
            return BOOKS


# Delete book
@app.delete("/books/delete_book")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            return BOOKS