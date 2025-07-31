from datetime import datetime

from simteam.core.models.employee import Employee
from simteam.core.enums import Role


class ManagerChangeLogic:
    """
    Handles logic for changing reporting lines (manager reassignments).

    Enforces:
    - Manager must exist and be active
    - Manager must have a higher role
    - No circular reporting
    """

    def change_manager(self, emp_id: str, new_mgr_id: str, date: datetime) -> bool:
        """
        Reassign an employee to a new manager, if valid.

        Returns:
            bool: True if reassignment succeeded, False otherwise.
        """
        emp = self.employees.get(emp_id)
        new_mgr = self.employees.get(new_mgr_id) or self.temp_employees.get(new_mgr_id)

        if not emp or not new_mgr:
            return False

        if not emp.state.active or not new_mgr.state.active:
            return False

        if not self.is_valid_manager_assignment(emp.state.role, new_mgr.state.role):
            return False

        if self.is_circular(emp_id, new_mgr_id):
            return False

        emp.change_manager(new_mgr_id, date)
        self.event_log.append(emp.state.history[-1])
        return True
    
    def is_valid_manager_assignment(self, emp_role: Role, mgr_role: Role) -> bool:
        """
        Check if manager's role is a valid direct supervisor for the employee's role.
        """
        allowed_roles = self.config.allowed_manager_mapping.get(emp_role, set())
        return mgr_role in allowed_roles


    def is_higher_role(self, manager_role: Role, emp_role: Role, manager_id: str = "") -> bool:
        """
        Ensure manager is more senior than employee.

        TEMP managers are always allowed to be assigned, even if they have the same or lower role.
        """
        if manager_id.startswith("TEMP"):
            return True

        return Role.get_level(manager_role) < Role.get_level(emp_role)

    def is_circular(self, emp_id: str, new_mgr_id: str) -> bool:
        """
        Check for circular reporting by walking up the new manager's chain.

        Returns:
            bool: True if the employee is in their own manager chain.
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
