from datetime import datetime, timedelta
import random

from simteam.core.config import SimulationConfig, get_default_config
from simteam.core.enums import Role
from simteam.core.simulator.base import BaseOrgSimulator
from simteam.core.simulator.dailyeventengine import DailyEventEngine
from simteam.core.simulator.hiring import HiringLogic
from simteam.core.simulator.leaving import LeavingLogic
from simteam.core.simulator.managerchange import ManagerChangeLogic
from simteam.core.simulator.promotion import PromotionLogic
from simteam.core.simulator.vacancy import VacancyLogic


class OrgSimulator(
    BaseOrgSimulator,
    HiringLogic,
    PromotionLogic,
    ManagerChangeLogic,
    VacancyLogic,
    LeavingLogic,
    DailyEventEngine,
):
    """
    Full organisational simulator, composed of all HR dynamics.

    Handles:
    - Daily event simulation via Poisson + weighted logic
    - Promotion, hiring, leaving, reassignments
    - Vacancy backfilling with deadlines
    """

    def __init__(self, start_date: datetime, config: SimulationConfig = get_default_config()):
        BaseOrgSimulator.__init__(self, start_date, config)
        DailyEventEngine.__init__(self)
        self.init_org(start_date)
        
    def init_org(self, date: datetime):
        """
        Create initial CEO and VPs so that org structure is bootstrapped.
        """
        ceo_id = self.hire(
            role=Role.CEO,
            manager_id=None,
            department=None,
            team=None,
            date=date,
        )
        if not ceo_id:
            return

    def simulate_one_day(self):
        """
        Run simulation logic for a single day:
        - Fill overdue vacancies
        - Generate and execute daily events
        - Advance date
        """
        self.generate_daily_events(self.today)
        self.today += timedelta(days=1)

    def simulate_for_days(self, n: int):
        """
        Run simulation for a given number of days.
        """
        for _ in range(n):
            self.simulate_one_day()

    # ==== Event Execution Stubs for DailyEventEngine ====

    def simulate_hiring(self, date: datetime):
        """
        Simulate a random hire event (default to Analyst under any Manager).
        """
        managers = [
            e for e in self.employees.values()
            if e.state.active and e.state.role == Role.MANAGER
        ]
        if not managers:
            return

        mgr = random.choice(managers)
        self.hire(
            role=Role.ANALYST,
            manager_id=mgr.state.emp_id,
            department=mgr.state.department,
            team=mgr.state.team,
            date=date,
        )

    def simulate_promotion(self, date: datetime):
        """
        Try to promote from any promotable role.
        Order: Analyst → SA → Manager → Director → VP
        """
        for from_role in [
            Role.ANALYST,
            Role.SENIOR_ANALYST,
            Role.MANAGER,
            Role.DIRECTOR,
            Role.VP,
        ]:
            if self.promote_random(from_role=from_role, date=date):
                break  # Only one promotion per call

    def simulate_leaving(self, date: datetime):
        """
        Randomly select someone to leave, excluding CEO and VPs.
        """
        leavers = [
            e for e in self.employees.values()
            if e.state.active and e.state.role not in {Role.CEO, Role.VP}
        ]
        if not leavers:
            return
        emp = random.choice(leavers)
        self.mark_left(emp.state.emp_id, date)

    def simulate_manager_change(self, date: datetime):
        """
        Randomly reassign a manager to a different valid higher-level manager.
        """
        candidates = [
            e for e in self.employees.values()
            if e.state.active and e.state.manager_id
        ]
        if not candidates:
            return

        emp = random.choice(candidates)

        # Find new possible manager
        potential_mgrs = [
            m for m in self.employees.values()
            if m.state.active
            and m.state.emp_id != emp.state.manager_id
            and self.is_higher_role(m.state.role, emp.state.role)
            and not self.is_circular(emp.state.emp_id, m.state.emp_id)
        ]

        if not potential_mgrs:
            return

        new_mgr = random.choice(potential_mgrs)
        self.change_manager(emp.state.emp_id, new_mgr.state.emp_id, date)
