from typing import Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    """Shared properties"""

    name: Optional[str]
    brand_name: Optional[str]
    regular_price_value: Optional[float]
    offer_price_value: Optional[float]
    currency: Optional[str]
    classification_l1: Optional[str]
    classification_l2: Optional[str]
    classification_l3: Optional[str]
    classification_l4: Optional[str]
    image_url: Optional[str]


class ItemRead(ItemBase):
    """Properties shared by models stored in DB"""

    id: int


class ItemCreate(ItemBase):
    """Properties to receive on item update"""

    name: str
    brand_name: str
    regular_price_value: float
    offer_price_value: float
    currency: str
    image_url: str


class ItemUpdate(ItemBase):
    """Properties to receive on item update"""

    pass
