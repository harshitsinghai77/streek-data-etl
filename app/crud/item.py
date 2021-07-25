from typing import Dict

from app.config.database import database
from app.models.item import item
from sqlalchemy import select


class Item:
    """Utility class to do CRUD operations on item."""

    @staticmethod
    async def get(skip: int = 0, limit: int = 100):
        """Get all items from the database."""
        query = item.select().offset(skip).limit(limit)
        result = await database.fetch_all(query=query)
        return result

    @staticmethod
    async def get_item_by_id(id: int):
        """Get item by id."""
        query = item.select().where(item.c.id == id)
        result = await database.fetch_one(query=query)
        return result

    @staticmethod
    async def get_item_by_brand_name(brand_name: str):
        """Get item by brand name."""
        query = item.select().where(item.c.brand_name == brand_name)
        result = await database.fetch_all(query=query)
        return result

    @staticmethod
    async def create(item_dict):
        """Create new item."""
        query = item.insert().values(**item_dict)
        last_record = await database.execute(query)
        return {"id": last_record, **item_dict}

    @staticmethod
    async def update(id: str, item_obj: Dict):
        """Update an item."""
        query = item.update().where(item.c.id == id).values(**item_obj)
        await database.execute(query)
        return item_obj

    @staticmethod
    async def remove(id: int):
        """Delete an item."""
        query = item.delete().where(item.c.id == id).returning(item.c.id)
        query_id = await database.execute(query)
        return query_id

    @staticmethod
    async def get_unique_brands():
        """Get unique brands in the database."""
        query = select([item.c.brand_name], distinct=True)
        results = await database.fetch_all(query)
        return results
