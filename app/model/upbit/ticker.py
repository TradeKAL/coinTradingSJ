from pydantic import BaseModel, Field


class UpbitTicker(BaseModel):
    """ 실시간 체결(Ticker) 응답 모델
    reference : https://docs.upbit.com/docs/upbit-quotation-websocket
    """
    type: str = Field(description="타입(ticker)")
    code: str = Field(description="마켓코드(ex.KRW-BTC)")
    opening_price: float = Field(description="시가")
    high_price: float = Field(description="고가")
    low_price: float = Field(description="저가")
    trade_price: float = Field(description="현재가")
    prev_closing_price: float = Field(description="전일 종가")
    change: str = Field(description="전일 대비 (RISE : 상승, EVEN : 보합, FALL : 하락)")

    change_price: float = Field(description="부호 없는 전일 대비값")
    signed_change_price: float = Field(description="전일 대비 값")
    change_rate: float = Field(description="부호 없는 전일 대비 등락율")
    signed_change_rate: float = Field(description="전일 대비 등락율")

    trade_volume: float = Field(description="가장 최근 거래량")

    acc_trade_volume: float = Field(description="누적 거래량(UTC 0시 기준)")
    acc_trade_volume_24h: float = Field(description="24시간 누적 거래량")
    acc_trade_price: float = Field(description="누적 거래대금(UTC 0시 기준)")
    acc_trade_price_24h: float = Field(description="24시간 누적 거래대금")

    trade_date: str = Field(description="최근 거래 일자(yyyyMMdd)")
    trade_time: str = Field(description="최근 거래 시각(HHmmss)")
    trade_timestamp: int = Field(description="체결 타임스탬프(milliseconds)")

    ask_bid: str = Field(description="매수/매도 구분(ASK : 매도 BID : 매수)")

    acc_ask_volume: float = Field(description="누적 매도량")
    acc_bid_volume: float = Field(description="누적 매수량")

    highest_52_week_price: float = Field(description="52주 최고가")
    highest_52_week_date: str = Field(description="52주 최고가 달성일")
    lowest_52_week_price: float = Field(description="52주 최저가")
    lowest_52_week_date: str = Field(description="52주 최저가 달성일")

    market_state: str = Field(description="거래상태 (PREVIEW : 입금지원, ACTIVE : 거래지원가능, DELISTED : 거래지원종료)")
    is_trading_suspended: bool = Field(description="거래 정지 여부")

    delisting_date: str = Field(None, description="상장페지일")

    market_warning: str = Field(description="유의 종목 여부(NONE: 해당 없음, CAUTION: 투자유의)")

    timestamp: int = Field(description="타임스탬프(milliseconds)")
    stream_type: str = Field(description="스트림 타입(SNAPSHOT : 스냅샵, REALTIME: 실시간)")
