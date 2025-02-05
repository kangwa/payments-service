from fastapi import APIRouter

from app.accounts.ports.rest.auth_api import router as auth_router
from app.accounts.ports.rest.merchant_api import router as merchant_router
from app.accounts.ports.rest.organization_api import router as organization_router
from app.accounts.ports.rest.users_api import router as user_router

accounts_router = APIRouter(prefix="/accounts")

accounts_router.include_router(auth_router)
accounts_router.include_router(merchant_router)
accounts_router.include_router(organization_router)
accounts_router.include_router(user_router)
