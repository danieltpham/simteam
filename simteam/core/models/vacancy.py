from datetime import datetime
from typing import List, Optional

from simteam.core.enums import Role
from simteam.core.models.base import VacancyRecord


class Vacancy:
    """
    Represents a role vacancy in the organisation.

    Stores metadata about the vacant position and associated team structure.
    """

    def __init__(
        self,
        role: Role,
        manager_id: Optional[str],
        department: Optional[str],
        team: Optional[str],
        report_ids: List[str],
        deadline: datetime,
    ):
        """
        Initialise a new vacancy record.

        Args:
            role (Role): The role that is vacant.
            manager_id (Optional[str]): Manager to whom the new hire would report.
            department (Optional[str]): Department of the vacancy.
            team (Optional[str]): Team name under the vacancy (if any).
            report_ids (List[str]): IDs of direct reports affected by this vacancy.
            deadline (datetime): Date by which the vacancy must be filled.
        """
        self.record = VacancyRecord(
            role=role,
            manager_id=manager_id,
            department=department,
            team=team,
            report_ids=report_ids,
            deadline=deadline,
        )

    @property
    def is_expired(self) -> bool:
        """
        Returns:
            bool: True if the vacancy deadline has passed, False otherwise.
        """
        from datetime import datetime
        return datetime.now() > self.record.deadline
