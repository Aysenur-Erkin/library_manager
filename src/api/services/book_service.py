from sqlalchemy.orm import Session
from ..models.book import Book
def decrement_available(db: Session, book_id: int):
    book = db.get(Book, book_id)
    if not book or book.copies_available <= 0: return None
    book.copies_available -= 1; db.add(book); db.commit(); db.refresh(book); return book
def increment_available(db: Session, book_id: int):
    book = db.get(Book, book_id)
    if not book: return None
    if book.copies_available < book.copies_total:
        book.copies_available += 1; db.add(book); db.commit(); db.refresh(book)
    return book
