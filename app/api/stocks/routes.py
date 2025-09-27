from fastapi import APIRouter, HTTPException

from app.api.models.stocks import Stocks
from app.services.stocks_service import get_global_indices, get_stock_data

router = APIRouter()


@router.get("/global")
def get_global_stocks():
    return get_global_indices()


@router.get("/{symbol}", response_model=Stocks)
def get_stocks_data(symbol: str):
    result = get_stock_data(symbol)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
