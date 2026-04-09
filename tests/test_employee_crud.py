def test_create_employee(client):
    response = client.post("/employees", json={
        "full_name": "John Doe",
        "job_title": "Software Engineer",
        "country": "India",
        "salary": 50000.0,
    })
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "John Doe"
    assert data["job_title"] == "Software Engineer"
    assert data["country"] == "India"
    assert data["salary"] == 50000.0
    assert "id" in data


def test_get_employee(client):
    create = client.post("/employees", json={
        "full_name": "Jane Smith",
        "job_title": "Designer",
        "country": "United States",
        "salary": 60000.0,
    })
    emp_id = create.json()["id"]

    response = client.get(f"/employees/{emp_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Jane Smith"
    assert data["id"] == emp_id


def test_get_employee_not_found(client):
    response = client.get("/employees/9999")
    assert response.status_code == 404


def test_list_employees(client):
    client.post("/employees", json={
        "full_name": "Alice",
        "job_title": "Manager",
        "country": "India",
        "salary": 70000.0,
    })
    response = client.get("/employees")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_update_employee(client):
    create = client.post("/employees", json={
        "full_name": "Bob",
        "job_title": "Tester",
        "country": "India",
        "salary": 40000.0,
    })
    emp_id = create.json()["id"]

    response = client.put(f"/employees/{emp_id}", json={
        "full_name": "Bob Updated",
        "job_title": "Senior Tester",
        "country": "India",
        "salary": 55000.0,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Bob Updated"
    assert data["salary"] == 55000.0


def test_update_employee_not_found(client):
    response = client.put("/employees/9999", json={
        "full_name": "Ghost",
        "job_title": "None",
        "country": "India",
        "salary": 0,
    })
    assert response.status_code == 404


def test_delete_employee(client):
    create = client.post("/employees", json={
        "full_name": "Charlie",
        "job_title": "Intern",
        "country": "United States",
        "salary": 30000.0,
    })
    emp_id = create.json()["id"]

    response = client.delete(f"/employees/{emp_id}")
    assert response.status_code == 200

    get_response = client.get(f"/employees/{emp_id}")
    assert get_response.status_code == 404


def test_delete_employee_not_found(client):
    response = client.delete("/employees/9999")
    assert response.status_code == 404


def test_create_employee_missing_fields(client):
    response = client.post("/employees", json={
        "full_name": "Incomplete",
    })
    assert response.status_code == 422


def test_create_employee_empty_name(client):
    response = client.post("/employees", json={
        "full_name": "",
        "job_title": "Developer",
        "country": "India",
        "salary": 50000.0,
    })
    assert response.status_code == 422


def test_create_employee_negative_salary(client):
    response = client.post("/employees", json={
        "full_name": "Negative Ned",
        "job_title": "Developer",
        "country": "India",
        "salary": -5000.0,
    })
    assert response.status_code == 422


def test_patch_employee_partial(client):
    create = client.post("/employees", json={
        "full_name": "Patchy",
        "job_title": "Tester",
        "country": "India",
        "salary": 40000.0,
    })
    emp_id = create.json()["id"]

    response = client.patch(f"/employees/{emp_id}", json={
        "salary": 50000.0,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["salary"] == 50000.0
    assert data["full_name"] == "Patchy"
    assert data["job_title"] == "Tester"
    assert data["country"] == "India"


def test_patch_employee_not_found(client):
    response = client.patch("/employees/9999", json={"salary": 50000.0})
    assert response.status_code == 404


def test_list_employees_empty(client):
    response = client.get("/employees")
    assert response.status_code == 200
    assert response.json() == []
