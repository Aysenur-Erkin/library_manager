from pydantic import BaseModel
from datetime import date
class LoanCreate(BaseModel):
    user_id: int
    book_id: int
    due_date: date | None = None
class LoanReturn(BaseModel):
    return_date: date | None = None
class LoanOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    loan_date: date
    due_date: date | None = None
    return_date: date | None = None
    status: str
    class Config: from_attributes = True
