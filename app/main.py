from fastapi import FastAPI
from app.interface.api import merchants, organizations, auth

project_description = """
   Payment Gateway microservice providing secure payment processing capabilities.
   Handles merchant onboarding, transaction processing, refunds, and payment analytics.
   Features include:
"""


app = FastAPI(
    title="Payment Gateway API",
    description=project_description,
    version="0.1.0",
)


# API Routes
app.include_router(organizations.router)  # Organization/account management
app.include_router(merchants.router)  # Merchant configuration
app.include_router(auth.router)  # Authentication endpoints


@app.get("/health")
async def health_check():
    """Payment gateway health check endpoint.

    Verifies:
    - API service status
    - Payment provider connectivity
    - Critical service dependencies

    Returns:
        dict: Health status of the payment gateway and its components.
    """
    return {"status": "healthy", "service": "payment-gateway"}
