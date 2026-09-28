from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db
import oauth2

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

# @router.get("/", response_model=list[schemas.BookResponse])
# def get_books(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
#     books = db.query(models.Book).all()
#     return books

@router.get("/", response_model=schemas.PaginatedBookResponse)
def get_books(q: str | None = Query(default=None, description="Search by title"), 
author_id: int | None = Query(default=None), 
category_id: int | None = Query(default=None),
page: int = Query(default=1, ge=1),
limit: int = Query(default=10, ge=1, le=25),
db: Session = Depends(get_db), 
current_user = Depends(oauth2.get_current_user)):
    query = (db.query(models.Book).join(models.Author).join(models.Category))

    if q:
        search = f"%{q}%"

        query = query.filter(
            or_(
                models.Book.title.ilike(search)
            )
        )
    
    if author_id is not None:
        query = query.filter(
            models.Book.author_id == author_id
        )

    if category_id is not None:
        query = query.filter(
            models.Category.category_id == category_id
        )
    
    total = query.count()
    offset = (page - 1) * limit

    books = (query.offset(offset).limit(limit).all())
    total_pages = (total + limit - 1) // limit

    return {
        "items": books,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages
    }

@router.delete("/{book_id}")
def delete_book(book_id: int, current_user = Depends(oauth2.require_librarian)):
    return {
        "message": "Book deleted"
    }

@router.post("/", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.require_librarian)):
    author = db.query(models.Author).filter(models.Author.id == book.author_id).first()

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )
    
    category = db.query(models.Category).filter(models.Category.id == book.category_id).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    
    new_book = models.Book(
        title = book.title,
        author_id = book.author_id,
        category_id = book.category_id
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.post("/{book_id}/borrow")
def borrow_book(book_id: int, current_user = Depends(oauth2.require_member)):
    return {
        "message": f"Book {book_id} borrowed",
        "borrowed_by": current_user.username
    }

@router.get("/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id:int, db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if book is None:
        raise HTTPException(status_code=404, detail = "Author not found")

    return book