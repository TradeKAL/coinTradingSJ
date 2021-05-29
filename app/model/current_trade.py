from datetime import datetime, timedelta

import pytz
from pydantic import BaseModel, Field


class CurrentTrade(BaseModel):
    code: str = Field(description="마켓코드(ex.KRW-BTC)")

    trade_timestamp: int = Field(description="체결 타임스탬프(milliseconds)")
    trade_price: float = Field(description="최근 거래가")
    trade_volume: float = Field(description="최근 거래량")


class SnapShotTrade(BaseModel):
    market: str = Field(description="마켓코드(ex.KRW-BTC)")
    unit: int = Field(description="캔들 시각 단위")

    candle_date_time_utc: datetime = Field(description='캔들 생성 시각(UTC)')
    candle_date_time_kst: datetime = Field(description='캔들 생성 시각(KST)')
    candle_acc_trade_price: float = Field(description="누적 거래 가격")
    candle_acc_trade_volume: float = Field(description="누적 거래 량")

    opening_price: float = Field(description="시작가")
    high_price: float = Field(description="고가")
    low_price: float = Field(description="저가")
    trade_price: float = Field(description="거래가")

    def is_recent(self):
        """ 해당 정보가 현재 시각 기준으로 최신인지 평가
        """
        kst = pytz.timezone("Asia/Seoul")
        margin = datetime.now(kst) - timedelta(minutes=self.unit)
        return kst.localize(self.candle_date_time_kst) > margin
