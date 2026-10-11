from datetime import date
from sqlalchemy.orm import Session
from ..models.loan import Loan
from ..models.book import Book

def create_loan(db: Session, user_id: int, book_id: int, due_date: date | None = None) -> Loan | None:
    book = db.get(Book, book_id)
    if not book or book.copies_available <= 0:
        return None
    book.copies_available -= 1
    loan = Loan(user_id=user_id, book_id=book_id, due_date=due_date)
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan

def return_loan(db: Session, loan_id: int, return_date: date | None = None):
    loan = db.get(Loan, loan_id)
    if not loan:
        return None
    if loan.status == "returned":
        return loan
    book = db.get(Book, loan.book_id)
    if book and book.copies_available < book.copies_total:
        book.copies_available += 1
    loan.return_date = return_date or date.today()
    loan.status = "returned"
    db.commit()
    db.refresh(loan)
    return loan
