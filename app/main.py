from fastapi import FastAPI

from app.api.stocks.routes import router as stocks_router

app = FastAPI(
    title="Next Stocks API",
    description="A sample stocks API",
    version="1.0.0",
)

app.include_router(stocks_router, prefix="/stocks", tags=["Stocks"])


@app.get("/")
def index():
    return {"data": {"Message": "Welcome to stocks API"}}
