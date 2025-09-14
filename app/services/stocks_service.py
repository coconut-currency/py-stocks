from datetime import datetime, timezone

import yfinance as yf


def test_services(symbol: str):
    ticker = yf.Ticker(symbol)
    info = ticker.fast_info

    stock_data = {
        "symbol": symbol,
        "name": ticker.get_info().get("longName") or ticker.get_info().get("shortName"),
        "currentPrice": info.get("lastPrice"),
        "previousClose": info.get("previousClose"),
        "dayHigh": info.get("dayHigh"),
        "dayLow": info.get("dayLow"),
        "volume": info.get("volume"),
        "lastUpdated": datetime.now(timezone.utc).isoformat(),
    }

    return stock_data
