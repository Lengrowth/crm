from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db_session
from app.models.domain import Module, SaaSUser
from app.schemas.domain import ModuleRead, PlanRead
from app.schemas.implementation import ImplementationTemplateRead
from app.schemas.modules import ModuleBundleRead, ModuleCatalogRead, PublicModuleRead
from app.services.catalog_service import CatalogService
from app.services.module_entitlement_service import module_entitlement_service

router = APIRouter(tags=["catalog"])
catalog_service = CatalogService()


@router.get("/modules", response_model=list[ModuleRead])
def list_modules(session: Session = Depends(get_db_session)):
    return module_entitlement_service.list_public_catalog(session)


def _catalog_read(module: Module) -> ModuleCatalogRead:
    return ModuleCatalogRead(
        id=module.id,
        code=module.code,
        name=module.name,
        category=module.category,
        description=module.description,
        public_description=module.public_description,
        internal_description=module.internal_description,
        is_active=module.is_active,
        is_marketed=module.is_marketed,
        display_order=module.display_order,
        dependency_codes=list(module.dependency_codes_json or []),
        incompatibility_codes=list(module.incompatibility_codes_json or []),
        required_app=module.required_app,
        minimum_app_version=module.minimum_app_version,
        compatible_app_version=module.compatible_app_version,
        default_roles=list(module.default_roles_json or []),
        default_workspaces=list(module.default_workspaces_json or []),
        configuration_schema=dict(module.configuration_schema_json or {}),
        administrative_visibility=module.administrative_visibility,
        alias_of=module.alias_of,
        deprecated_at=module.deprecated_at,
        metadata_version=module.metadata_version,
    )


@router.get("/catalog/modules", response_model=list[ModuleCatalogRead])
def list_internal_modules(
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    # Catalog metadata is not tenant data; authentication is still required for
    # the internal view so it cannot be used as an anonymous control-plane read.
    return [_catalog_read(module) for module in module_entitlement_service.list_catalog(session)]


@router.get("/public/modules", response_model=list[PublicModuleRead])
def list_public_modules(session: Session = Depends(get_db_session)):
    return [
        PublicModuleRead(
            code=module.code,
            name=module.name,
            category=module.category,
            description=module.public_description or module.description or "",
            display_order=module.display_order,
        )
        for module in module_entitlement_service.list_public_catalog(session)
    ]


@router.get("/module-bundles", response_model=list[ModuleBundleRead])
def list_module_bundles(
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    return module_entitlement_service.list_bundles(session)


@router.get("/plans", response_model=list[PlanRead])
def list_plans(session: Session = Depends(get_db_session)):
    return catalog_service.list_plans(session)


@router.get("/implementation-templates", response_model=list[ImplementationTemplateRead])
def list_templates(session: Session = Depends(get_db_session)):
    return catalog_service.list_templates(session)
