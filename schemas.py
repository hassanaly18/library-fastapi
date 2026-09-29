from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

class UserCreate(BaseModel):
    username: str 
    email: EmailStr
    password: str 
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRole(str, Enum):
    admin = "admin"
    librarian = "librarian"
    member = "member"

class UserResponse(BaseModel):
    id: int
    username: str 
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True

class UserRoleUpdate(BaseModel):
    role: UserRole

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

class PaginationMeta(BaseModel): 
    page: int
    limit: int 
    total: int
    total_pages: int 

class PaginatedBookResponse(BaseModel):
    items: list[BookResponse]
    page: int
    limit: int 
    total: int
    total_pages: int 

class PaginatedAuthorResponse(BaseModel):
    items: list[AuthorResponse]
    page: int
    limit: int 
    total: int
    total_pages: int 

class PaginatedCategoryResponse(BaseModel):
    items: list[CategoryResponse]
    page: int
    limit: int 
    total: int
    total_pages: int 

class PaginatedBorrowingResponse(BaseModel):
    items: list[BorrowingResponse]
    page: int
    limit: int 
    total: int
    total_pages: int 

class PaginatedUserResponse(BaseModel):
    items: list[UserResponse]
    page: int
    limit: int 
    total: int
    total_pages: int 

class DashboardResponse(BaseModel):
    role: UserRole
    total_books: int
    total_authors: int 
    total_categories: int

    total_users: int |None=None

    total_borrowings: int 
    active_borrowings: int
    overdue_borrowings: int 
    returned_borrowings: int 
    available_books: int

class PopularBookStat(BaseModel):
    book_id: int
    title: str
    borrow_count: int 

class LibraryStatisticsResponse(BaseModel):
    total_books: int
    total_authors: int
    total_categories: int
    total_users: int 
    total_borrowings: int
    active_borrowings: int
    returned_borrowings: int
    overdue_borrowings: int
    available_books: int
    most_borrowed_books: list[PopularBookStat]