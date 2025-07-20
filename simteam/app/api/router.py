# router.py
from fastapi import FastAPI
from app.api.v1 import employees

app = FastAPI()
app.include_router(employees.router, prefix="/api/v1")
