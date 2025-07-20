class DailyEventEngine:
    """
    Controls the simulation of daily HR events.

    Responsibilities:
    - Decide how many events occur per day
    - Choose which types (hire, promote, leave, etc.)
    - Enforce daily and weekly constraints
    """

    EVENT_TYPE_WEIGHTS = {
        EventType.HIRE: 4,
        EventType.PROMOTE: 2,
        EventType.LEAVE: 1,
        EventType.CHANGE: 1,
    }

    EVENT_TYPE_CAPS = {
        EventType.HIRE: 3,
        EventType.PROMOTE: 3,
        EventType.LEAVE: 2,
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

        n_events = poisson_event_count()

        events_today = defaultdict(int)
        for _ in range(n_events):
            event_type = self.sample_event_type(events_today)
            if not event_type:
                continue

            self.execute_event(event_type, date)
            events_today[event_type] += 1
            self.weekly_event_tracker[event_type] += 1

        # If no events this week, force one fallback
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
        if event_type == EventType.HIRE:
            self.simulate_hiring(date)
        elif event_type == EventType.PROMOTE:
            self.simulate_promotion(date)
        elif event_type == EventType.LEAVE:
            self.simulate_leaving(date)
        elif event_type == EventType.CHANGE:
            self.simulate_manager_change(date)

    def force_fallback_event(self, date: datetime):
        """
        Force at least one event this week if none occurred.
        Defaults to a hire attempt.
        """
        self.simulate_hiring(date)
