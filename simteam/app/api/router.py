# router.py
from fastapi import FastAPI
from simteam.app.api.v1 import employees
from simteam.app.api.v1 import eventlog

app = FastAPI()
app.include_router(employees.router, prefix="/api/v1")
app.include_router(eventlog.router, prefix="/api/v1")