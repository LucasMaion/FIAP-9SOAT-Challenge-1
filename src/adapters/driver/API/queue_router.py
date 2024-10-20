from fastapi import APIRouter

router = APIRouter(
    prefix="/queue",
    tags=["queue"],
)


@router.get("/")
async def get_item():
    return {"item": {"id": 1, "name": "Item name"}}
