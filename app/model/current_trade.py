from pydantic import BaseModel, Field


class CurrentTrade(BaseModel):
    code: str = Field(description="마켓코드(ex.KRW-BTC)")

    trade_timestamp: int = Field(description="체결 타임스탬프(milliseconds)")
    trade_price: float = Field(description="최근 거래가")
    trade_volume: float = Field(description="최근 거래량")
