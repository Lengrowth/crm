from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.hardening import RateLimitMiddleware, SecurityHeadersMiddleware
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(title=settings.product_name, version=settings.release_id)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)

if settings.cors_origin_list:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": settings.product_name,
        "status": "ok",
        "release_id": settings.release_id,
    }
