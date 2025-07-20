from datetime import datetime
from typing import Optional

from simteam.core.enums import Role, ROLE_QUOTAS, MAX_EMPLOYEES
from simteam.core.utils import generate_emp_id
from simteam.core.models.employee import Employee
from simteam.core.models.base import EventLog


class HiringLogic:
    """
    Handles external hiring logic and enforces role quotas.
    """

    def hire(
        self,
        role: Role,
        manager_id: Optional[str],
        department: Optional[str],
        team: Optional[str],
        date: datetime,
    ) -> Optional[str]:
        """
        Hire a new employee if quota allows and assign appropriate structure.

        Rules:
        - Must not exceed total or role quota.
        - Manager must exist and be active.
        - CEO/VP roles do not receive department/team metadata.

        Returns:
            Optional[str]: Employee ID if hired, else None.
        """
        
        # Must not exceed total
        if len(self.employees) >= MAX_EMPLOYEES:
            return None

        # Must not exceed role quota
        current_count = sum(
            1 for e in self.employees.values()
            if e.state.active and e.state.role == role
        )
        if current_count >= ROLE_QUOTAS[role]:
            return None


        # Manager must exist and be active
        if manager_id:
            mgr = self.employees.get(manager_id)
            if not mgr or not mgr.state.active:
                return None

        # Only assign dept/team if below VP
        assign_structure = role in {
            Role.DIRECTOR,
            Role.MANAGER,
            Role.SENIOR_ANALYST,
            Role.ANALYST,
        }

        emp_id = self.generate_emp_id()
        new_emp = Employee(
            emp_id=emp_id,
            role=role,
            hire_date=date,
            manager_id=manager_id,
            department=department if assign_structure else None,
            team=team if assign_structure else None,
        )
        self.employees[emp_id] = new_emp
        self.event_log.append(new_emp.state.history[-1])
        return emp_id
