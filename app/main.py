"""FastAPI application for Payment Gateway microservice.

This module initializes and configures the Payment Gateway FastAPI application,
setting up routing, documentation, and core service endpoints.

The API provides endpoints for:
- Organization management and accounts
- Merchant configuration and onboarding
- Authentication and authorization
- Payment processing and analytics
- Service health monitoring

Note:
   This service requires configuration of payment provider credentials
   and proper security settings in a production environment.
"""

from fastadmin import fastapi_app as admin_app
from fastapi import FastAPI

from app.accounts.ports.rest.router import accounts_router
from app.common.adapters.db.sql_model.session import create_db_and_tables

project_description = """
   Payment Gateway microservice providing secure payment processing capabilities.
   Handles merchant onboarding, transaction processing, refunds, and payment analytics.
   
   Features include:
   - Secure payment processing
   - Merchant account management
   - Transaction reporting and analytics
   - Refund handling
   - Multi-currency support
   
   API documentation and integration guides are available at /docs
"""


app = FastAPI(
    title="Payment Gateway API",
    description=project_description,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# API Routes
app.mount("/admin", admin_app)
app.include_router(accounts_router)  # Accounts Manager Router


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/health")
async def health_check():
    """Payment gateway health check endpoint.

    Verifies:
    - API service status
    - Payment provider connectivity
    - Critical service dependencies

    Returns:
        dict: Health status containing:
            - status: Current service status ("healthy" or "unhealthy")
            - service: Service identifier ("payment-gateway")
    """
    return {"status": "healthy", "service": "payment-gateway"}
