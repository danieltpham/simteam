from datetime import datetime
import json
from typing import Dict, List

from simteam.core.models.employee import Employee
from simteam.core.models.vacancy import Vacancy
from simteam.core.models.base import EmployeeState, EventLog, VacancyRecord


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
        self.temp_employees: Dict[str, Employee] = {}  # TEMP placeholders
        self.vacancies: List[Vacancy] = []
        self.event_log: List[EventLog] = []
        
    @property
    def active_employees(self) -> list[Employee]:
        return [e for e in self.employees.values() if e.state.active]

    @property
    def employee_count(self) -> int:
        return len(self.active_employees)
    
    def employee_count_by_role(self) -> dict:
        """
        Returns a dictionary mapping each Role to the number of active employees in that role.
        """
        from collections import Counter
        counts = Counter(e.state.role for e in self.active_employees)
        return dict(counts)
    
    def get_active_employees_by_role(self, role) -> list:
        """
        Returns a dictionary mapping each Role to a list of active employees in that role.
        """
        return [e for e in self.active_employees if e.state.role==role]
        
    def generate_emp_id(self, prefix="EMP") -> str:
        """
        Generate the next unique employee ID (e.g. EMP001).
        """
        self.emp_counter += 1
        return f"{prefix}{self.emp_counter:03d}"

    def export_to_json(self) -> dict:
        """
        Export simulation state as a dictionary (JSON-serialisable).
        """
        return {
            "employees": [e.state.model_dump() for e in self.employees.values()],
            "temp_employees": [e.state.model_dump() for e in self.temp_employees.values()],
            "vacancies": [v.record.model_dump() for v in self.vacancies],
            "event_log": [e.model_dump() for e in self.event_log],
            "start_date": self.start_date.isoformat(),
            "current_date": self.today.isoformat(),
        }

    def save_to_json(self, path: str):
        """
        Save current simulation state to JSON file.

        Args:
            path (str): File path to write to.
        """
        with open(path, "w") as f:
            json.dump(self.export_to_json(), f, indent=2, default=str)

    @classmethod
    def load_from_json(cls, path: str) -> "BaseOrgSimulator":
        """
        Load simulation state from JSON file.

        Args:
            path (str): Path to saved simulation state.

        Returns:
            BaseOrgSimulator: Restored simulator instance.
        """
        with open(path, "r") as f:
            data = json.load(f)

        start_date = datetime.fromisoformat(data["start_date"])
        sim = cls(start_date=start_date)
        sim.today = datetime.fromisoformat(data["current_date"])

        # Restore regular employees
        for emp_data in data.get("employees", []):
            emp = Employee(state=EmployeeState(**emp_data))
            sim.employees[emp.state.emp_id] = emp
            sim.emp_counter = max(sim.emp_counter, int(emp.state.emp_id.strip("EMP")))

        # Restore TEMP employees
        for temp_data in data.get("temp_employees", []):
            temp = Employee(state=EmployeeState(**temp_data))
            sim.temp_employees[temp.state.emp_id] = temp
            sim.emp_counter = max(sim.emp_counter, int(temp.state.emp_id.strip("TEMP")))

        # Restore vacancies
        for vdata in data.get("vacancies", []):
            sim.vacancies.append(Vacancy(record=VacancyRecord(**vdata)))

        # Restore event log
        for edata in data.get("event_log", []):
            sim.event_log.append(EventLog(**edata))

        return sim