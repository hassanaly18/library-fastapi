from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from datetime import datetime
import models
import schemas
import oauth2

router = APIRouter(prefix="/statistics",tags = ["Statistics"])

@router.get("/", response_model=schemas.LibraryStatisticsResponse)
def get_statistics(db: Session = Depends(get_db), current_user = Depends(oauth2.require_librarian)):
    total_books = db.query(models.Book).count()
    total_authors = db.query(models.Author).count()
    total_categories = db.query(models.Category).count()
    total_users = db.query(models.User).count()
    total_borrowings = db.query(models.Borrowing).count()
    active_borrowings = db.query(models.Borrowing).filter(models.Borrowing.status == "borrowed").count()
    returned_borrowings = db.query(models.Borrowing).filter(models.Borrowing.status == "returned").count()
    overdue_borrowings = db.query(models.Borrowing).filter(models.Borrowing.status == "borrowed", models.Borrowing.due_date < datetime.now()).count()
    available_books = total_books - active_borrowings

    popular_books = (
        db.query(
            models.Book.id.label("book_id"),
            models.Book.title.label("title"),
            func.count(
                models.Borrowing.id
            ).label("borrow_count")
        ).outerjoin(
            models.Borrowing,
            models.Book.id == models.Borrowing.book_id
        ).group_by(
            models.Book.id,
            models.Book.title
        ).order_by(
            func.count(
                models.Borrowing.id
            ).desc()
        ).limit(5).all()
    )

    most_borrowed_books = [
        {
            "book_id": book.book_id,
            "title": book.title,
            "borrow_count": book.borrow_count
        }
        
        for book in popular_books
    ]

    return {
        "total_books": total_books,
        "total_authors": total_authors,
        "total_categories": total_categories,
        "total_users": total_users,
        "total_borrowings": total_borrowings,
        "active_borrowings": active_borrowings,
        "overdue_borrowings": overdue_borrowings,
        "returned_borrowings": returned_borrowings,
        "available_books": available_books,
        "most_borrowed_books": most_borrowed_books
    }