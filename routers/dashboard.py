from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
import models
import schemas
import oauth2

router = APIRouter(prefix="/dashboard",tags = ["Dashboard"])

@router.get("/", response_model=schemas.DashboardResponse)
def get_dashboard(db: Session = Depends(get_db), current_user = Depends(oauth2.require_member)):
    total_books = db.query(models.Book).count()
    total_authors = db.query(models.Author).count()
    total_categories = db.query(models.Category).count()

    if current_user.role in ["admin", "librarian"]:
        total_users = db.query(models.User).count()
        total_borrowings = db.query(models.Borrowing).count()
        active_borrowings = db.query(models.Borrowing).filter(models.Borrowing.status == "borrowed").count()
        returned_borrowings = db.query(models.Borrowing).filter(models.Borrowing.status == "returned").count()
        overdue_borrowings = db.query(models.Borrowing).filter(models.Borrowing.status == "borrowed", models.Borrowing.due_date < datetime.now()).count()
        available_books = total_books - active_borrowings

        return {
            "role": current_user.role,
            "total_books": total_books,
            "total_authors": total_authors,
            "total_categories": total_categories,
            "total_users": total_users,
            "total_borrowings": total_borrowings,
            "active_borrowings": active_borrowings,
            "overdue_borrowings": overdue_borrowings,
            "returned_borrowings": returned_borrowings,
            "available_books": available_books
        }
    
    total_borrowings = db.query(models.Borrowing).filter(models.Borrowing.user_id == current_user.id).count()
    active_borrowings = db.query(models.Borrowing).filter(models.Borrowing.status == "borrowed", models.Borrowing.user_id == current_user.id).count()
    returned_borrowings = db.query(models.Borrowing).filter(models.Borrowing.status == "returned", models.Borrowing.user_id == current_user.id).count()
    overdue_borrowings = db.query(models.Borrowing).filter(models.Borrowing.user_id == current_user.id, models.Borrowing.status == "borrowed", models.Borrowing.due_date < datetime.now()).count()
    available_books = total_books - active_borrowings

    return {
            "role": current_user.role,
            "total_books": total_books,
            "total_authors": total_authors,
            "total_categories": total_categories,
            "total_users": None,
            "total_borrowings": total_borrowings,
            "active_borrowings": active_borrowings,
            "overdue_borrowings": overdue_borrowings,
            "returned_borrowings": returned_borrowings,
            "available_books": available_books
        }
    