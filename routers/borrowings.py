from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
import models
import schemas
import oauth2

router = APIRouter(prefix="/borrowings",tags = ["Borrowings"])

@router.post("/", response_model=schemas.BorrowingWithBook)
def borrow_book(borrowing: schemas.BorrowingCreate, db: Session=Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    book = db.query(models.Book).filter(models.Book.id == borrowing.book_id).first()

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    
    if borrowing.due_date <= datetime.now():
        raise HTTPException(
            status_code=400,
            detail="Due must be in the future"
        )
    
    active_borrowing = db.query(models.Borrowing).filter(models.Borrowing.book_id == borrowing.book_id, models.Borrowing.status=="borrowed").first()
    
    if active_borrowing is not None:
        raise HTTPException(
            status_code=400,
            detail="Book is already borrowed"
        )

    new_borrowing = models.Borrowing(
        user_id = current_user.id,
        book_id = borrowing.book_id,
        borrow_date = datetime.now(),
        due_date = borrowing.due_date,
        status = "borrowed"
    )

    db.add(new_borrowing)
    db.commit()
    db.refresh(new_borrowing)
    return new_borrowing

@router.get("/", response_model=list[schemas.BorrowingWithBook])
def get_all_borrowings(db: Session=Depends(get_db), current_user = Depends(oauth2.require_librarian)):
    borrowings = db.query(models.Borrowing).all()

    return borrowings

@router.get("/my", response_model=list[schemas.BorrowingWithBook])
def get_my_borrowings(db: Session = Depends(get_db), current_user = Depends(oauth2.require_member)):
    borrowings = db.query(models.Borrowing).filter(models.Borrowing.user_id == current_user.id).all()
    return borrowings

@router.get("/{borrowing_id}", response_model=schemas.BorrowingWithBook)
def get_borrowing(borrowing_id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    borrowing = db.query(models.Borrowing).filter(models.Borrowing.id == borrowing_id).first()

    if borrowing is None:
        raise HTTPException(
            status_code=404,
            detail="Borrowing record not found"
        )
        return borrowing

#return routes

@router.put("/{borrowing_id}/return")
def return_book(borrowing_id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.require_member)):
    borrowing = db.query(models.Borrowing).filter(models.Borrowing.id == borrowing_id).first()

    if borrowing is None:
        raise HTTPException(
            status_code=404,
            detail="Borrowing record not found"
        )
    
    if borrowing.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only return your own borrowed book"
        )
    
    if borrowing.status == "returned":
        raise HTTPException(
            status_code=400,
            detail="Book has already been returned"
        )
    
    borrowing.return_date = datetime.now()
    borrowing.status = "returned"

    db.commit()
    db.refresh(borrowing)

    return borrowing