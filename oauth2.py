from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db


SECRET_KEY = "this_is_the_jwt_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login"
)

def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def verify_access_token(token:str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate":"Bearer"}
    )
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms = [ALGORITHM]
        )
        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(
            id = user_id
        )

        return token_data
    except JWTError:
        raise credentials_exception

def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token_data = verify_access_token(token)

    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    return user

def require_admin(current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return current_user

def require_librarian(current_user = Depends(get_current_user)):
    if current_user.role not in ["librarian", "admin"]:
        raise HTTPException(status_code=403, detail="Librarian access required")
    
    return current_user

def require_member(current_user = Depends(get_current_user)):
    if current_user.role not in ["member", "librarian", "admin"]:
        raise HTTPException(status_code=403, detail="Valid user role required")
    
    return current_user

def require_roles(allowed_roles: list[str]):
    def role_checker(current_user = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="You do not have the permission"
            )
        return current_user
    return role_checker
