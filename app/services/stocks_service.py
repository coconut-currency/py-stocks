import logging
import warnings
from datetime import datetime, timezone

import pandas as pd
import yfinance as yf

from app.api.models.stocks import News, Stocks

logger = logging.getLogger(__name__)


def get_stock_data(symbol: str) -> Stocks:
    try:
        # Add timeout and retry logic
        ticker = yf.Ticker(symbol, session=None)

        # Use fast_info first (faster, less likely to timeout)
        info = ticker.fast_info

        if not info or not info.get("lastPrice"):
            raise ValueError("No price data available")

        # Get name from fast_info if available, fallback to info
        name = (
            info.get("longName")
            or info.get("shortName")
            or ticker.info.get("longName")
            or ticker.info.get("shortName")
            or symbol.upper()
        )

        stock = Stocks(
            symbol=symbol.upper(),
            name=name,
            currentPrice=info.get("lastPrice"),
            previousClose=info.get("previousClose"),
            dayHigh=info.get("dayHigh"),
            dayLow=info.get("dayLow"),
            volume=info.get("volume"),
            lastUpdated=datetime.now(timezone.utc).isoformat(),
        )

        return stock

    except Exception as e:
        logger.error(f"Failed to fetch {symbol}: {str(e)}")
        return Stocks(
            symbol=symbol.upper(),
            name="Unknown",
        )


def get_stock_news(symbol: str) -> list[News]:
    try:
        ticker = yf.Ticker(symbol)
        news = ticker.news

        news_data: list[News] = []
        if news:
            for item in news:
                content = item.get("content", {})
                news_item = News(
                    id=content.get("id", ""),
                    title=content.get("title", ""),
                    summary=content.get("summary"),
                    published_date=content.get("pubDate"),
                    provider=content.get("provider", {}).get("displayName", ""),
                    url=content.get("clickThroughUrl", {}).get("url", ""),
                    content_type=content.get("contentType", ""),
                )
                news_data.append(news_item)
        return news_data
    except Exception as e:
        print(f"Error fetching news for {symbol}: {e}")
        return []


def get_global_indices():
    """Fetch latest data for top 5 global stock market indices"""
    indices = {
        "S&P 500": "^GSPC",
        "NASDAQ": "^IXIC",
        "Dow Jones": "^DJI",
        "FTSE 100": "^FTSE",
        "Nikkei 225": "^N225",
    }

    try:
        data_frames = []

        for name, symbol in indices.items():
            df = yf.download(symbol, period="2d", progress=False)

            if df.empty:
                continue  # Skip if no data returned

            # Remove multilevel column headers
            if df.columns.nlevels > 1:
                df.columns = df.columns.get_level_values(0)

            df = df.reset_index()
            df.insert(0, "Index", name)
            df.insert(1, "Symbol", symbol)
            df["Change_%"] = df["Close"].pct_change() * 100

            data_frames.append(df)

        if not data_frames:
            return {"error": "No data available"}

        combined_df = pd.concat(data_frames, ignore_index=True)
        combined_df = combined_df.dropna(subset=["Change_%"])
        combined_df = combined_df.drop(columns=["High", "Low", "Volume"])

        # Convert datetime to string for JSON serialization
        combined_df["Date"] = combined_df["Date"].dt.strftime("%Y-%m-%d")

        return combined_df.to_dict("records")

    except Exception as e:
        return {"error": f"Failed to fetch market data: {str(e)}"}
