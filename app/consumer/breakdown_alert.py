import json

from app.model import CurrentTrade


class PriceRangeBreakTimeAlertingConsumer:
    """ 실시간 가격 정보에서, 특정 가격 정보 단위로 붕괴(폭등/폭락)이 일어났을 때를 감지
    """

    def __init__(self, price_unit=100000):
        self.price_unit = price_unit
        self.prev_price = None

    def __call__(self, message: bytes):
        # (1) bytes -> dict
        value = json.loads(message)
        # (2) dict -> domain object : 이 과정에서 validation이 진행
        trade = CurrentTrade(**value)

        # (3) 현재 가격 가져오기
        curr_price = trade.trade_price

        if self.prev_price is None:
            self.prev_price = trade.trade_price
            return

        # (4) 붕괴 여부 확인하기
        if self.prev_price // self.price_unit != curr_price // self.price_unit:
            # 이전 가격과 현재 가격이 동일한 가격 상에 존재하지 않으면, 붕괴되었다고 봄

            # 붕괴 방향
            if self.prev_price < trade.trade_price:
                direction = "상승"
            else:
                direction = "하락"

            # 붕괴 가격대
            price_range = (curr_price // self.price_unit) * self.price_unit

            # 노티하기
            print(f"[{int(price_range)}원대|{direction}] 현재 가격 : {curr_price:.1f}원 ")

        # (5) 이전 가격 저장
        self.prev_price = curr_price
