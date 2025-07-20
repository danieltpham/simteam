from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from simteam.core.enums import Role, EventType
from simteam.core.models.base import EventLog, EmployeeState


class Employee(BaseModel):
    """
    A wrapper around EmployeeState with helper methods for mutation.
    """
    state: EmployeeState = Field(..., description="Current state of the employee")

    @classmethod
    def create(
        cls,
        emp_id: str,
        role: Role,
        hire_date: datetime,
        manager_id: Optional[str] = None,
        department: Optional[str] = None,
        team: Optional[str] = None,
    ) -> "Employee":
        """
        Factory method to create a new employee with initial EMPLOYED event.
        """
        state = EmployeeState(
            emp_id=emp_id,
            role=role,
            manager_id=manager_id,
            department=department,
            team=team,
            hire_date=hire_date,
            active=True,
            history=[
                EventLog(
                    date=hire_date,
                    event_type=EventType.EMPLOYED,
                    employee_id=emp_id,
                    role=role,
                    manager_id=manager_id,
                    department=department,
                    team=team,
                )
            ],
        )
        return cls(state=state)

    def promote(self, new_role: Role, date: datetime):
        self.state.role = new_role
        self.state.history.append(
            EventLog(
                date=date,
                event_type=EventType.PROMOTED,
                employee_id=self.state.emp_id,
                role=new_role,
                manager_id=self.state.manager_id,
                department=self.state.department,
                team=self.state.team,
            )
        )

    def change_manager(self, new_manager_id: str, date: datetime):
        self.state.manager_id = new_manager_id
        self.state.history.append(
            EventLog(
                date=date,
                event_type=EventType.CHANGE,
                employee_id=self.state.emp_id,
                role=self.state.role,
                manager_id=new_manager_id,
                department=self.state.department,
                team=self.state.team,
            )
        )

    def leave(self, date: datetime):
        self.state.active = False
        self.state.history.append(
            EventLog(
                date=date,
                event_type=EventType.LEFT,
                employee_id=self.state.emp_id,
                role=self.state.role,
                manager_id=self.state.manager_id,
                department=self.state.department,
                team=self.state.team,
            )
        )
