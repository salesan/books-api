from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session, select
from models import Book, BookCreate, BookUpdate
from database import engine, get_session
from typing import List

app = FastAPI(title="Books API")

@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.get("/books", response_model=List[Book])
def get_books(
    title: str = Query(None),
    min_pages: int = Query(None),
    session: Session = Depends(get_session)
) -> List[Book]:
    query = select(Book)
    if title:
        query = query.where(Book.title.ilike(f"%{title}%"))
    if min_pages:
        query = query.where(Book.pages >= min_pages)

    return session.exec(query).all()


@app.get("/books/{book_id}", response_model=Book)
def get_book_by_id(book_id: int, session: Session = Depends(get_session)) -> Book:
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.post("/books", response_model=Book, status_code=201)
def add_book(book_create: BookCreate, session: Session = Depends(get_session)) -> Book:
    book: Book = Book.model_validate(book_create)
    session.add(book)
    session.commit()
    session.refresh(book)

    return book


@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book_update: BookUpdate, session: Session = Depends(get_session)) -> Book:
    if not book_update.price and not book_update.rating:
        raise HTTPException(status_code=400, detail="No fields to update")
    book: Book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book_update.price is not None:
        book.price = book_update.price
    if book_update.rating is not None:
        book.rating = book_update.rating
    session.add(book)
    session.commit()
    session.refresh(book)

    return book
