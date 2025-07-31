# app/db/models.py

from sqlalchemy import Column, String, DateTime, Boolean, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship
from simteam.server.db.session import Base
from simteam.core.enums import Role, EventType

class EmployeeORM(Base):
    """
    Table: employees

    Represents an employee in the organisation. 
    Each employee may optionally report to another employee (via manager_id).

    Columns:
    - emp_id: Unique identifier for the employee (TEMP/EMP-prefixed).
    - role: Organisational role, defined in the `Role` enum (e.g., Analyst, Manager, VP).
    - manager_id: Optional ID of the employee’s direct manager.
    - department: Optional department name (e.g., Engineering, Marketing).
    - team: Optional sub-team name within a department.
    - hire_date: Date the employee joined the organisation.
    - active: Boolean flag for whether the employee is currently active.

    Relationships:
    - events: One-to-many relationship to EventLogORM, representing career events.
    """
    __tablename__ = "employees"

    emp_id = Column(String, primary_key=True, index=True, doc="Unique employee ID (e.g., EMP001 or TEMP123)")
    role = Column(Enum(Role), nullable=False, doc="Organisational role of the employee (Role enum)")
    manager_id = Column(String, nullable=True, doc="ID of the employee's manager (may be TEMP during hiring)")
    department = Column(String, nullable=True, doc="Optional department assignment")
    team = Column(String, nullable=True, doc="Optional team assignment")
    hire_date = Column(DateTime, nullable=False, doc="Date when employee was hired")
    active = Column(Boolean, default=True, doc="Whether the employee is currently active")

    events = relationship("EventLogORM", back_populates="employee", doc="List of associated event log entries")


class EventLogORM(Base):
    """
    Table: event_log

    Records an event in an employee’s lifecycle (e.g., hire, promotion, termination).

    Columns:
    - id: Auto-incrementing primary key.
    - date: Date the event occurred.
    - event_type: Type of event (e.g., hire, promote, exit), from `EventType` enum.
    - employee_id: Foreign key linking to Employee.emp_id.
    - role: Role at the time of the event.
    - manager_id: Reporting manager at the time.
    - department: Department at the time of the event.
    - team: Team at the time of the event.

    Relationships:
    - employee: Many-to-one link to the EmployeeORM.
    """
    __tablename__ = "event_log"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, doc="Primary key")
    date = Column(DateTime, nullable=False, doc="Date the event occurred")
    event_type = Column(Enum(EventType), nullable=False, doc="Type of lifecycle event (EventType enum)")
    employee_id = Column(String, ForeignKey("employees.emp_id"), nullable=False, doc="Linked employee ID")
    role = Column(Enum(Role), nullable=False, doc="Role of the employee at the time of event")
    manager_id = Column(String, nullable=True, doc="Manager at the time of the event")
    department = Column(String, nullable=True, doc="Department at the time of the event")
    team = Column(String, nullable=True, doc="Team at the time of the event")

    employee = relationship("EmployeeORM", back_populates="events", doc="Associated employee entity")
