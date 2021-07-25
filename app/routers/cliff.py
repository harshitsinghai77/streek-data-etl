import logging
from typing import List

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

from app.crud.item import Item
from app.schemas.item import (
    GetCount,
    DiscountPercentage,
    ItemCreate,
    ItemRead,
    ItemUpdate,
    ItemDelete,
    UniqueBrands,
)

LOGGER = logging.getLogger()
cliff_router = APIRouter()


@cliff_router.get("/items", response_model=List[ItemRead])
async def read_item(skip: int = 0, limit: int = 100):
    """Read all items in the database."""
    items = await Item.get(limit=limit, skip=skip)
    if not items:
        raise HTTPException(status_code=404, detail="No items found")
    return items


@cliff_router.get("/item/{item_id}", response_model=ItemRead)
async def read_item_by_id(item_id: int):
    """Read item by id."""
    items = await Item.get_item_by_id(id=item_id)
    if not items:
        raise HTTPException(status_code=404, detail=f"No item found with id {item_id}")
    return items


@cliff_router.get("/item/brand/{brand_name}", response_model=List[ItemRead])
async def read_item_by_brand_name(brand_name: str):
    """Get all items with the given brand_name."""
    brand_item = await Item.get_item_by_brand_name(brand_name=brand_name)
    if not brand_item:
        raise HTTPException(
            status_code=404, detail=f"No item found with brand_name {brand_name}"
        )
    return brand_item


@cliff_router.post("/item", response_model=ItemRead)
async def create_item(item_in: ItemCreate):
    """Create new item."""
    item_in = jsonable_encoder(item_in)
    item = await Item.create(item_in)
    return item


@cliff_router.patch("/item/{id}")
async def update_item(id: int, updated_item: ItemUpdate):
    """Update the item by id."""
    item = await Item.get_item_by_id(id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item = updated_item.dict(exclude_unset=True)
    if not updated_item:
        raise HTTPException(
            status_code=404, detail="Empty body. Cannot update the item."
        )
    item = await Item.update(id=id, item_obj=updated_item)
    return item


@cliff_router.delete("/item/{id}", response_model=ItemDelete)
async def delete_item(id: int):
    """Delete a item by id."""
    item = await Item.get_item_by_id(id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    query_id = await Item.remove(id=id)
    return {"success": True, "id": query_id}


@cliff_router.get("/count_discounted_products", response_model=GetCount)
async def count_discounted_products():
    """Number of items having a discount."""
    items_count = await Item.count_discounted_products()
    if not items_count:
        raise HTTPException(status_code=404, detail="No such items found.")
    return {"count": items_count}


@cliff_router.get("/list_unique_brands", response_model=UniqueBrands)
async def list_unique_brands():
    """List of unique brands in the database."""
    unique_brands = await Item.get_unique_brands()
    if not unique_brands:
        raise HTTPException(status_code=404, detail="No unique brands found.")

    unique_brands_lst = [brand["brand_name"] for brand in unique_brands]
    return {
        "count_unique_brands": len(unique_brands_lst),
        "unique_brands": unique_brands_lst,
    }


@cliff_router.get("/count_high_offer_price", response_model=GetCount)
async def count_high_offer_price(greater_than: int = 300):
    """Items with offer_price greater than a given value."""
    items_count = await Item.count_offer_price_greater_than(value=greater_than)
    if not items_count:
        raise HTTPException(status_code=404, detail="No such items found.")
    return {"count": items_count}


@cliff_router.get("/count_high_discount", response_model=DiscountPercentage)
async def count_high_discount(greater_than: int = 30):
    """Items with discount % greater than a given value."""
    discount_percentage = await Item.calculate_discount_percentage(value=greater_than)
    if not discount_percentage:
        raise HTTPException(status_code=404, detail="No such items found.")
    return {"count": len(discount_percentage), "items": discount_percentage}
