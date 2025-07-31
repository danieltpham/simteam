from enum import Enum, auto


class Role(str, Enum):
    CEO = "CEO"
    VP = "VP"
    DIRECTOR = "Director"
    MANAGER = "Manager"
    SENIOR_ANALYST = "Senior Analyst"
    ANALYST = "Analyst"
    
    @staticmethod
    def get_level(role: "Role") -> int:
        """
        Return the numeric hierarchy level of a role.
        Lower is higher in the org.
        """
        hierarchy = {
            Role.CEO: 0,
            Role.VP: 1,
            Role.DIRECTOR: 2,
            Role.MANAGER: 3,
            Role.SENIOR_ANALYST: 4,
            Role.ANALYST: 5,
        }
        return hierarchy[role]


class EventType(str, Enum):
    EMPLOYED = "employed"
    LEFT = "left"
    PROMOTED = "promoted"
    CHANGE = "change"


# Maximum quotas for each role
# ROLE_QUOTAS = {
#     Role.CEO: 1,
#     Role.VP: 3,
#     Role.DIRECTOR: 10,     # max 4 per VP
#     Role.MANAGER: 10,      # max 5 per Director
#     Role.SENIOR_ANALYST: 30,
#     Role.ANALYST: 50,
# }

# # Maximum number of employees allowed in the simulation
# MAX_EMPLOYEES = 100

# # Max events of the same type per day
MAX_EVENTS_PER_TYPE = 3

# # Max events overall per day (after truncation)
# MAX_EVENTS_PER_DAY = 8

# # Number of days a vacant role must be filled by
# VACANCY_FILL_DEADLINE_DAYS = 14

# # Minimum number of employees before "leaving" is allowed
# MIN_EMPLOYEES_FOR_LEAVING = 30

# ALLOWED_MANAGER_MAPPING = {
#     Role.ANALYST: {Role.SENIOR_ANALYST, Role.MANAGER},
#     Role.SENIOR_ANALYST: {Role.MANAGER},
#     Role.MANAGER: {Role.DIRECTOR},
#     Role.DIRECTOR: {Role.VP},
#     Role.VP: {Role.CEO},
# }

# PROMOTION_ORDER = {
#     Role.ANALYST: Role.SENIOR_ANALYST,
#     Role.SENIOR_ANALYST: Role.MANAGER,
#     Role.MANAGER: Role.DIRECTOR,
#     Role.DIRECTOR: Role.VP,
#     Role.VP: Role.CEO,
# }