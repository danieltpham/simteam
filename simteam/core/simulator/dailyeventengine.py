from collections import defaultdict
from datetime import datetime
import random
from simteam.core.enums import MAX_EVENTS_PER_DAY, MIN_EMPLOYEES_FOR_LEAVING, EventType
from simteam.core.utils import poisson_event_count


class DailyEventEngine:
    """
    Controls the simulation of daily HR events.

    Responsibilities:
    - Decide how many events occur per day
    - Choose which types (EMPLOYED, PROMOTED, LEFT, etc.)
    - Enforce daily and weekly constraints
    """

    EVENT_TYPE_WEIGHTS = {
        EventType.EMPLOYED: 4,
        EventType.PROMOTED: 2,
        EventType.LEFT: 1,
        EventType.CHANGE: 1,
    }

    EVENT_TYPE_CAPS = {
        EventType.EMPLOYED: 3,
        EventType.PROMOTED: 3,
        EventType.LEFT: 2,
        EventType.CHANGE: 2,
    }

    MIN_EVENTS_PER_WEEK = 1

    def __init__(self):
        self.week_counter = 0
        self.weekly_event_tracker = defaultdict(int)

    def generate_daily_events(self, date: datetime) -> None:
        """
        Generate and execute events for a single day.

        Steps:
        1. Sample number of events (Poisson)
        2. Sample event types (capped)
        3. Call corresponding simulator logic
        4. Track weekly totals
        """
        
        
        is_monday = date.weekday() == 0
        if is_monday:
            self.week_counter += 1
            self.weekly_event_tracker.clear()

        events_today = defaultdict(int)
        
        max_daily_events = poisson_event_count()

        # === 1. Fill vacancies first (count as events)
        if self.emp_counter <= MIN_EMPLOYEES_FOR_LEAVING:
            max_fill = int(max_daily_events)
        else:
            max_fill = int(max_daily_events/2)
        num_vacancy_fill_events = self.resolve_vacancies(date, max_fill=max_fill)

        # === 2. Sample how many new events to add
        remaining_budget =  max(max_daily_events-num_vacancy_fill_events, 0)

        for _ in range(remaining_budget):
            event_type = self.sample_event_type(events_today)
            if not event_type:
                break

            self.execute_event(event_type, date)
            events_today[event_type] += 1
            self.weekly_event_tracker[event_type] += 1

        # === 3. Fallback: force 1 guaranteed event on new week
        if is_monday and sum(self.weekly_event_tracker.values()) == 0:
            self.force_fallback_event(date)

    def sample_event_type(self, current_day_counts: dict) -> EventType | None:
        """
        Choose an event type based on weights, respecting per-day caps.
        """
        valid_types = []
        weights = []

        for etype, weight in self.EVENT_TYPE_WEIGHTS.items():
            if current_day_counts[etype] < self.EVENT_TYPE_CAPS[etype]:
                valid_types.append(etype)
                weights.append(weight)

        if not valid_types:
            return None

        return random.choices(valid_types, weights=weights, k=1)[0]

    def execute_event(self, event_type: EventType, date: datetime):
        """
        Dispatch actual logic per event type.
        """
        if event_type == EventType.EMPLOYED:
            self.simulate_hiring(date)
        elif event_type == EventType.PROMOTED:
            self.simulate_promotion(date)
        elif event_type == EventType.LEFT:
            self.simulate_leaving(date)
        elif event_type == EventType.CHANGE:
            self.simulate_manager_change(date)

    def force_fallback_event(self, date: datetime):
        """
        Force at least one event this week if none occurred.
        Defaults to a EMPLOYED attempt.
        """
        self.simulate_hiring(date)
