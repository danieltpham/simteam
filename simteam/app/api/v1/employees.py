# app/api/v1/employees.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from simteam.app.db.session import get_db
from simteam.app.db.models import EmployeeORM
from simteam.core.models.base import EmployeeState

router = APIRouter()

@router.get("/employees", response_model=list[EmployeeState])
def list_employees(db: Session = Depends(get_db)):
    employees = db.query(EmployeeORM).all()
    return [EmployeeState(
        emp_id=e.emp_id,
        role=e.role,
        manager_id=e.manager_id,
        department=e.department,
        team=e.team,
        hire_date=e.hire_date,
        active=e.active,
        # history=[],  # Expand this if needed
    ) for e in employees]
