from pydantic import BaseModel
class AuthorBase(BaseModel):
    name: str
    biography: str | None = None
class AuthorCreate(AuthorBase): pass
class AuthorUpdate(BaseModel):
    name: str | None = None
    biography: str | None = None
class AuthorOut(AuthorBase):
    id: int
    class Config: from_attributes = True
