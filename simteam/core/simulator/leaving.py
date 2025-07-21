from datetime import datetime

from simteam.core.enums import EventType, Role
from simteam.core.models.employee import Employee


class LeavingLogic:
    """
    Handles logic for employee exits and associated updates.

    - Marks the employee as inactive
    - Logs the LEAVE event
    - Creates a vacancy
    """

    def mark_left(self, emp_id: str, date: datetime):
        emp = self.employees.get(emp_id)
        if not emp or not emp.state.active:
            return

        emp.leave(date)
        self.event_log.append(emp.state.history[-1])

        report_ids = [
            e.state.emp_id for e in self.employees.values()
            if e.state.active and e.state.manager_id == emp_id
        ]

        # STEP 1 — Create TEMP placeholder
        if report_ids and emp.state.role in {Role.MANAGER, Role.DIRECTOR, Role.VP}:
            placeholder_id = self.generate_emp_id(prefix="TEMP")
            self.emp_counter += 1

            temp_emp = Employee.create(
                emp_id=placeholder_id,
                role=emp.state.role,
                hire_date=date,
                manager_id=emp.state.manager_id,
                department=emp.state.department,
                team=emp.state.team,
            )
            temp_emp.state.active = False  # this is not a real person
            self.temp_employees[placeholder_id] = temp_emp  # Track in temp_employees

            # Reassign direct reports to the placeholder
            for report_id in report_ids:
                self.employees[report_id].change_manager(placeholder_id, date)
                self.event_log.append(self.employees[report_id].state.history[-1])

            temp_manager_id = placeholder_id
        else:
            temp_manager_id = emp.state.manager_id

        # STEP 2 — Create real vacancy as usual
        self.create_vacancy(
            role=emp.state.role,
            manager_id=temp_manager_id,
            department=emp.state.department,
            team=emp.state.team,
            report_ids=report_ids,
            date=date,
        )
