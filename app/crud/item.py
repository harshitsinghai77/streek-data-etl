from app.config.database import database
from app.models.item import item


class Item:
    """Utility class to do CRUD operations on item."""

    @staticmethod
    async def get_all():
        """Get all items from the database."""
        query = item.select()
        return await database.fetch_all(query=query)
