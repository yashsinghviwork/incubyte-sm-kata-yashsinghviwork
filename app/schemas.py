from pydantic import BaseModel, field_validator


class EmployeeCreate(BaseModel):
    full_name: str
    job_title: str
    country: str
    salary: float

    @field_validator("full_name", "job_title", "country")
    @classmethod
    def must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("must not be empty")
        return v

    @field_validator("salary")
    @classmethod
    def salary_must_be_non_negative(cls, v: float) -> float:
        if v < 0:
            raise ValueError("must not be negative")
        return v


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
