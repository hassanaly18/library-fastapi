from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db
import oauth2

router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)

@router.post("/", response_model=schemas.AuthorResponse)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    new_author = models.Author(
        name= author.name,
        bio=author.bio
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

@router.get("/", response_model=list[schemas.AuthorResponse])
def get_authors(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    authors = db.query(models.Author).all()
    return authors

@router.get("/{author_id}", response_model=schemas.AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )
    
    return author

@router.put("/{author_id}", response_model=schemas.AuthorResponse)
def update_author(author_id: int, author_data: schemas.AuthorCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )
    
    author.name = author_data.name
    author.bio = author_data.bio

    db.commit()
    db.refresh(author)
    return author

@router.delete("/{author_id}")
def update_author(author_id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )
    
    db.delete(author)
    db.commit()
    return {
        "message": "Author deleted successfully"
    }

@router.get("/{author_id}/books", response_model=list[schemas.BookResponse])
def get_author_books(author_id: int, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )
    
    return author.books 