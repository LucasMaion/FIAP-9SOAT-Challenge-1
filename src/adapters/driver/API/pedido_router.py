from fastapi import APIRouter

router = APIRouter(
    prefix="/pedido",
    tags=["Pedidos"],
)


# TODO: add list pedidos; get pedido; create pedido; add new selected product; add new selected product component; add conclude pedido; add cancel pedido
@router.get("/")
async def get_item():
    return {"item": {"id": 1, "name": "Item name"}}
