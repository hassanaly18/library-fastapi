from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db
import oauth2

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.post("/", response_model=schemas.CategoryResponse)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.require_librarian)):
    new_category = models.Category(
        name=category.name,
        description=category.description
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/", response_model=list[schemas.CategoryResponse])
def get_categories(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    categories = db.query(models.Category).all()
    return categories

@router.get("/{category_id}", response_model=schemas.CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    
    return category

@router.put("/{category_id}", response_model=schemas.CategoryResponse)
def update_category(category_id: int, category_data: schemas.CategoryCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.require_librarian)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    
    category.name = category_data.name
    category.bio = category_data.bio

    db.commit()
    db.refresh(category)
    return category

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.require_librarian)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    
    db.delete(category)
    db.commit()
    return {
        "message": "Category deleted successfully"
    }