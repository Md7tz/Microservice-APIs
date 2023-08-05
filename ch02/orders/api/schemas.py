from enum import Enum
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, conlist, conint, validator

class Size(Enum):
    small = 'small'
    medium = 'medium'
    big = 'big'
    
class Status(Enum):
    created = 'created'
    progress = 'progress'
    cancelled = 'cancelled'
    dispatched = 'dispatched'
    delivered = 'delivered'
    
class OrderItemSchema(BaseModel):
    product: str
    size: Size
    quantity: Optional[conint(ge=1, strict=True)] = 1
    
    @validator('quantity')
    def quantity_non_nullable(cls, value):
        assert value is not None, 'quantity is required'
        return value
    
class CreateOrderSchema(BaseModel):
    order: conlist(OrderItemSchema, min_length=1)

class GetOrderSchema(BaseModel):
    id: UUID
    created: datetime
    status: Status
    
class GetOrdersSchema(BaseModel):
    orders: List[GetOrderSchema]
