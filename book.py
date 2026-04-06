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