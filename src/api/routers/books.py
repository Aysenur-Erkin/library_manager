from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ..schemas.book import BookCreate, BookUpdate, BookOut
from ..models.book import Book
router = APIRouter(prefix="/books", tags=["books"])
@router.get("/", response_model=list[BookOut])
def list_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Book).offset(skip).limit(limit).all()
@router.post("/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    book = Book(**payload.dict()); db.add(book); db.commit(); db.refresh(book); return book
@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book: raise HTTPException(status_code=404, detail="Book not found")
    return book
@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    book = db.get(Book, book_id)
    if not book: raise HTTPException(status_code=404, detail="Book not found")
    for k, v in payload.dict(exclude_unset=True).items(): setattr(book, k, v)
    db.add(book); db.commit(); db.refresh(book); return book
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    book = db.get(Book, book_id)
    if not book: raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book); db.commit(); return None
