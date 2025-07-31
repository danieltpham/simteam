import os
from pathlib import Path
import pandas as pd
from itertools import product
from datetime import datetime
from tqdm import tqdm

from simteam.core.config import SimulationConfig, get_default_config
from simteam.core.orgsimulator import OrgSimulator
from simteam.core.enums import Role, EventType

DATA_PATH = Path(__file__).resolve().parent / "sim_training_data.csv"

# 8 valid weight combos: (LEFT, CHANGE, PROMOTED, EMPLOYED)
event_type_weight_combinations = [
    (1, 1, 2, 3),
    (1, 1, 2, 4),
    (1, 2, 3, 4),
    (1, 2, 3, 5),
    (1, 2, 4, 5),
    (2, 2, 3, 4),
    (2, 2, 3, 5),
    (2, 3, 4, 5),
]

# Grid parameters
min_employees_list = [10, 20, 30]
min_events_per_week_list = [1, 2]
max_events_per_day_list = [6, 7, 8]
max_events_per_type_list = [2, 3]
seeds = list(range(20))

manager_quota = 15
max_employees = 100
start_date = datetime(2025, 1, 1)


def generate_surrogate_training_data() -> pd.DataFrame:
    results = []
    grid = product(
        event_type_weight_combinations,
        min_employees_list,
        min_events_per_week_list,
        max_events_per_day_list,
        max_events_per_type_list,
        seeds,
    )

    for (
        (w_left, w_change, w_promoted, w_employed),
        min_employees_for_leaving,
        min_events_per_week,
        max_events_per_day,
        max_events_per_type,
        seed,
    ) in tqdm(grid, total=8 * 3 * 2 * 3 * 2 * 20):

        base_cfg = get_default_config()
        event_type_weights = {
            EventType.EMPLOYED: w_employed,
            EventType.PROMOTED: w_promoted,
            EventType.LEFT: w_left,
            EventType.CHANGE: w_change,
        }

        config = SimulationConfig(
            role_quotas={**base_cfg.role_quotas, Role.MANAGER: manager_quota},
            max_employees=max_employees,
            max_events_per_type=max_events_per_type,
            max_events_per_day=max_events_per_day,
            vacancy_fill_deadline_days=10,
            min_employees_for_leaving=min_employees_for_leaving,
            promotion_order=base_cfg.promotion_order,
            allowed_manager_mapping=base_cfg.allowed_manager_mapping,
            event_type_weights=event_type_weights,
            event_type_caps=base_cfg.event_type_caps,
            min_events_per_week=min_events_per_week,
            random_seed=seed,
        )

        sim = OrgSimulator(start_date=start_date, config=config)
        sim.simulate_for_days(365)
        sim.compute_hiring_statistics()
        row = sim.compute_hiring_statistics()

        row.update({
            "seed": seed,
            "weight_employed": w_employed,
            "weight_promoted": w_promoted,
            "weight_change": w_change,
            "weight_left": w_left,
            "min_employees_for_leaving": min_employees_for_leaving,
            "min_events_per_week": min_events_per_week,
            "max_events_per_day": max_events_per_day,
            "max_events_per_type": max_events_per_type
        })

        results.append(row)

    return pd.DataFrame(results)


if __name__ == "__main__":
    if not os.path.exists(DATA_PATH):
        print("📦 Training data not found. Generating synthetic dataset...")
        df = generate_surrogate_training_data()
        os.makedirs("training_data", exist_ok=True)
        df.to_csv(DATA_PATH, index=False)
        print(f"✅ Saved to {DATA_PATH}")
    else:
        print("✅ Training data already exists. Skipping generation.")
