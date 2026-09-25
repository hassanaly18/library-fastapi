from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
import oauth2

router = APIRouter(prefix="/users",tags = ["Users"])

@router.get("/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db), current_user = Depends(oauth2.require_admin)):
    users = db.query(models.User).all()
    return users

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.require_admin)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@router.put("/{user_id}/role", response_model=schemas.UserResponse)
def update_user_role(user_id: int, role_data: schemas.UserRoleUpdate, db: Session = Depends(get_db), current_user = Depends(oauth2.require_admin)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    if user.id == current_user.id and role_data.role.value != "admin":
        raise HTTPException(
            status_code=400,
            detail="You can not remove your own admin role"
        )
    
    user.role = role_data.role.value

    db.commit()
    db.refresh(user)

    return user 