from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from .settings import settings
from .db import Base, engine
from .routers import users, books, authors, loans
from .routers import auth as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="library_manager", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

web_dir = Path(__file__).resolve().parents[2] / "web"
if web_dir.exists():
    app.mount("/ui", StaticFiles(directory=str(web_dir), html=True), name="ui")

@app.get("/")
def root_redirect():
    return RedirectResponse(url="/docs")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth_router.router)
app.include_router(users.router)
app.include_router(authors.router)
app.include_router(books.router)
app.include_router(loans.router)
