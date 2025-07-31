# simteam/core/config.py

from dataclasses import dataclass, field
from typing import Dict
from simteam.core.enums import Role, EventType

@dataclass
class SimulationConfig:
    role_quotas: Dict[Role, int]
    max_employees: int
    max_events_per_type: int
    max_events_per_day: int
    vacancy_fill_deadline_days: int
    min_employees_for_leaving: int
    promotion_order: Dict[Role, Role]
    allowed_manager_mapping: Dict[Role, set[Role]]
    random_seed: int = 42

    event_type_weights: Dict[EventType, int] = field(default_factory=lambda: {
        EventType.EMPLOYED: 4,
        EventType.PROMOTED: 2,
        EventType.LEFT: 1,
        EventType.CHANGE: 1,
    })
    event_type_caps: Dict[EventType, int] = field(default_factory=lambda: {
        EventType.EMPLOYED: 3,
        EventType.PROMOTED: 3,
        EventType.LEFT: 2,
        EventType.CHANGE: 2,
    })
    min_events_per_week: int = 1

    
def get_default_config() -> SimulationConfig:

    return SimulationConfig(
        role_quotas={
            Role.CEO: 1,
            Role.VP: 3,
            Role.DIRECTOR: 10,
            Role.MANAGER: 10,
            Role.SENIOR_ANALYST: 30,
            Role.ANALYST: 50,
        },
        max_employees=100,
        max_events_per_type=3,
        max_events_per_day=8,
        vacancy_fill_deadline_days=14,
        min_employees_for_leaving=30,
        promotion_order={
            Role.ANALYST: Role.SENIOR_ANALYST,
            Role.SENIOR_ANALYST: Role.MANAGER,
            Role.MANAGER: Role.DIRECTOR,
            Role.DIRECTOR: Role.VP,
            Role.VP: Role.CEO,
        },
        allowed_manager_mapping={
            Role.ANALYST: {Role.SENIOR_ANALYST, Role.MANAGER},
            Role.SENIOR_ANALYST: {Role.MANAGER},
            Role.MANAGER: {Role.DIRECTOR},
            Role.DIRECTOR: {Role.VP},
            Role.VP: {Role.CEO},
        }
    )