import random
from faker import Faker
from typing import List
from datetime import datetime, timedelta
from scipy.stats import poisson

from simteam.core.enums import MAX_EVENTS_PER_DAY, MAX_EVENTS_PER_TYPE


def generate_emp_id(counter: int) -> str:
    """
    Generate a unique employee ID from a global counter.

    Args:
        counter (int): Current integer counter.

    Returns:
        str: Formatted employee ID (e.g. 'E0001').
    """
    return f"E{counter:04d}"


def poisson_event_count(mu: float = 1.5, max_events: int = MAX_EVENTS_PER_DAY) -> int:
    """
    Sample the number of events for the day using a Poisson distribution.

    Args:
        mu (float): The lambda parameter (mean rate of events).
        max_events (int): Maximum allowed events.

    Returns:
        int: Truncated number of events for the day.
    """
    return min(poisson.rvs(mu=mu), max_events)


def sample_limited(
    population: List,
    k: int,
    max_per_item: int = MAX_EVENTS_PER_TYPE
) -> List:
    """
    Sample up to `k` unique items from a list, capped by `max_per_item`.

    Args:
        population (List): List of items to sample from.
        k (int): Number of samples to return.
        max_per_item (int): Cap on same-item selection frequency.

    Returns:
        List: Sampled items.
    """
    if not population:
        return []
    if len(population) <= k:
        return population
    return random.sample(population, min(k, max_per_item))


def random_name() -> str:
    """
    Generate a random human-like name for visualisation/demo purposes.

    Returns:
        str: A pseudo-random name string.
    """
    return Faker('en_AU').name()


def days_between(d1: datetime, d2: datetime) -> int:
    """
    Calculate number of days between two dates.

    Args:
        d1 (datetime): Start date.
        d2 (datetime): End date.

    Returns:
        int: Number of days between (can be negative).
    """
    return (d2 - d1).days


def advance_date(date: datetime, days: int) -> datetime:
    """
    Add a number of days to a date.

    Args:
        date (datetime): Starting date.
        days (int): Number of days to advance.

    Returns:
        datetime: New date.
    """
    return date + timedelta(days=days)

def weighted_sample(items: list, weights: list, k: int = 1):
    return random.choices(items, weights=weights, k=k)[0]