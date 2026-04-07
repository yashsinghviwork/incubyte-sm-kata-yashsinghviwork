from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    full_name: str
    job_title: str
    country: str
    salary: float


class EmployeeResponse(BaseModel):
    id: int
    full_name: str
    job_title: str
    country: str
    salary: float

    model_config = {"from_attributes": True}


class SalaryResponse(BaseModel):
    gross_salary: float
    deductions: dict[str, float]
    net_salary: float


class SalaryMetricsResponse(BaseModel):
    min: float
    max: float
    average: float
