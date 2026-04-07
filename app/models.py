from sqlalchemy import Column, Float, Integer, String

from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    country = Column(String, nullable=False)
    salary = Column(Float, nullable=False)
