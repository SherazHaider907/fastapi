from fastapi import FastAPI

app = FastAPI()

@app.get("/api-endpoint")
async def book_api():
    return {"message": "Welcome to the Book API!"}