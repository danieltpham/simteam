# # app/org_builder.py

# import pandas as pd
# from typing import List, Dict, Optional

# def build_org_structure(df: pd.DataFrame, date: Optional[str] = None) -> List[Dict]:
#     """
#     Build org chart node structure for a given snapshot date.
#     """
#     df["date"] = pd.to_datetime(df["date"])
#     if date:
#         df = df[df["date"] <= pd.to_datetime(date)]

#     latest = df.sort_values("date", ascending=False).drop_duplicates("employee_id")
#     active = latest[latest["event_type"] != "left"]

#     return [
#         {
#             "id": row["employee_id"],
#             "parentId": row["manager_id"],
#             "name": row["employee_id"],
#             "title": row["role"]
#         }
#         for _, row in active.iterrows()
#     ]


# app/org_builder.py

import pandas as pd
from typing import List, Dict, Optional
import random

def build_org_structure(df: pd.DataFrame, date: Optional[str] = None) -> List[Dict]:
    df["date"] = pd.to_datetime(df["date"])
    if date:
        df = df[df["date"] <= pd.to_datetime(date)]

    latest = df.sort_values("date", ascending=False).drop_duplicates("employee_id")
    active = latest[latest["event_type"] != "left"]

    def fake_email(eid): return f"{eid.lower()}@simteam.com"
    def fake_name(eid): return ("Emp", eid[-3:])  # ("Emp", "001")
    def fake_img(): return f"https://bumbeishvili.github.io/avatars/avatars/portrait{random.randint(10,99)}.png"

    return [
        {
            "id": row["employee_id"],
            "parentId": row["manager_id"],
            "name": fake_name(row["employee_id"])[0],
            "lastName": fake_name(row["employee_id"])[1],
            "position": row["role"],
            "image": fake_img(),
            "email": fake_email(row["employee_id"]),
            "phone_number": "000-000-0000",
            "hire_date": row["date"].isoformat(),
            "job_id": row["role"].upper().replace(" ", "_"),
            "salary": random.randint(70000, 200000),
            "commission_pct": None,
            "department_id": 1,
            "job_min_salary": 60000,
            "location_state": "Melbourne",
            "job_max_salary": 220000,
            "department_name": "SimOps",
            "department_location_id": 999,
            "department_location_street_address": "123 Strategy Rd",
            "department_location_postal_code": "3000",
            "department_location_country_id": "AU",
            "department_location_country_name": "Australia",
            "department_location_country_region_id": 3,
            "department_location_country_region_name": "Asia-Pacific"
        }
        for _, row in active.iterrows()
    ]