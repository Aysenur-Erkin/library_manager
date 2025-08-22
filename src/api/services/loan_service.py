from datetime import date
from sqlalchemy.orm import Session
from ..models.loan import Loan
def create_loan(db: Session, user_id: int, book_id: int, due_date: date | None = None) -> Loan:
    loan = Loan(user_id=user_id, book_id=book_id, due_date=due_date); db.add(loan); db.commit(); db.refresh(loan); return loan
def return_loan(db: Session, loan_id: int, return_date: date | None = None):
    loan = db.get(Loan, loan_id)
    if not loan: return None
    loan.return_date = return_date or date.today(); loan.status = "returned"; db.add(loan); db.commit(); db.refresh(loan); return loan
