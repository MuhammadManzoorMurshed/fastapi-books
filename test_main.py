import sys, os
sys.path.append(os.path.dirname(__file__))  # নিশ্চিত করার জন্য main.py detect হবে

from fastapi.testclient import TestClient
from main import app, books  # app import করলাম

client = TestClient(app)

def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to the Book Management System"}

def test_add_and_get_book():
    books.clear()  # reset before test
    new_book = {"id": 1, "name": "Python 101", "description": "Intro to Python", "isAvailable": True}
    response = client.post("/book", json=new_book)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Python 101"

    response = client.get("/book")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 1

def test_update_book():
    updated_book = {"id": 1, "name": "Python Advanced", "description": "Deep Python", "isAvailable": False}
    response = client.put("/book/1", json=updated_book)
    assert response.status_code == 200
    assert response.json()["name"] == "Python Advanced"

def test_delete_book():
    response = client.delete("/book/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

    response = client.delete("/book/1")
    assert response.status_code == 200
    assert response.json() == {"error": "Book not found, deletion failed"}
