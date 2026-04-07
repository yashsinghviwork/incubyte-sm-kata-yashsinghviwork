from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers.employees import _get_employee_or_404
from app.schemas import SalaryResponse

router = APIRouter(tags=["salary"])

DEDUCTION_RULES = {
    "India": {"TDS": 0.10},
    "United States": {"TDS": 0.12},
}


@router.get(
    "/employees/{employee_id}/salary", response_model=SalaryResponse
)
def calculate_salary(employee_id: int, db: Session = Depends(get_db)):
    employee = _get_employee_or_404(employee_id, db)

    gross = employee.salary
    rules = DEDUCTION_RULES.get(employee.country, {})
    deductions = {name: round(gross * rate, 2) for name, rate in rules.items()}
    net = gross - sum(deductions.values())

    return SalaryResponse(gross_salary=gross, deductions=deductions, net_salary=net)
