from pydantic import BaseModel
class BookBase(BaseModel):
    title: str
    description: str | None = None
    author_id: int
    isbn: str | None = None
    published_year: int | None = None
    copies_total: int = 1
    copies_available: int = 1
class BookCreate(BookBase): pass
class BookUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    author_id: int | None = None
    isbn: str | None = None
    published_year: int | None = None
    copies_total: int | None = None
    copies_available: int | None = None
class BookOut(BookBase):
    id: int
    class Config: from_attributes = True
