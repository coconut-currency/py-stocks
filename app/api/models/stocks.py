from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, HttpUrl


class Stocks(BaseModel):
    symbol: str
    name: str
    currentPrice: Optional[Decimal] = None
    previousClose: Optional[Decimal] = None
    dayHigh: Optional[Decimal] = None
    dayLow: Optional[Decimal] = None
    volume: Optional[int] = None
    lastUpdated: Optional[str] = None


class News(BaseModel):
    id: str
    title: str
    summary: Optional[str] = None
    published_date: datetime
    provider: str
    url: HttpUrl
    content_type: str
