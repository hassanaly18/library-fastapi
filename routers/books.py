from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db
import oauth2

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

@router.get("/", response_model=list[schemas.BookResponse])
def get_books(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    books = db.query(models.Book).all()
    return books

@router.delete("/{book_id}")
def delete_book(book_id: int, current_user = Depends(oauth2.require_roles(["admin", "librarian"]))):
    return {
        "message": "Book deleted"
    }

@router.post("/", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
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
def borrow_book(book_id: int, current_user = Depends(oauth2.require_roles(["member"]))):
    return {
        "message": f"Book {book_id} borrowed",
        "borrowed_by": current_user.username
    }