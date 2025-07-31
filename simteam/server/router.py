# router.py
from fastapi import FastAPI
from simteam.server.api.v1 import employees
from simteam.server.api.v1 import eventlog
from simteam.server.api.v1 import simulate
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    root_path="/api",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict by domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees.router, prefix="/v1")
app.include_router(eventlog.router, prefix="/v1")
app.include_router(simulate.router, prefix="/v1")