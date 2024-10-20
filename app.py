"""
This is a FastFood API. 🍔

It implements all the necessary endpoints to manage a FastFood restaurant.
Allowing the creation of clients, products, and purchases.
Managing the queue of purchases and the status of the purchases.

It was developed as a challenge project for the FIAP Software Architecture Post Graduation 9th class.
"""

from fastapi import FastAPI

from src.adapters.driven.infra.database.db import start_db
from src.adapters.driver.API import (
    client_router,
    product_router,
    purchase_router,
    queue_router,
)


app = FastAPI(
    title="FastFood API - FIAP-9SOAT 🚀",
    description=__doc__,
    summary="Challenge project for FIAP Software Architecture Post Graduation 9th class.",
    version="0.0.1",
    # terms_of_service="http://example.com/terms/",
    contact={
        "name": "Lucas Maion",
        "url": "https://github.com/LucasMaion",
        "email": "lucasmgois@outlook.com",
    },
    license_info={
        "name": "MIT License",
        "identifier": "MIT",
    },
)

start_db()


@app.get("/")
def welcome():
    """
    Welcome Message
    """
    return "Welcome to the API"


@app.get("/health_check")
def health_check():
    """
    Request this to check on the server health.
    """
    return "Healthy"


app.include_router(client_router.router)
app.include_router(product_router.router)
app.include_router(purchase_router.router)
app.include_router(queue_router.router)
