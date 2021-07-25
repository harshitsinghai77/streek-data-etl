import logging
from typing import List

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder

from app.crud.item import Item
from app.schemas.item import (
    ItemUpdate,
    ItemCreate,
    ItemRead,
    UniqueBrands,
    CountOfferPrice,
    DiscountPercentage,
)

LOGGER = logging.getLogger()
cliff_router = APIRouter()


@cliff_router.get("/items", response_model=List[ItemRead])
async def read_item(skip: int = 0, limit: int = 100):
    items = await Item.get(limit=limit, skip=skip)
    if not items:
        raise HTTPException(status_code=404, detail="No items found")
    return items


@cliff_router.get("/item/{item_id}", response_model=ItemRead)
async def read_item_by_id(item_id: int):
    items = await Item.get_item_by_id(id=item_id)
    if not items:
        raise HTTPException(status_code=404, detail=f"No item found with id {item_id}")
    return items


@cliff_router.get("/item/brand/{brand_name}", response_model=List[ItemRead])
async def read_item_by_brand_name(brand_name: str):
    brand_item = await Item.get_item_by_brand_name(brand_name=brand_name)
    if not brand_item:
        raise HTTPException(
            status_code=404, detail=f"No item found with brand_name {brand_name}"
        )
    return brand_item


@cliff_router.post("/item")
async def create_item(item_in: ItemCreate):
    item_in = jsonable_encoder(item_in)
    item = await Item.create(item_in)
    return item


@cliff_router.patch("/item/{id}")
async def update_item(id: int, updated_item: ItemUpdate):
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


@cliff_router.delete("/item/{id}")
async def delete_item(id: int):
    item = await Item.get_item_by_id(id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    query_id = await Item.remove(id=id)
    if query_id:
        return {"success": True, "id": query_id}
    return {"success": False}


@cliff_router.get("/count_discounted_products")
async def count_discounted_products():
    items_count = await Item.count_discounted_products()
    if not items_count:
        raise HTTPException(status_code=404, detail="No such items found.")
    return {"count": items_count}


@cliff_router.get("/list_unique_brands", response_model=UniqueBrands)
async def list_unique_brands():
    unique_brands = await Item.get_unique_brands()
    if not unique_brands:
        raise HTTPException(status_code=404, detail="No unique brands found.")

    unique_brands_lst = [brand["brand_name"] for brand in unique_brands]
    return {
        "count_unique_brands": len(unique_brands_lst),
        "unique_brands": unique_brands_lst,
    }


@cliff_router.get("/count_high_offer_price", response_model=CountOfferPrice)
async def count_high_offer_price(greater_than: int = 300):
    items_count = await Item.count_offer_price_greater_than(value=greater_than)
    if not items_count:
        raise HTTPException(status_code=404, detail="No such items found.")
    return {"count": items_count}


@cliff_router.get("/count_high_discount", response_model=DiscountPercentage)
async def count_high_discount(greater_than: int = 30):
    discount_percentage = await Item.calculate_discount_percentage(value=greater_than)
    if not discount_percentage:
        raise HTTPException(status_code=404, detail="No such items found.")
    return {"count": len(discount_percentage), "items": discount_percentage}
