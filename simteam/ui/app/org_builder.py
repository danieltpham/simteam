import pandas as pd
from typing import List, Dict, Optional, Tuple

def build_org_structure(df: pd.DataFrame, temp_list: Dict, date: Optional[str] = None) -> Tuple[List[Dict], List[Dict]]:
       
    df["date"] = pd.to_datetime(df["date"])
    if date:
        df = df[df["date"] <= pd.to_datetime(date)]

    latest = df.sort_index(ascending=False).drop_duplicates("employee_id", keep='first')
    active = latest[latest["event_type"] != "first"]

    def fake_img(id): return f"https://bumbeishvili.github.io/avatars/avatars/portrait{id}.png"

    # Build base list
    actives = [
        {
            "id": row["employee_id"],
            "parentId": row["manager_id"],
            "name": row["employee_id"],
            "positionName": row["role"],
            "imageUrl": fake_img(int(row["employee_id"].replace("EMP", "").replace("TEMP", "130"))),  # TEMPs as 100 fallback
        }
        for _, row in active.iterrows()
    ]

    # Add TEMP managers if any are referenced in parentId
    temp_ids = { row["manager_id"]
        for _, row in active.iterrows()
        if isinstance(row["manager_id"], str) and row["manager_id"].startswith("TEMP")
    }
    
    temps = [
        {"id": temp_id,
         "parentId": temp_list[temp_id],
         "name": "Empty position",
         "positionName": "Empty position",
         "imageUrl": fake_img(130),
         } for temp_id in temp_ids]

    return (actives, temps)
