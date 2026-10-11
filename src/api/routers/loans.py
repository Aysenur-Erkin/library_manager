from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ..schemas.loan import LoanCreate, LoanReturn, LoanOut
from ..models.loan import Loan
from ..services.loan_service import create_loan as svc_create_loan, return_loan as svc_return_loan

router = APIRouter(prefix="/loans", tags=["loans"])

@router.get("/", response_model=list[LoanOut])
def list_loans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Loan).offset(skip).limit(limit).all()

@router.post("/", response_model=LoanOut, status_code=status.HTTP_201_CREATED)
def create_loan(payload: LoanCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    loan = svc_create_loan(db, user_id=user.id, book_id=payload.book_id, due_date=payload.due_date)
    if not loan:
        raise HTTPException(status_code=400, detail="Book not available")
    return loan

@router.post("/{loan_id}/return", response_model=LoanOut)
def return_loan(loan_id: int, payload: LoanReturn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    loan = svc_return_loan(db, loan_id=loan_id, return_date=payload.return_date)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan
