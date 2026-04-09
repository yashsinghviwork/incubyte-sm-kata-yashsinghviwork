from fastapi import APIRouter, Depends, Query
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
    "/employees/{employee_id}/salary",
    response_model=SalaryResponse,
    summary="Calculate net salary with deductions",
    description="Calculates deductions and net salary for an employee. "
    "Pass gross_salary to override the stored salary, otherwise the employee's salary on record is used. "
    "Deduction rules: India 10% TDS, United States 12% TDS, all others no deductions.",
)
def calculate_salary(
    employee_id: int,
    gross_salary: float | None = Query(None, description="Override gross salary for calculation"),
    db: Session = Depends(get_db),
):
    employee = _get_employee_or_404(employee_id, db)

    gross = gross_salary if gross_salary is not None else employee.salary
    rules = DEDUCTION_RULES.get(employee.country, {})
    deductions = {name: round(gross * rate, 2) for name, rate in rules.items()}
    net = gross - sum(deductions.values())

    return SalaryResponse(gross_salary=gross, deductions=deductions, net_salary=net)
