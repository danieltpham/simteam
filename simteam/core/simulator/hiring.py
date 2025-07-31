from datetime import datetime
import random
from typing import Optional

from simteam.core.enums import Role
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
        if len(self.active_employees) >= self.config.max_employees:
            return None

        # Must not exceed role quota
        current_count = sum(
            1 for e in self.active_employees
            if e.state.active and e.state.role == role
        )
        if current_count >= self.config.role_quotas[role]:
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
        new_emp = Employee.create(
            emp_id=emp_id,
            role=role,
            hire_date=date,
            manager_id=manager_id,
            department=department,
            team=team
        )
        self.employees[emp_id] = new_emp
        self.event_log.append(new_emp.state.history[-1])
        
        # Create subordinate vacancies if this is a managerial role
        
        if role not in [Role.SENIOR_ANALYST, Role.ANALYST]:
            # Define what the subordinate role should be
            subordinate_role = {
                Role.CEO: Role.VP,
                Role.VP: Role.DIRECTOR,
                Role.DIRECTOR: Role.MANAGER,
                Role.MANAGER: random.choice([Role.SENIOR_ANALYST, Role.ANALYST]),
            }.get(role)
            
            if subordinate_role:
                # Count how many already exist in this department/team
                current = sum(
                    1 for e in self.active_employees
                    if e.state.active
                    and e.state.role == subordinate_role
                    and e.state.manager_id == emp_id
                )
                quota = self.config.role_quotas[subordinate_role]
                n_vacancies = max(0, quota - current)
                
                for _ in range(n_vacancies):
                    self.create_vacancy(
                        role=subordinate_role,
                        manager_id=emp_id,
                        department=new_emp.state.department,
                        team=new_emp.state.team,
                        report_ids=[],
                        date=date,
                    )
        
        return emp_id
