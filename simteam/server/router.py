from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from simteam.server.api.v1 import employees, eventlog, simulate

# Create FastAPI app with custom docs path
app = FastAPI(
    root_path="/api",
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json"
)

# Provide a valid OpenAPI schema with version
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="S.I.M.T.E.A.M API",
        version="1.0.0",  # required!
        description="FastAPI Documentations for SIMTEAM. Currently read-only.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Mount local static folder to serve custom.css
app.mount("/static", StaticFiles(directory="simteam/server/api/static"), name="static")

# Allow CORS (optional but recommended)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register versioned API routers
app.include_router(employees.router, prefix="/v1")
app.include_router(eventlog.router, prefix="/v1")
app.include_router(simulate.router, prefix="/v1")

# Custom Swagger UI with CDN + local custom.css
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    html = get_swagger_ui_html(
        openapi_url="/api/openapi.json",
        title="SimTeam API - Swagger UI",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    ).body.decode()  # type: ignore

    # Inject custom CSS into the <head> section
    inject_css = '<link rel="stylesheet" type="text/css" href="/api/static/custom.css">'
    html = html.replace("</head>", f"{inject_css}</head>")
    return HTMLResponse(content=html)

# Required for OAuth2 redirect (even if unused)
@app.get("/docs/oauth2-redirect", include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()
