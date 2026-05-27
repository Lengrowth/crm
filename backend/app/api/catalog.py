from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.schemas.domain import ModuleRead, PlanRead
from app.schemas.implementation import ImplementationTemplateRead
from app.services.catalog_service import CatalogService

router = APIRouter(tags=["catalog"])
catalog_service = CatalogService()


@router.get("/modules", response_model=list[ModuleRead])
def list_modules(session: Session = Depends(get_db_session)):
    return catalog_service.list_modules(session)


@router.get("/plans", response_model=list[PlanRead])
def list_plans(session: Session = Depends(get_db_session)):
    return catalog_service.list_plans(session)


@router.get("/implementation-templates", response_model=list[ImplementationTemplateRead])
def list_templates(session: Session = Depends(get_db_session)):
    return catalog_service.list_templates(session)
