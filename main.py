from fastapi import FastAPI, APIRouter, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from src.middleware.ip_middleware import AddClientIPMiddleware
from src.health.router import routerHealth
from src.user.router import routerUser
from src.refresh_token.router import routerRefreshToken
from src.utils.allowed_middleware import (
    ALLOWED_METHODS,
    ALLOWED_HEADERS,
    ALLOWED_ORIGINS,
)
from fastapi.responses import JSONResponse
from decouple import config
import uvicorn as uvicorn
import logging
import sys

# environment server
ENVIRONMENT = config("ENVIRONMENT", default="prod")

# Konfigurasi Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"
)
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

# Menjalankan informasi bahwa API sedang dijalankan
logger.debug("API is starting up")

logger.info(f"Environment Server: {ENVIRONMENT}")


# Exception handler
async def custom_exception_handler(request, exc):
    if app.debug:  # Check if the app is in debug mode
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )
    else:
        logger.error(f"An error occurred: {exc}")  # Log the error
        return JSONResponse(
            status_code=400,
            content={
                "detail": "Internal Server Error"
            },  # Generic message for production
        )


def create_app() -> FastAPI:
    app = FastAPI(
        swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
        version="1.0.0",
        title="RESTful API Aksara AI Backend",
        description="Swagger documentation RESTful API for Aksara AI Backend",
        docs_url="/api/docs",  # 👈 Ganti path Swagger UI
        openapi_url="/api/docs/openapi.json",  # 👈 Ganti path OpenAPI JSON
    )

    # Add custom exception handler
    app.add_exception_handler(Exception, custom_exception_handler)

    # Middleware for adding client IP
    app.add_middleware(AddClientIPMiddleware)

    # Middleware for adding CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,  # Allows all domains
        allow_methods=ALLOWED_METHODS,  # Allows all HTTP methods
        allow_headers=ALLOWED_HEADERS,  # Allows all headers (Authorization, Content-Type, etc.)
        allow_credentials=True,  # Allows cookies or authentication credentials
    )

    # Middleware for adding security headers
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response: Response = await call_next(request)

        # Longgarkan hanya untuk Swagger UI
        if request.url.path.startswith("/api/docs") or request.url.path.startswith(
            "/endpoints/docs"
        ):
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https:; "
                "style-src 'self' 'unsafe-inline' https:; "
                "img-src 'self' https: data:;"
            )
        # else:
        #     # CSP ketat untuk route lain
        #     response.headers["Content-Security-Policy"] = (
        #         "default-src 'self'; img-src 'self' https://;"
        #     )

        response.headers["Strict-Transport-Security"] = (
            "max-age=63072000; includeSubDomains"
        )
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
        return response

    # Create router with the prefix '/api/v1'
    router_api_v1 = APIRouter(prefix="/api/v1")

    router_api_v1.include_router(routerHealth, prefix="/health", tags=["Health Check"])
    router_api_v1.include_router(
        routerRefreshToken, prefix="/refresh-token", tags=["Refresh Token"]
    )
    router_api_v1.include_router(routerUser, prefix="/users", tags=["Users"])

    app.include_router(router_api_v1)
    return app


# def create_limited_docs_app() -> FastAPI:
#     limited_app = FastAPI(
#         title="Tahanan & Barbuk",
#         version="1.0",
#         docs_url="/docs",
#         openapi_url="/docs/openapi.json",
#         redoc_url=None,
#     )
#     return limited_app


app = create_app()

# Mount sub-app di path root "/endpoints-data"
# app.mount("/endpoints", create_limited_docs_app())

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        debug=True,
        reload=True,
    )
