# simteam/server/api/v1/model.py

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict

from simteam.core.orgsimulator import OrgSimulator
from simteam.core.config import SimulationConfig, get_default_config
from simteam.core.enums import Role, EventType

from automl.surrogate_trainer import SurrogateTrainer
from automl.config import target_cols

from pydantic import BaseModel
from typing import Dict

class DailyStats(BaseModel):
    hire: int
    promote: int
    leave: int
    total_employees: int

class ActualSim(BaseModel):
    time_series: Dict[str, DailyStats]
    stats: Dict[str, float]

class ModelResponse(BaseModel):
    actual_sim: ActualSim
    predicted_stats: Dict[str, float]

router = APIRouter(prefix="/simulate", tags=["SIMULATION"])

class SimulationInput(BaseModel):
    """
    Input schema for running a simulation and surrogate model prediction.
    """
    seed: int = 42
    weight_employed: int = Field(ge=1, le=5)
    weight_promoted: int = Field(ge=1, le=5)
    weight_change: int = Field(ge=1, le=5)
    weight_left: int = Field(ge=1, le=5)
    min_employees_for_leaving: int
    min_events_per_week: int
    max_events_per_day: int
    max_events_per_type: int
    sim_days: int = 365


# Load the surrogate model once
_surrogate = SurrogateTrainer()
_surrogate.load()


@router.get("/", response_model=ModelResponse)
def run_simulation_and_predict(input: SimulationInput = Depends()):
    """
    Run the rule-based simulator and predict summary outcomes using the surrogate model.

    Returns:
        - Actual simulation results:
            - A time series of key events (hire, promote, leave, total employees)
            - Summary statistics (e.g. total hires, promotions, etc.)
        - Surrogate model prediction of the same summary statistics based on input configuration
    """
    base_cfg = get_default_config()

    config = SimulationConfig(
        role_quotas={**base_cfg.role_quotas, Role.MANAGER: 15},
        max_employees=100,
        max_events_per_type=input.max_events_per_type,
        max_events_per_day=input.max_events_per_day,
        vacancy_fill_deadline_days=10,
        min_employees_for_leaving=input.min_employees_for_leaving,
        promotion_order=base_cfg.promotion_order,
        allowed_manager_mapping=base_cfg.allowed_manager_mapping,
        event_type_weights={
            EventType.EMPLOYED: input.weight_employed,
            EventType.PROMOTED: input.weight_promoted,
            EventType.LEFT: input.weight_left,
            EventType.CHANGE: input.weight_change,
        },
        event_type_caps=base_cfg.event_type_caps,
        min_events_per_week=input.min_events_per_week,
        random_seed=input.seed,
    )

    # Run the actual simulation
    sim = OrgSimulator(start_date=datetime(2025, 1, 1), config=config)
    sim.simulate_for_days(input.sim_days)
    stats = sim.compute_hiring_statistics()

    # Build time series event summary
    time_series = {}
    for event in sim.event_log:
        date = event.date.date().isoformat()
        if date not in time_series:
            time_series[date] = {"hire": 0, "promote": 0, "leave": 0}
        if event.event_type == EventType.EMPLOYED:
            time_series[date]["hire"] += 1
        elif event.event_type == EventType.PROMOTED:
            time_series[date]["promote"] += 1
        elif event.event_type == EventType.LEFT:
            time_series[date]["leave"] += 1

    # Add total employees per date
    for date in time_series:
        total = sum(
            1 for e in sim.employees.values()
            if e.state.active and e.state.hire_date.date().isoformat() <= date
        )
        time_series[date]["total_employees"] = total

    # Prepare input vector for surrogate model prediction
    X_pred = [[
        input.seed,
        input.weight_employed,
        input.weight_promoted,
        input.weight_change,
        input.weight_left,
        input.min_employees_for_leaving,
        input.min_events_per_week,
        input.max_events_per_day,
        input.max_events_per_type
    ]]
    y_pred = _surrogate.predict(X_pred)

    # --- Format predictions ---
    raw_pred = dict(zip(target_cols, y_pred[0]))
    int_fields = {
        "total_num_hired",
        "total_num_left",
        "total_num_promoted",
        "org_saturation_day"
    }
    predicted_stats = {
        k: int(v) if k in int_fields else round(float(v), 3)
        for k, v in raw_pred.items()
    }

    return ModelResponse(
        actual_sim=ActualSim(
            time_series=time_series,
            stats=stats
        ),
        predicted_stats=predicted_stats
    )