import logging

from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from app.crud.item import Item

LOGGER = logging.getLogger()
cliff_route = APIRouter()


@cliff_route.get("/login")
async def read_items():
    items = await Item.get_all()
    if not items:
        raise HTTPException(status_code=404, detail="No items found")
    return items
