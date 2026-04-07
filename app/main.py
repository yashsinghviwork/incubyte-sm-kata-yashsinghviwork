from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Employee
from app.schemas import (
    EmployeeCreate,
    EmployeeResponse,
    SalaryMetricsResponse,
    SalaryResponse,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()


# --- Employee CRUD ---


@app.post("/employees", response_model=EmployeeResponse, status_code=201)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@app.get("/employees", response_model=list[EmployeeResponse])
def list_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()


@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int, employee: EmployeeCreate, db: Session = Depends(get_db)
):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    for key, value in employee.model_dump().items():
        setattr(db_employee, key, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    return {"detail": "Employee deleted"}


# --- Salary Calculation ---

DEDUCTION_RULES = {
    "India": {"TDS": 0.10},
    "United States": {"TDS": 0.12},
}


@app.get("/employees/{employee_id}/salary", response_model=SalaryResponse)
def calculate_salary(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    gross = employee.salary
    rules = DEDUCTION_RULES.get(employee.country, {})
    deductions = {name: round(gross * rate, 2) for name, rate in rules.items()}
    net = gross - sum(deductions.values())

    return SalaryResponse(gross_salary=gross, deductions=deductions, net_salary=net)


# --- Salary Metrics ---


@app.get("/metrics/salary", response_model=SalaryMetricsResponse)
def salary_metrics(
    country: str | None = Query(None),
    job_title: str | None = Query(None),
    db: Session = Depends(get_db),
):
    if not country and not job_title:
        raise HTTPException(status_code=422, detail="Provide country or job_title")

    query = db.query(Employee)
    if country:
        query = query.filter(Employee.country == country)
    if job_title:
        query = query.filter(Employee.job_title == job_title)

    result = query.with_entities(
        func.min(Employee.salary),
        func.max(Employee.salary),
        func.avg(Employee.salary),
    ).first()

    if result[0] is None:
        raise HTTPException(status_code=404, detail="No employees found")

    return SalaryMetricsResponse(min=result[0], max=result[1], average=result[2])
