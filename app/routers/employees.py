from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Employee
from app.schemas import EmployeeCreate, EmployeePatch, EmployeeResponse

router = APIRouter(prefix="/employees", tags=["employees"])


def _get_employee_or_404(employee_id: int, db: Session) -> Employee:
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.post("", response_model=EmployeeResponse, status_code=201)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@router.get("", response_model=list[EmployeeResponse])
def list_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    return _get_employee_or_404(employee_id, db)


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int, employee: EmployeeCreate, db: Session = Depends(get_db)
):
    db_employee = _get_employee_or_404(employee_id, db)
    for key, value in employee.model_dump().items():
        setattr(db_employee, key, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@router.patch("/{employee_id}", response_model=EmployeeResponse)
def patch_employee(
    employee_id: int, updates: EmployeePatch, db: Session = Depends(get_db)
):
    db_employee = _get_employee_or_404(employee_id, db)
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_employee, key, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = _get_employee_or_404(employee_id, db)
    db.delete(employee)
    db.commit()
    return {"detail": "Employee deleted"}
