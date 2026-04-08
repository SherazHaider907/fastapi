from typing import Optional
from fastapi import FastAPI #,Body
from pydantic import BaseModel,Field

app = FastAPI()


class Book:
    id: int
    title: str
    auther: str
    description: str
    rating: int


    def __init__(self, id, title, auther, description, rating):
        self.id = id
        self.title = title
        self.auther = auther
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id: Optional[int] = Field(description = 'ID is not needed to create a book',default=None)
    title: str = Field(min_length=3)
    auther: str = Field(min_length=1)
    description: str = Field(min_length=1 , max_length=100)
    rating: int = Field(gt=-1, lt=6)

    model_config = {
        "json_schema_extra":{
            "example":{
                "title": "A new book",
                "auther": "Harvard University",
                "description": "A new description for the a book",
                "rating": 5
            }
        }
    }

BOOKS = [
    Book(
        1,
        "Computer Science Fundamentals",
        "Harvard University",
        "A beginner-friendly introduction to core computer science concepts including programming basics, algorithms, and problem-solving techniques.",
        5
    ),
    Book(
        2,
        "Data Structures Essentials",
        "Tenzela Academy",
        "Covers important data structures like arrays, linked lists, stacks, queues, trees, and graphs with practical explanations.",
        4
    ),
    Book(
        3,
        "Introduction to Algorithms",
        "MIT",
        "A comprehensive guide to algorithms covering sorting, searching, dynamic programming, and complexity analysis for advanced learners.",
        5
    ),
    Book(
        4,
        "Python Programming Basics",
        "Open Learning Institute",
        "Explains Python fundamentals including variables, loops, functions, and object-oriented programming with simple examples.",
        5
    ),
    Book(
        5,
        "Web Development with Django",
        "Django Community",
        "A practical guide to building web applications using Django, covering models, views, templates, and REST APIs.",
        4
    ),
    Book(
        6,
        "Machine Learning Introduction",
        "Stanford University",
        "Introduces machine learning concepts such as supervised learning, unsupervised learning, and model evaluation techniques.",
        5
    ),
    Book(
        7,
        "Database Systems Concepts",
        "University Press",
        "Covers relational databases, SQL queries, normalization, indexing, and transaction management in detail.",
        4
    )
]

@app.get("/books")
async def read_all_books():
    return BOOKS

# simple way to create book
# @app.post("/create_books")
# async def create_book(book_request = Body()):
#     BOOKS.append(book_request)
#     # return book_request

# using pydantic model to create book
@app.post("/create_books")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))
    # return new_book

def find_book_id(book:Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book