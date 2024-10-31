from fastapi import APIRouter

router = APIRouter(
    prefix="/payment",
    tags=["payment"],
)


# TODO: add make payment; add get payment methods
@router.get("/")
async def get_item():
    return {"item": {"id": 1, "name": "Item name"}}
