from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from simteam.core.enums import Role
from simteam.core.models.base import VacancyRecord


class Vacancy(BaseModel):
    """
    Wraps a VacancyRecord and provides convenience methods.
    """
    record: VacancyRecord = Field(..., description="Details of the open vacancy")

    @classmethod
    def create(
        cls,
        role: Role,
        manager_id: Optional[str],
        department: Optional[str],
        team: Optional[str],
        report_ids: List[str],
        deadline: datetime,
    ) -> "Vacancy":
        """
        Factory method to create a new vacancy with required fields.
        """
        record = VacancyRecord(
            role=role,
            manager_id=manager_id,
            department=department,
            team=team,
            report_ids=report_ids,
            deadline=deadline,
        )
        return cls(record=record)

    @property
    def is_expired(self) -> bool:
        """
        Returns:
            bool: True if the vacancy deadline has passed, False otherwise.
        """
        return datetime.now() > self.record.deadline