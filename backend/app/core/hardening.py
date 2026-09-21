from __future__ import annotations

from collections import defaultdict, deque
from time import monotonic
from typing import Optional

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.domain import SSORateLimitBucket


class InMemoryRateLimiter:
    def __init__(self) -> None:
        self._buckets: dict[str, deque[float]] = defaultdict(deque)

    def reset(self) -> None:
        self._buckets.clear()

    def allow(self, key: str, limit: int, window_seconds: int) -> tuple[bool, int]:
        now = monotonic()
        bucket = self._buckets[key]
        while bucket and now - bucket[0] >= window_seconds:
            bucket.popleft()

        if len(bucket) >= limit:
            retry_after = max(1, int(window_seconds - (now - bucket[0]))) if bucket else window_seconds
            return False, retry_after

        bucket.append(now)
        return True, 0


class DatabaseRateLimiter:
    """A small fixed-window limiter whose counters survive worker restarts."""

    def allow(self, session: Session, key: str, limit: int, window_seconds: int) -> tuple[bool, int]:
        from datetime import datetime, timedelta, timezone

        now = datetime.now(timezone.utc)
        bucket = session.execute(select(SSORateLimitBucket).where(SSORateLimitBucket.bucket_key == key)).scalar_one_or_none()
        if bucket is None:
            bucket = SSORateLimitBucket(bucket_key=key, window_started_at=now, request_count=0)
            session.add(bucket)
            try:
                session.flush()
            except IntegrityError:
                session.rollback()
                bucket = session.execute(select(SSORateLimitBucket).where(SSORateLimitBucket.bucket_key == key)).scalar_one()
        started = bucket.window_started_at.replace(tzinfo=timezone.utc) if bucket.window_started_at.tzinfo is None else bucket.window_started_at
        if now - started >= timedelta(seconds=window_seconds):
            bucket.window_started_at = now
            bucket.request_count = 0
        if bucket.request_count >= limit:
            retry_after = max(1, int((timedelta(seconds=window_seconds) - (now - started)).total_seconds()))
            session.commit()
            return False, retry_after
        bucket.request_count += 1
        session.commit()
        return True, 0


rate_limiter = InMemoryRateLimiter()


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        if settings.security_headers_enabled:
            response.headers.setdefault("X-Content-Type-Options", "nosniff")
            response.headers.setdefault("X-Frame-Options", "DENY")
            response.headers.setdefault("Referrer-Policy", "no-referrer")
            response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limiter: Optional[InMemoryRateLimiter] = None) -> None:
        super().__init__(app)
        self.limiter = limiter or rate_limiter

    @staticmethod
    def _normalize_path(path: str) -> str:
        normalized = path.rstrip("/")
        return normalized or "/"

    def _is_exempt_path(self, path: str) -> bool:
        normalized_path = self._normalize_path(path)
        for raw_prefix in settings.rate_limit_exempt_path_list:
            prefix = self._normalize_path(raw_prefix)
            if normalized_path == prefix or normalized_path.startswith(prefix + "/"):
                return True
        return False

    async def dispatch(self, request: Request, call_next) -> Response:
        if not settings.rate_limit_effective_enabled or self._is_exempt_path(request.url.path):
            return await call_next(request)

        client_host = request.client.host if request.client else "anonymous"
        key = f"{client_host}:{request.method}:{self._normalize_path(request.url.path)}"
        allowed, retry_after = self.limiter.allow(
            key,
            settings.rate_limit_max_requests,
            settings.rate_limit_window_seconds,
        )
        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded."},
                headers={"Retry-After": str(retry_after)},
            )

        return await call_next(request)
