from fastapi import FastAPI
from database import engine
import models
from auth import router as auth_router
from routers import books, authors, categories, borrowings

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Library Management API")

app.include_router(auth_router)
app.include_router(books.router)
app.include_router(authors.router)
app.include_router(categories.router)
app.include_router(borrowings.router)

@app.get("/")
def home():
    return {
        "message": "Welcome to Library Management API"
    }