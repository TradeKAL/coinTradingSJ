from pydantic import BaseModel, Field


class UpbitTrade(BaseModel):
    """ 실시간 체결(Trade) 응답 모델
    reference : https://docs.upbit.com/docs/upbit-quotation-websocket
    """
    type: str = Field(description="타입(ticker)")
    code: str = Field(description="마켓코드(ex.KRW-BTC)")
    timestamp: int = Field(description="타임스탬프(milliseconds)")

    trade_date: str = Field(description="최근 거래 일자(yyyyMMdd)")
    trade_time: str = Field(description="최근 거래 시각(HHmmss)")
    trade_timestamp: int = Field(description="체결 타임스탬프(milliseconds)")
    trade_price: float = Field(description="현재가")
    trade_volume: float = Field(description="가장 최근 거래량")
    ask_bid: str = Field(description="매수/매도 구분(ASK : 매도 BID : 매수)")
    prev_closing_price: float = Field(description="전일 종가")
    change: str = Field(description="전일 대(RISE : 상승, EVEN : 보합, FALL : 하락)")
    change_price: float = Field(description="부호 없는 전일 대비값")
    sequential_id: int = Field(description="체결 번호 (Unique)")
    stream_type: str = Field(description="스트림 타입(SNAPSHOT : 스냅샵, REALTIME: 실시간)")
