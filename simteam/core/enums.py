from enum import Enum, auto


class Role(str, Enum):
    CEO = "CEO"
    VP = "VP"
    DIRECTOR = "Director"
    MANAGER = "Manager"
    SENIOR_ANALYST = "Senior Analyst"
    ANALYST = "Analyst"


class EventType(str, Enum):
    EMPLOYED = "employed"
    LEFT = "left"
    PROMOTED = "promoted"
    CHANGE = "change"


# Maximum quotas for each role
ROLE_QUOTAS = {
    Role.CEO: 1,
    Role.VP: 3,
    Role.DIRECTOR: 20,     # max 5 per VP
    Role.MANAGER: 50,      # max 5 per Director
    Role.SENIOR_ANALYST: 100,
    Role.ANALYST: 100,
}

# Maximum number of employees allowed in the simulation
MAX_EMPLOYEES = 100

# Max events of the same type per day
MAX_EVENTS_PER_TYPE = 3

# Max events overall per day (after truncation)
MAX_EVENTS_PER_DAY = 8

# Number of days a vacant role must be filled by
VACANCY_FILL_DEADLINE_DAYS = 14

# Minimum number of employees before "leaving" is allowed
MIN_EMPLOYEES_FOR_LEAVING = 30