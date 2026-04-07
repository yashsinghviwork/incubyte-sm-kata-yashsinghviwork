def test_salary_calculation_india(client):
    create = client.post("/employees", json={
        "full_name": "Raj Patel",
        "job_title": "Developer",
        "country": "India",
        "salary": 100000.0,
    })
    emp_id = create.json()["id"]

    response = client.get(f"/employees/{emp_id}/salary")
    assert response.status_code == 200
    data = response.json()
    assert data["gross_salary"] == 100000.0
    assert data["deductions"]["TDS"] == 10000.0
    assert data["net_salary"] == 90000.0


def test_salary_calculation_us(client):
    create = client.post("/employees", json={
        "full_name": "John Adams",
        "job_title": "Manager",
        "country": "United States",
        "salary": 100000.0,
    })
    emp_id = create.json()["id"]

    response = client.get(f"/employees/{emp_id}/salary")
    assert response.status_code == 200
    data = response.json()
    assert data["gross_salary"] == 100000.0
    assert data["deductions"]["TDS"] == 12000.0
    assert data["net_salary"] == 88000.0


def test_salary_calculation_other_country(client):
    create = client.post("/employees", json={
        "full_name": "Hans Muller",
        "job_title": "Analyst",
        "country": "Germany",
        "salary": 80000.0,
    })
    emp_id = create.json()["id"]

    response = client.get(f"/employees/{emp_id}/salary")
    assert response.status_code == 200
    data = response.json()
    assert data["deductions"] == {}
    assert data["net_salary"] == 80000.0


def test_salary_calculation_not_found(client):
    response = client.get("/employees/9999/salary")
    assert response.status_code == 404


def test_salary_calculation_zero_salary(client):
    create = client.post("/employees", json={
        "full_name": "Zero Sam",
        "job_title": "Volunteer",
        "country": "India",
        "salary": 0.0,
    })
    emp_id = create.json()["id"]

    response = client.get(f"/employees/{emp_id}/salary")
    assert response.status_code == 200
    data = response.json()
    assert data["gross_salary"] == 0.0
    assert data["deductions"]["TDS"] == 0.0
    assert data["net_salary"] == 0.0
