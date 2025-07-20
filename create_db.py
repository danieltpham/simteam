# create_db.py

import json
from pathlib import Path
from simteam.app.db.session import Base, engine, SessionLocal
from simteam.app.db import models  # Ensure models are registered
from simteam.core.enums import Role, EventType
from datetime import datetime

def parse_datetime(dt_str):
    return datetime.fromisoformat(dt_str) if dt_str else None

def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def load_json(filepath: Path) -> dict:
    with open(filepath, "r") as f:
        return json.load(f)

def insert_data(db_session, data: dict):
    # Insert all employees (regular + temp)
    all_employees = data.get("employees", []) + data.get("temp_employees", [])
    for entry in all_employees:
        db_session.add(models.EmployeeORM(
            emp_id=entry["emp_id"],
            role=Role(entry["role"]),
            manager_id=entry.get("manager_id"),
            department=entry.get("department"),
            team=entry.get("team"),
            hire_date=parse_datetime(entry["hire_date"]),
            active=entry["active"]
        ))

    # Insert event logs
    for entry in data.get("event_log", []):
        db_session.add(models.EventLogORM(
            date=parse_datetime(entry["date"]),
            event_type=EventType(entry["event_type"]),
            employee_id=entry["employee_id"],
            role=Role(entry["role"]),
            manager_id=entry.get("manager_id"),
            department=entry.get("department"),
            team=entry.get("team")
        ))

    db_session.commit()

if __name__ == "__main__":
    reset_database()
    session = SessionLocal()
    json_data = load_json(Path("sim_output.json"))
    insert_data(session, json_data)
    session.close()
