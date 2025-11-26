from pydantic import BaseModel, Field
from typing import Optional


class Product(BaseModel):
    id: int = Field(..., description="The unique identifier for the product")
    name: str = Field(..., description="The name of the product")
    description: Optional[str] = Field(None, description="A brief description of the product")
    price: float = Field(..., gt=0, description="The price of the product, must be greater than zero")
    in_stock: bool = Field(..., description="Availability status of the product")
    category: Optional[str] = Field(None, description="The category to which the product belongs")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Customer rating of the product, between 0 and 5")