from datetime import datetime
from typing import Dict, List

from simteam.core.models.employee import Employee
from simteam.core.models.vacancy import Vacancy
from simteam.core.models.base import EventLog


class BaseOrgSimulator:
    """
    Base simulator class holding core state.

    This is extended by logic-specific mixins (e.g. HiringLogic, VacancyLogic).
    """

    def __init__(self, start_date: datetime):
        """
        Initialise the shared simulation environment.

        Args:
            start_date (datetime): The first day of simulation.
        """
        self.start_date = start_date
        self.today = start_date
        self.emp_counter = 0

        # Global registries
        self.employees: Dict[str, Employee] = {}
        self.vacancies: List[Vacancy] = []
        self.event_log: List[EventLog] = []
        
    @property
    def active_employees(self) -> list[Employee]:
        return [e for e in self.employees.values() if e.state.active]

    @property
    def employee_count(self) -> int:
        return len(self.active_employees)

