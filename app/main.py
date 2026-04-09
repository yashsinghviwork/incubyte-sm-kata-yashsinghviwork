from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import employees, metrics, salary


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Salary Management API",
    description="Employee CRUD, salary calculation with country-based tax deductions, and salary metrics.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(employees.router)
app.include_router(salary.router)
app.include_router(metrics.router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
