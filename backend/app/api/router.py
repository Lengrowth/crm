from fastapi import APIRouter

from app.api import billing as billing_router
from app.api.audit import router as audit_router
from app.api.auth import router as auth_router
from app.api.catalog import router as catalog_router
from app.api.contact import router as contact_router
from app.api.domain_management import router as domain_management_router
from app.api.dashboard import router as dashboard_router
from app.api.health import router as health_router
from app.api.implementation import router as implementation_router
from app.api.integrations import router as integrations_router
from app.api.marketing import router as marketing_router
from app.api.modules import router as modules_router
from app.api.organizations import router as organizations_router
from app.api.provisioning import router as provisioning_router
from app.api.tenants import router as tenants_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(health_router)
api_router.include_router(audit_router)
api_router.include_router(catalog_router)
api_router.include_router(implementation_router)
api_router.include_router(integrations_router)
api_router.include_router(organizations_router)
api_router.include_router(tenants_router)
api_router.include_router(domain_management_router)
api_router.include_router(dashboard_router)
api_router.include_router(billing_router.router)
api_router.include_router(provisioning_router)
api_router.include_router(contact_router)
api_router.include_router(marketing_router)
api_router.include_router(modules_router)
