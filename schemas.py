from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str 
    email: EmailStr
    password: str 
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str 
    email: EmailStr
    role: str 

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str 
    token_type: str 

class TokenData(BaseModel):
    id: int | None = None

class AuthorShort(BaseModel):
    id: int
    name: str 

    class Config:
        from_attributes = True

class CategoryShort(BaseModel):
    id: int
    name: str 

    class Config:
        from_attributes = True

class BookCreate(BaseModel):
    title: str
    author_id: int
    category_id: int

class BookResponse(BaseModel):
    id: int
    title: str
    author: AuthorShort
    category: CategoryShort

    class Config:
        from_attributes = True

class AuthorCreate(BaseModel):
    name: str 
    bio: str | None = None

class AuthorResponse(BaseModel):
    id: int
    name: str
    bio: str | None = None

    class Config:
        from_attributes = True

class CategoryCreate(BaseModel):
    name:str
    description:str | None = None

class CategoryResponse(BaseModel):
    id:int
    name:str
    description:str | None = None

    class Config:
        from_attributes = True

class BorrowingCreate(BaseModel):
    book_id: int
    due_date: datetime

class BorrowingResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrow_date: datetime
    due_date: datetime
    return_date: datetime | None = None
    status: str
    
    class Config:
        from_attributes = True 

class BorrowingWithBook(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrow_date: datetime
    due_date: datetime
    return_date: datetime | None = None
    status: str
    book: BookResponse
    
    class Config:
        from_attributes = True 