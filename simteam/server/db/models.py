# app/db/models.py
from sqlalchemy import Column, String, DateTime, Boolean, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship
from simteam.server.db.session import Base
from simteam.core.enums import Role, EventType


class EmployeeORM(Base):
    __tablename__ = "employees"

    emp_id = Column(String, primary_key=True, index=True)
    role = Column(Enum(Role), nullable=False)
    manager_id = Column(String, ForeignKey("employees.emp_id"), nullable=True)
    department = Column(String, nullable=True)
    team = Column(String, nullable=True)
    hire_date = Column(DateTime, nullable=False)
    active = Column(Boolean, default=True)

    events = relationship("EventLogORM", back_populates="employee")


class EventLogORM(Base):
    __tablename__ = "event_log"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(DateTime, nullable=False)
    event_type = Column(Enum(EventType), nullable=False)
    employee_id = Column(String, ForeignKey("employees.emp_id"), nullable=False)
    role = Column(Enum(Role), nullable=False)
    manager_id = Column(String, nullable=True)
    department = Column(String, nullable=True)
    team = Column(String, nullable=True)

    employee = relationship("EmployeeORM", back_populates="events")
