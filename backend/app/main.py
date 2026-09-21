from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.core.config import settings
from app.core.hardening import RateLimitMiddleware, SecurityHeadersMiddleware
from app.core.logging import configure_logging
from app.services.auth_service import AuthError

configure_logging()

app = FastAPI(title=settings.product_name, version=settings.release_id)


@app.exception_handler(AuthError)
async def handle_auth_error(_: Request, exc: AuthError) -> JSONResponse:
    """Return actionable JSON for expected authentication failures.

    AuthService deliberately raises a domain exception so the service layer is
    independent from FastAPI.  The API boundary must translate that exception;
    otherwise normal invalid credentials or an expired one-time token becomes
    an opaque HTTP 500 and the browser appears to do nothing.
    """
    detail = str(exc)
    if detail == "Invalid email or password." or detail.endswith("account is not active."):
        status_code = 401
    elif detail == "A user with that email already exists.":
        status_code = 409
    else:
        status_code = 400

    headers = {"WWW-Authenticate": "Bearer"} if status_code == 401 else None
    return JSONResponse(status_code=status_code, content={"detail": detail}, headers=headers)

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
