def _seed_employees(client):
    employees = [
        {"full_name": "A", "job_title": "Developer", "country": "India", "salary": 50000.0},
        {"full_name": "B", "job_title": "Developer", "country": "India", "salary": 70000.0},
        {"full_name": "C", "job_title": "Manager", "country": "India", "salary": 90000.0},
        {"full_name": "D", "job_title": "Developer", "country": "United States", "salary": 80000.0},
        {"full_name": "E", "job_title": "Manager", "country": "United States", "salary": 100000.0},
    ]
    for emp in employees:
        client.post("/employees", json=emp)


def test_salary_metrics_by_country(client):
    _seed_employees(client)

    response = client.get("/metrics/salary", params={"country": "India"})
    assert response.status_code == 200
    data = response.json()
    assert data["min"] == 50000.0
    assert data["max"] == 90000.0
    assert data["average"] == 70000.0


def test_salary_metrics_by_job_title(client):
    _seed_employees(client)

    response = client.get("/metrics/salary", params={"job_title": "Developer"})
    assert response.status_code == 200
    data = response.json()
    # Average of 50000, 70000, 80000 = 66666.67
    assert round(data["average"], 2) == 66666.67


def test_salary_metrics_country_no_employees(client):
    response = client.get("/metrics/salary", params={"country": "Antarctica"})
    assert response.status_code == 404


def test_salary_metrics_job_title_no_employees(client):
    response = client.get("/metrics/salary", params={"job_title": "Astronaut"})
    assert response.status_code == 404


def test_salary_metrics_no_filter(client):
    response = client.get("/metrics/salary")
    assert response.status_code == 422


def test_salary_metrics_by_country_and_job_title(client):
    _seed_employees(client)

    response = client.get("/metrics/salary", params={
        "country": "India",
        "job_title": "Developer",
    })
    assert response.status_code == 200
    data = response.json()
    # Only Indian Developers: 50000, 70000
    assert data["min"] == 50000.0
    assert data["max"] == 70000.0
    assert data["average"] == 60000.0


def test_salary_metrics_single_employee(client):
    client.post("/employees", json={
        "full_name": "Solo",
        "job_title": "CTO",
        "country": "Germany",
        "salary": 120000.0,
    })

    response = client.get("/metrics/salary", params={"country": "Germany"})
    assert response.status_code == 200
    data = response.json()
    assert data["min"] == 120000.0
    assert data["max"] == 120000.0
    assert data["average"] == 120000.0
