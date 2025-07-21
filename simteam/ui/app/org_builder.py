# app/org_builder.py

import pandas as pd
from typing import List, Dict, Optional

def build_org_structure(df: pd.DataFrame, date: Optional[str] = None) -> List[Dict]:
    df["date"] = pd.to_datetime(df["date"])
    if date:
        df = df[df["date"] <= pd.to_datetime(date)]

    latest = df.sort_values("date", ascending=False).drop_duplicates("employee_id")
    active = latest[latest["event_type"] != "left"]
    
    def fake_img(id): return f"https://bumbeishvili.github.io/avatars/avatars/portrait{id}.png"

    return [
        {
            "id": row["employee_id"],
            "parentId": row["manager_id"],
            "name": row["employee_id"],
            "positionName": row["role"],
            "imageUrl": fake_img(int(row["employee_id"].replace('EMP',''))),
        }
        for _, row in active.iterrows()
    ]