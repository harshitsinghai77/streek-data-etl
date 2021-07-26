from sqlalchemy import select, func

from app.config.database import database
from app.models.item import item


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
    async def update(id: int, item_obj):
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
    async def count_discounted_products():
        "Count items having a discount on them."
        dicount_amount = item.c.regular_price_value - item.c.offer_price_value
        query = select([func.count()]).where(dicount_amount > 0)
        count = await database.execute(query)
        return count

    @staticmethod
    async def get_unique_brands():
        """Get unique brands in the database."""
        query = select([item.c.brand_name], distinct=True)
        results = await database.fetch_all(query)
        return results

    @staticmethod
    async def count_offer_price_greater_than(value: int = 300):
        """No. of items with offer_price greater than a given value."""
        query = select([func.count()]).where(item.c.offer_price_value > value)
        results = await database.execute(query)
        return results

    @staticmethod
    async def calculate_discount_percentage(value: int = 30):
        """
        Items with discount % greater than a given value.
        To calculate the discount percentage following approach is used:
        1. Subtract the regular_price_value from offer_price_value.
        2. Divide this new number by the regular_price_value.
        3. Multiply the resultant number by 100.
        """
        percentage_query = item.c.regular_price_value - item.c.offer_price_value
        percentage_query = (percentage_query / item.c.regular_price_value) * 100
        percentage_query = percentage_query.label("discount_percentage")

        query = select([item.c.name, item.c.brand_name, percentage_query]).where(
            percentage_query > value
        )
        results = await database.fetch_all(query)
        return results
