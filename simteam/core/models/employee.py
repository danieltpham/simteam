from datetime import datetime
from typing import Optional

from simteam.core.enums import Role, EventType
from simteam.core.models.base import EventLog, EmployeeState


class Employee:
    """
    Represents an employee in the organisation.

    Tracks their role, reporting structure, status (active/inactive),
    and a full history of employment-related events.
    """

    def __init__(
        self,
        emp_id: str,
        role: Role,
        hire_date: datetime,
        manager_id: Optional[str] = None,
        department: Optional[str] = None,
        team: Optional[str] = None,
    ):
        """
        Initialise a new employee instance.

        Args:
            emp_id (str): Unique employee identifier.
            role (Role): Initial role of the employee.
            hire_date (datetime): Date the employee was hired.
            manager_id (Optional[str]): ID of the manager (if any).
            department (Optional[str]): Department the employee belongs to.
            team (Optional[str]): Team name (if applicable).
        """
        self.state = EmployeeState(
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

    def promote(self, new_role: Role, date: datetime):
        """
        Promote the employee to a new role.

        Args:
            new_role (Role): The new role after promotion.
            date (datetime): The date the promotion occurs.
        """
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
        """
        Update the employee's manager.

        Args:
            new_manager_id (str): ID of the new manager.
            date (datetime): The date the change takes effect.
        """
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
        """
        Mark the employee as having left the organisation.

        Args:
            date (datetime): The date of departure.
        """
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
