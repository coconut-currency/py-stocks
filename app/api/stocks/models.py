from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class Stocks(BaseModel):
    symbol: str
    name: str
    currentPrice: Optional[Decimal] = None
    previousClose: Optional[Decimal] = None
    dayHigh: Optional[Decimal] = None
    dayLow: Optional[Decimal] = None
    volume: Optional[int] = None
    lastUpdated: Optional[str] = None
