from fastapi import APIRouter, HTTPException

from app.services.stocks_service import test_services

from .models import Stocks

router = APIRouter()


@router.get("/symbol/{symbol}", response_model=Stocks)
def get_stocks_data(symbol: str):
    return test_services(symbol)
