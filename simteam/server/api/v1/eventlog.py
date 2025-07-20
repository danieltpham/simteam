from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from simteam.core.models.base import EventLog
from simteam.server.db.models import EventLogORM
from simteam.server.db.session import get_db
from simteam.core.enums import Role, EventType

from datetime import datetime

router = APIRouter(prefix="/eventlog", tags=["EventLog"])

@router.get("/", response_model=List[EventLog])
def get_all_eventlogs(db: Session = Depends(get_db)):
    return db.query(EventLogORM).all()

@router.post("/", response_model=EventLog)
def create_eventlog(event: EventLog, db: Session = Depends(get_db)):
    event_db = EventLogORM(
        date=event.date if isinstance(event.date, datetime) else datetime.fromisoformat(event.date),
        event_type=EventType(event.event_type),
        employee_id=event.employee_id,
        role=Role(event.role),
        manager_id=event.manager_id,
        department=event.department,
        team=event.team
    )
    db.add(event_db)
    db.commit()
    db.refresh(event_db)
    return event_db
