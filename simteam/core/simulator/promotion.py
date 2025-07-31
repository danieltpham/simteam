from datetime import datetime
from typing import Optional
import random

from simteam.core.enums import Role
from simteam.core.models.employee import Employee
from simteam.core.utils import weighted_sample


class PromotionLogic:
    """
    Handles promotion logic and candidate selection.

    - Promotes eligible employees based on hierarchy
    - Honors quota (only promotes if there's vacancy)
    - Uses weighted sampling (e.g. tenure-based)
    - Reassigns a valid manager after promotion
    """

    def get_promotable_candidates(self, from_role: Role) -> list[Employee]:
        """
        Return active employees in the specified `from_role` who are eligible for promotion.
        """
        return [
            e for e in self.employees.values()
            if e.state.active
            and e.state.role == from_role
            and self.can_be_promoted(e)
        ]

    def can_be_promoted(self, emp: Employee) -> bool:
        """
        Hook to define additional promotion eligibility rules.

        Returns:
            bool: True if eligible
        """
        return True  # Extendable (e.g. tenure, skill, review score)

    def promote_random(self, from_role: Role, date: datetime) -> Optional[str]:
        """
        Promote a randomly selected eligible employee from `from_role` to the next role.

        Returns:
            Optional[str]: Promoted employee ID, or None if not promoted.
        """
        to_role = self.config.promotion_order.get(from_role)
        if not to_role:
            return None

        # === 1. Check vacancy (quota not exceeded)
        current_count = sum(
            1 for e in self.employees.values()
            if e.state.active and e.state.role == to_role
        )
        if current_count >= self.config.role_quotas[to_role]:
            return None

        # === 2. Find candidates
        candidates = self.get_promotable_candidates(from_role)
        if not candidates:
            return None

        # === 3. Weighted sampling by tenure
        weights = [(date - e.state.hire_date).days + 1 for e in candidates]
        selected = weighted_sample(candidates, weights)

        # === 4. Promote
        selected.promote(to_role, date)
        self.event_log.append(selected.state.history[-1])

        # === 5. Reassign manager (if needed)
        new_mgr_id = self.find_valid_manager(selected.state.emp_id, to_role)
        if new_mgr_id:
            self.change_manager(selected.state.emp_id, new_mgr_id, date)
            self.event_log.append(selected.state.history[-1])

        return selected.state.emp_id

    def find_valid_manager(self, emp_id: str, role: Role) -> Optional[str]:
        """
        Find a valid, active manager one level above `role`.
        TEMP allowed if no real manager available.
        """
        allowed_roles = self.config.allowed_manager_mapping.get(role, set())

        for e in self.employees.values():
            if (
                e.state.active
                and e.state.emp_id != emp_id
                and e.state.role in allowed_roles
            ):
                return e.state.emp_id

        for tid, temp in self.temp_employees.items():
            if temp.state.role in allowed_roles:
                return tid

        return None
