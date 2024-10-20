from fastapi import APIRouter

router = APIRouter(
    prefix="/purchase",
    tags=["purchase"],
)


@router.get("/")
async def get_item():
    return {"item": {"id": 1, "name": "Item name"}}
