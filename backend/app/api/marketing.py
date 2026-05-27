from __future__ import annotations

from fastapi import APIRouter, Body

router = APIRouter()


@router.post("/marketing/analytics")
def track_event(payload: dict = Body(...)):
    # Lightweight acceptor for anonymous marketing analytics events.
    # For now simply log or accept without persistence. This endpoint allows
    # the frontend to POST page views and simple interaction events for
    # heatmap/analytics experimentation.
    # NOTE: in a real deployment you'd validate and store or forward events.
    print("MARKETING EVENT:", payload)
    return {"status": "ok"}
