from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta

class DateRange(BaseModel):
    date_from: datetime
    date_to: Optional[datetime] = None

class ItemCreate(BaseModel):
    user_id: str
    keywords: List[str]
    description: str
    image: Optional[str] = None
    lat: float
    lon: float

class Item(ItemCreate, DateRange):
    id: str