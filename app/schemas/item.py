from typing import Optional, List

from pydantic import BaseModel


class ItemBase(BaseModel):
    """Shared properties."""

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
    """Properties shared by models stored in DB."""

    id: int


class ItemCreate(ItemBase):
    """Properties to receive on item update."""

    name: str
    brand_name: str
    regular_price_value: float
    offer_price_value: float
    currency: str
    image_url: str


class ItemUpdate(ItemBase):
    """Properties to receive on item update."""

    pass


class UniqueBrands(BaseModel):
    """Properties to get unique brands in the database."""

    count_unique_brands: int
    unique_brands: List[str]


class CountOfferPrice(BaseModel):
    """Properties to count offer price."""

    count: int


class Discount(BaseModel):
    """Single dicount entry."""

    name: str
    brand_name: str
    discount_percentage: int


class DiscountPercentage(BaseModel):
    """Properties for DiscountPercentage."""

    count: int
    items: List[Discount]
