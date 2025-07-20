import json
from pathlib import Path
from datetime import datetime

from simteam.server.db.session import Base, engine, SessionLocal
from simteam.server.db import models
from simteam.core.enums import Role, EventType

from sqlalchemy.exc import SQLAlchemyError


def parse_datetime(dt_str: str) -> datetime | None:
    return datetime.fromisoformat(dt_str) if dt_str else None


def reset_database() -> None:
    """Drop and recreate all tables."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def load_json(filepath: Path) -> dict:
    with open(filepath, "r") as f:
        return json.load(f)


def insert_data(session, data: dict) -> None:
    """Insert employees (incl. temps) and event logs into DB."""
    try:
        all_employees = data.get("employees", []) + data.get("temp_employees", [])
        for entry in all_employees:
            session.add(models.EmployeeORM(
                emp_id=entry["emp_id"],
                role=Role(entry["role"]),
                manager_id=entry.get("manager_id"),
                department=entry.get("department"),
                team=entry.get("team"),
                hire_date=parse_datetime(entry["hire_date"]),
                active=entry["active"]
            ))

        for entry in data.get("event_log", []):
            session.add(models.EventLogORM(
                date=parse_datetime(entry["date"]),
                event_type=EventType(entry["event_type"]),
                employee_id=entry["employee_id"],
                role=Role(entry["role"]),
                manager_id=entry.get("manager_id"),
                department=entry.get("department"),
                team=entry.get("team")
            ))

        session.commit()

    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ DB insert failed: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    print("🔄 Resetting and populating database...")
    reset_database()
    session = SessionLocal()
    data = load_json(Path("sim_output.json"))
    insert_data(session, data)
    print("✅ Database created and populated.")
