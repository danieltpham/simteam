import random
from datetime import datetime
from typing import List

from simteam.core.enums import Role
from simteam.core.models.vacancy import Vacancy
from simteam.core.utils import advance_date

# Moved to top-level constant for reuse and testability
PROMOTE_HIRE_WEIGHTS = {
    Role.CEO: (1, 9),               # Prefer external
    Role.VP: (2, 8),
    Role.DIRECTOR: (7, 3),          # Prefer promoting managers
    Role.MANAGER: (5, 5),           # Equal SA promote or hire
    Role.SENIOR_ANALYST: (5, 5),    # Equal Analyst promote or hire
    Role.ANALYST: (0, 1),           # Always hire
}

class VacancyLogic:
    """
    Handles creation, resolution, and tracking of role vacancies.

    - Vacancies are triggered by departures with direct reports.
    - Fill logic considers weighted chance of promotion vs hire.
    """

    def create_vacancy(
        self,
        role: Role,
        manager_id: str,
        department: str,
        team: str,
        report_ids: List[str],
        date: datetime,
    ) -> None:
        """
        Create a new vacancy and add it to the queue.
        """
        deadline = advance_date(date, self.config.vacancy_fill_deadline_days)
        vacancy = Vacancy.create(
            role=role,
            manager_id=manager_id,
            department=department,
            team=team,
            report_ids=report_ids,
            deadline=deadline,
        )
        self.vacancies.append(vacancy)

    def resolve_vacancies(self, date: datetime, max_fill: int = None) -> int:
        """
        Attempt to resolve open vacancies (by promotion or hiring), up to a maximum number.

        Args:
            date (datetime): Current simulation date.
            max_fill (int, optional): Maximum number of fills to perform today. If None, unlimited.

        Returns:
            int: Number of vacancies successfully filled.
        """
        still_open = []
        filled_count = 0

        for vacancy in self.vacancies:
            if self.is_vacancy_expired(vacancy, date):
                continue

            if max_fill is not None and filled_count >= max_fill:
                still_open.append(vacancy)
                continue

            filled = self.try_fill_vacancy(vacancy, date)
            if filled:
                filled_count += 1
            else:
                still_open.append(vacancy)

        self.vacancies = still_open
        return filled_count

    def try_fill_vacancy(self, vacancy: Vacancy, date: datetime) -> bool:
        """
        Attempt to fill a given vacancy via promotion or hiring,
        and reassigns reportees. Automatically cleans up TEMP placeholders.

        Args:
            vacancy (Vacancy): The vacant role object.
            date (datetime): Current simulation date.

        Returns:
            bool: True if vacancy successfully filled, False otherwise.
        """
        role = vacancy.record.role
        manager_id = vacancy.record.manager_id
        department = vacancy.record.department
        team = vacancy.record.team
        report_ids = vacancy.record.report_ids

        # Step 1: Choose method based on defined promotion/hiring weights
        strategy = PROMOTE_HIRE_WEIGHTS.get(role, (0, 1))  # default: always hire
        method = random.choices(["promote", "hire"], weights=strategy, k=1)[0]

        # Step 2: Attempt promotion or fallback to hire
        emp_id = None
        if method == "promote":
            from_role = self.get_promotion_source(role)
            emp_id = self.promote_random(from_role=from_role, date=date)

        if not emp_id:
            emp_id = self.hire(
                role=role,
                manager_id=manager_id,
                department=department,
                team=team,
                date=date,
            )

        if not emp_id:
            return False

        # Step 3: Reassign reportees to new employee
        for report_id in report_ids:
            self.change_manager(report_id, emp_id, date)

        return True

    def is_vacancy_expired(self, vacancy: Vacancy, date: datetime) -> bool:
        return date > vacancy.record.deadline

    def get_promotion_source(self, to_role: Role) -> Role:
        """
        Get the typical role that promotes into this target role.
        """
        for from_role, to in self.config.promotion_order.items():
            if to == to_role:
                return from_role
        return to_role  # fallback
