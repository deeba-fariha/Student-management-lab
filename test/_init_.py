from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


# GET - Get all students
def test_get_all_students():

    response = client.get("/students")

    assert response.status_code == 200
    assert len(response.json()) >= 1


# GET - Get one student
def test_get_single_student():

    response = client.get("/students/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Rahim"


# Invalid Scenario 1
# GET a student that does not exist
def test_get_nonexistent_student():

    response = client.get("/students/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"


# POST - Create a new student
def test_create_student():

    new_student = {
        "id": 10,
        "name": "Sabbir",
        "department": "CSE",
        "semester": 6,
        "cgpa": 3.90
    }

    response = client.post(
        "/students",
        json=new_student
    )

    assert response.status_code == 201
    assert response.json()["id"] == 10
    assert response.json()["name"] == "Sabbir"


# Invalid Scenario 2
# POST a student with duplicate ID
def test_create_duplicate_student():

    new_student = {
        "id": 1,
        "name": "Another Student",
        "department": "BBA",
        "semester": 2,
        "cgpa": 3.20
    }

    response = client.post(
        "/students",
        json=new_student
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student ID already exists"


# PUT - Update a student
def test_update_student():

    updated_student = {
        "id": 1,
        "name": "Rahim Updated",
        "department": "CSE",
        "semester": 6,
        "cgpa": 3.85
    }

    response = client.put(
        "/students/1",
        json=updated_student
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Rahim Updated"
    assert response.json()["cgpa"] == 3.85


# Invalid Scenario 3
# PUT a student that does not exist
def test_update_nonexistent_student():

    updated_student = {
        "id": 999,
        "name": "Unknown",
        "department": "Unknown",
        "semester": 1,
        "cgpa": 2.00
    }

    response = client.put(
        "/students/999",
        json=updated_student
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"


# Invalid Scenario 4
# PUT with mismatched student ID
def test_update_student_id_mismatch():

    updated_student = {
        "id": 5,
        "name": "Rahim Changed",
        "department": "CSE",
        "semester": 6,
        "cgpa": 3.80
    }

    response = client.put(
        "/students/1",
        json=updated_student
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student ID mismatch"


# DELETE - Delete a student
def test_delete_student():

    response = client.delete("/students/2")

    assert response.status_code == 200
    assert response.json()["message"] == "Student deleted successfully"


# Invalid Scenario 5
# DELETE a student that does not exist
def test_delete_nonexistent_student():

    response = client.delete("/students/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"