from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ..schemas.author import AuthorCreate, AuthorUpdate, AuthorOut
from ..models.author import Author
router = APIRouter(prefix="/authors", tags=["authors"])
@router.get("/", response_model=list[AuthorOut])
def list_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Author).offset(skip).limit(limit).all()
@router.post("/", response_model=AuthorOut, status_code=status.HTTP_201_CREATED)
def create_author(payload: AuthorCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    author = Author(**payload.dict()); db.add(author); db.commit(); db.refresh(author); return author
@router.get("/{author_id}", response_model=AuthorOut)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.get(Author, author_id)
    if not author: raise HTTPException(status_code=404, detail="Author not found")
    return author
@router.put("/{author_id}", response_model=AuthorOut)
def update_author(author_id: int, payload: AuthorUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    author = db.get(Author, author_id)
    if not author: raise HTTPException(status_code=404, detail="Author not found")
    for k, v in payload.dict(exclude_unset=True).items(): setattr(author, k, v)
    db.add(author); db.commit(); db.refresh(author); return author
@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    author = db.get(Author, author_id)
    if not author: raise HTTPException(status_code=404, detail="Author not found")
    db.delete(author); db.commit(); return None
