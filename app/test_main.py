import pytest
from fastapi.testclient import TestClient
from main import app
from models import Book
from sqlmodel import Session, text
from database import engine

client = TestClient(app)


# ----------------------
# Fixture: DB session
# ----------------------
@pytest.fixture
def session():
    with Session(engine) as s:
        yield s

# ----------------------
# Fixture: ID generator
# ----------------------
@pytest.fixture()
def generate_id():
    """Generate a unique ID for testing."""
    with Session(engine) as session:
        result = session.exec(text("SELECT MAX(id) FROM book"))
        max_id = result.one()[0] or 0
        return max_id + 1

# ----------------------
# Fixture: temporary book
# ----------------------
@pytest.fixture
def temp_book(session, generate_id):
    book = Book(id=generate_id, title="Temp Test Book", author="Fixture Author", pages=123, rating=4.5, price=9.99)
    session.add(book)
    session.commit()
    session.refresh(book)
    yield book
    # Cleanup after test
    session.delete(book)
    session.commit()


# ----------------------
# Health check test
# ----------------------
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ----------------------
# Get all books test
# ----------------------
def test_get_books(session):
    response = client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1  # seeded books from migrations


# ----------------------
# Get book by ID test
# ----------------------
def test_get_book_by_id(temp_book):
    response = client.get(f"/books/{temp_book.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == temp_book.id
    assert data["title"] == temp_book.title


# ----------------------
# Get books by title test
# ----------------------
def test_get_books_by_title(temp_book):
    response = client.get(f"/books?title={temp_book.title}")
    assert response.status_code == 200
    data = response.json()
    assert any(b["id"] == temp_book.id for b in data)


# ----------------------
# Get books by min_pages test
# ----------------------
def test_get_books_by_min_pages(temp_book):
    response = client.get(f"/books?min_pages={temp_book.pages - 1}")
    assert response.status_code == 200
    data = response.json()
    assert any(b["id"] == temp_book.id for b in data)


# ----------------------
# Add a new book test
# ----------------------
def test_add_book(session, generate_id):
    new_book = {
        "id": generate_id,
        "title": "Integration Test Book",
        "author": "Test Author",
        "pages": 200,
        "rating": 4.2,
        "price": 15.99
    }
    response = client.post("/books", json=new_book)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == new_book["title"]

    # Cleanup
    book = session.get(Book, data["id"])
    session.delete(book)
    session.commit()


# ----------------------
# Update book (update price/rating) test
# ----------------------
def test_update_book(temp_book, session):
    update_data = {"price": 19.99, "rating": 4.9}
    response = client.put(f"/books/{temp_book.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 19.99
    assert data["rating"] == 4.9

# ----------------------
# Get book by ID: not found
# ----------------------
def test_get_book_by_id_not_found():
    response = client.get("/books/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

# ----------------------
# Add book: missing required fields
# ----------------------
def test_add_book_missing_fields():
    incomplete_book = {
        "title": "Missing Author",
        "pages": 100,
        "rating": 3.5,
        "price": 10.0
        # Missing 'author'
    }
    response = client.post("/books", json=incomplete_book)
    assert response.status_code == 422  # Unprocessable Entity

# ----------------------
# Update book: book not found
# ----------------------
def test_update_book_not_found():
    update_data = {"price": 12.99, "rating": 4.0}
    response = client.put("/books/999999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

# ----------------------
# Update book: no fields to update
# ----------------------
def test_update_book_no_fields(temp_book):
    response = client.put(f"/books/{temp_book.id}", json={})
    assert response.status_code == 422
    # Check that the response contains validation errors for missing fields
    assert isinstance(response.json()["detail"], list)
    assert any("Field required" in err["msg"] for err in response.json()["detail"])

# ----------------------
# Get books: filter returns empty list
# ----------------------
def test_get_books_filter_empty():
    response = client.get("/books?title=NoSuchTitle")
    assert response.status_code == 200
    assert response.json() == []

# ----------------------
# Add book: duplicate ID
# ----------------------
def test_add_book_duplicate_id(temp_book):
    duplicate_book = {
        "id": temp_book.id,
        "title": "Duplicate ID Book",
        "author": "Author",
        "pages": 100,
        "rating": 3.0,
        "price": 5.0
    }
    response = client.post("/books", json=duplicate_book)
    # Should fail due to unique constraint violation
    assert response.status_code in (400, 409, 422)
