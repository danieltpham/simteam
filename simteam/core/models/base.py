from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from ..enums import Role, EventType


class EventLog(BaseModel):
    """
    The atomic event type used in employee history and export
    """
    date: datetime
    event_type: EventType
    employee_id: str
    role: Role
    manager_id: Optional[str] = None
    department: Optional[str] = None
    team: Optional[str] = None


class EmployeeState(BaseModel):
    """
    A persistent state container used for graph-building and lookup
    """
    emp_id: str
    role: Role
    manager_id: Optional[str]
    department: Optional[str]
    team: Optional[str]
    hire_date: datetime
    active: bool = True
    history: List[EventLog] = Field(default_factory=list)


class VacancyRecord(BaseModel):
    """
    A temporary open position with associated reports and a resolution deadline
    """
    role: Role
    manager_id: Optional[str]
    department: Optional[str]
    team: Optional[str]
    report_ids: List[str]
    deadline: datetime
