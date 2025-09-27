from fastapi import APIRouter, HTTPException

from app.api.models.stocks import News
from app.services.stocks_service import get_stock_news

router = APIRouter()


@router.get("/{symbol}", response_model=list[News])
def get_stocks_news(symbol: str):
    result = get_stock_news(symbol)
    if not result:
        raise HTTPException(status_code=404, detail="No news found")
    return result
