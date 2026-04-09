from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Employee
from app.schemas import SalaryMetricsResponse

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get(
    "/salary",
    response_model=SalaryMetricsResponse,
    summary="Get salary statistics",
    description="Returns min, max, and average salary filtered by country, job title, or both. "
    "At least one filter is required.",
)
def salary_metrics(
    country: str | None = Query(None, description="Filter by country"),
    job_title: str | None = Query(None, description="Filter by job title"),
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
