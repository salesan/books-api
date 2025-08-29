import random
import sys
import requests
BASE = "http://localhost:8080"
HEADERS = {"Content-Type": "application/json"}

def test_health_check():
    r = requests.get(f"{BASE}/health", timeout=3)
    assert r.status_code == 200
    assert r.json().get("status") == "ok"
    print("Health check")

def test_get_book_by_id():
    r = requests.get(f"{BASE}/books/1", timeout=3)
    assert r.status_code == 200
    book = r.json()
    assert book["id"] == 1 and book["title"] == "To Kill a Mockingbird"
    print("Get by id")

def test_get_book_by_title():
    r = requests.get(f"{BASE}/books", params={"title": "1984"}, timeout=3)
    assert r.status_code == 200
    assert any(b["title"] == "1984" for b in r.json())
    print("Get by title")

def test_add_book():
    new_id = random.randint(1000, 9999)
    payload = {
    "id": new_id,
    "title": "The Hobbit",
    "author": "J. R. R. Tolkien",
    "pages": 310,
    "rating": 4.9,
    "price": 15.99,
    }
    r = requests.post(f"{BASE}/books", json=payload, headers=HEADERS, timeout=3)
    assert r.status_code in (200, 201)
    r = requests.get(f"{BASE}/books/{new_id}", timeout=3)
    assert r.status_code == 200 and r.json()["title"] == "The Hobbit"
    print("Add book")
    return new_id

def test_update_price_and_rating(book_id):
    patch = {"price": 12.49, "rating": 4.8}
    r = requests.put(f"{BASE}/books/{book_id}", json=patch, headers=HEADERS, timeout=3)
    print("Update price & rating", r.status_code, r.text)
    assert r.status_code == 200
    data = r.json()
    assert data["price"] == patch["price"] and data["rating"] == patch["rating"]
    print("Update price & rating")

def test_filter_by_pages():
    r = requests.get(f"{BASE}/books", params={"min_pages": 300}, timeout=3)
    assert r.status_code == 200
    books = r.json()
    assert books and all(b["pages"] >= 300 for b in books)
    print("Filter by pages")

def test_validation_missing_fields():
    bad_payload = {"title": "Missing many fields"}
    r = requests.post(f"{BASE}/books", json=bad_payload, headers=HEADERS, timeout=3)
    assert r.status_code in (400, 422), "Server did not reject missing-field payload"
    print("Validation (missing fields)")

def test_validation_invalid_values():
    bad_payload = {
    "id": -5,
    "title": "Bad Data",
    "author": "Nobody",
    "pages": "three hundred",
    "rating": 6.0,
    "price": -1.00,
    }
    r = requests.post(f"{BASE}/books", json=bad_payload, headers=HEADERS, timeout=3)
    assert r.status_code in (400, 422), "Server accepted invalid value types/ranges"
    print("Validation (invalid values)")

def main():
    test_health_check()
    test_get_book_by_id()
    test_get_book_by_title()
    new_id = test_add_book()
    test_update_price_and_rating(new_id)
    test_filter_by_pages()
    test_validation_missing_fields()
    test_validation_invalid_values()
    print("ALL TESTS PASSED")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print("TEST FAILED:", str(exc))
        sys.exit(1)
    except Exception as exc:
        print("ERROR:", str(exc))
        sys.exit(1)
