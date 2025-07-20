# router.py
from fastapi import FastAPI
from simteam.server.api.v1 import employees
from simteam.server.api.v1 import eventlog
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict by domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees.router, prefix="/api/v1")
app.include_router(eventlog.router, prefix="/api/v1")