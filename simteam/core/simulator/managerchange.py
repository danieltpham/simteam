from datetime import datetime

from simteam.core.models.employee import Employee
from simteam.core.enums import Role


class ManagerChangeLogic:
    """
    Handles logic for changing reporting lines (manager reassignments).

    Enforces:
    - Manager must exist and be active
    - New manager must have a higher role
    - No circular reporting (cannot assign manager to their own report chain)
    """

    def change_manager(self, emp_id: str, new_mgr_id: str, date: datetime):
        """
        Reassign an employee to a new manager, if valid.

        Args:
            emp_id (str): Employee to reassign.
            new_mgr_id (str): Target manager.
            date (datetime): Effective date.
        """
        emp = self.employees.get(emp_id)
        new_mgr = self.employees.get(new_mgr_id)

        if not emp or not new_mgr:
            return  # Employee or manager not found

        if not emp.state.active or not new_mgr.state.active:
            return  # Either not active

        if not self.is_higher_role(new_mgr.state.role, emp.state.role):
            return  # Manager must be higher in org

        if self.is_circular(emp_id, new_mgr_id):
            return  # Prevent indirect cycles

        emp.change_manager(new_mgr_id, date)
        self.event_log.append(emp.state.history[-1])

    def is_higher_role(self, manager_role: Role, emp_role: Role) -> bool:
        """
        Compare role hierarchy to ensure manager is senior to employee.
        """
        return Role.get_level(manager_role) < Role.get_level(emp_role)

    def is_circular(self, emp_id: str, new_mgr_id: str) -> bool:
        """
        Check for circular reporting: employee should not be reassigned
        to someone in their own report chain.
        """
        visited = set()
        current = new_mgr_id

        while current:
            if current == emp_id:
                return True
            current_emp = self.employees.get(current)
            if not current_emp or not current_emp.state.manager_id:
                break
            current = current_emp.state.manager_id
            if current in visited:
                break
            visited.add(current)

        return False
