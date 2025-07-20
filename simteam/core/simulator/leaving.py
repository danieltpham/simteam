from datetime import datetime

from simteam.core.enums import EventType


class LeavingLogic:
    """
    Handles logic for employee exits and associated updates.

    - Marks the employee as inactive
    - Logs the LEAVE event
    - Creates a vacancy if they had direct reports
    """

    def mark_left(self, emp_id: str, date: datetime):
        emp = self.employees.get(emp_id)
        if not emp or not emp.state.active:
            return

        emp.mark_left(date)
        self.event_log.append(emp.state.history[-1])

        report_ids = [
            e.state.emp_id for e in self.employees.values()
            if e.state.active and e.state.manager_id == emp_id
        ]

        if report_ids:
            self.create_vacancy(
                role=emp.state.role,
                manager_id=emp.state.manager_id,
                department=emp.state.department,
                team=emp.state.team,
                report_ids=report_ids,
                date=date,
            )
