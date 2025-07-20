from datetime import datetime
from typing import Optional
import random

from simteam.core.enums import Role
from simteam.core.models.employee import Employee
from simteam.core.utils import weighted_sample


PROMOTION_ORDER = {
    Role.ANALYST: Role.SENIOR_ANALYST,
    Role.SENIOR_ANALYST: Role.MANAGER,
    Role.MANAGER: Role.DIRECTOR,
    Role.DIRECTOR: Role.VP,
    Role.VP: Role.CEO,
}


class PromotionLogic:
    """
    Handles promotion logic and candidate selection.

    - Promotes eligible employees based on role hierarchy.
    - Supports weighted sampling (e.g. tenure-based).
    - Can record prior role metadata.
    """

    def get_promotable_candidates(self, from_role: Role) -> list[Employee]:
        """
        Return active employees eligible to be promoted from the given role.
        """
        return [
            e for e in self.employees.values()
            if e.state.active
            and e.state.role == from_role
            and self.can_be_promoted(e)
        ]

    def can_be_promoted(self, emp: Employee) -> bool:
        """
        Hook for promotion eligibility logic.

        Returns:
            bool: True if eligible.
        """
        return True  # Extendable later (e.g. tenure, performance)

    def promote_random(self, from_role: Role, date: datetime) -> Optional[str]:
        """
        Promote a randomly selected eligible employee from a given role.

        Weights are based on hire date (longer tenure = more likely).

        Returns:
            Optional[str]: Promoted employee ID or None.
        """
        to_role = PROMOTION_ORDER.get(from_role)
        if not to_role:
            return None

        candidates = self.get_promotable_candidates(from_role)
        if not candidates:
            return None

        # Weighted by tenure
        weights = [
            (date - e.state.hire_date).days + 1  # +1 to avoid zero weight
            for e in candidates
        ]
        selected = weighted_sample(candidates, weights)
        prior_role = selected.state.role

        selected.promote(to_role, date)
        self.event_log.append(selected.state.history[-1])

        return selected.state.emp_id
