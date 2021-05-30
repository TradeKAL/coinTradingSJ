import json
import time
import uuid
from datetime import datetime, timedelta
from typing import List

import pytz
import requests
import websockets
from websocket import WebSocket
from websocket import create_connection

from app.model.current_trade import SnapShotTrade


class UpbitRealTimeTradeSubscriber:
    """ upbit 서버에 실시간 체결 거래를 가져오는 클래스
    동기/비동기 방식 모두 지원

    1. 동기 메서드 호출 방식 (.subscribe())
        ````python
        subscriber = UpbitRealTimeTradeSubscriber("trade", isOnlyRealtime=True)
        print(subscriber.subscribe())
        ````
    2. 동기 제너레이터 호출 방식 (for ... in ...)
        ````python
        subscriber = UpbitRealTimeTradeSubscriber("trade", isOnlyRealtime=True)
        for message in subscriber:
            print(message)
            break
        ````

    3. 비동기 방식
        ````python
        import asyncio

        async def run():
            subscriber = UpbitRealTimeTradeSubscriber("trade", isOnlyRealtime=True)
            async for response in subscriber:
               print(response)

        if __name__ == '__main__':
            loop = asyncio.get_event_loop()
            loop.run_until_complete(run())
            loop.close()
        ````
    """

    WSS_URI = "wss://api.upbit.com/websocket/v1"
    ws: WebSocket = None

    def __init__(self,
                 type_="ticker",
                 codes=["KRW-BTC"],
                 isOnlySnapshot=False,
                 isOnlyRealtime=False
                 ):
        """

        :param type_: 수신할 시세 타입. (현재가: ticker, 체결: trade, 호가: orderbook)
        :param codes: 수신할 시세 종목 정보 (codes 필드에 명시되는 종목들은 대문자로 요청)
        :param isOnlySnapshot: 시세 스냅샷만 제공
        :param isOnlyRealtime: 실시간 시세만 제공
        """
        self.type = type_
        self.codes = codes
        self.isOnlyRealtime = isOnlyRealtime
        self.isOnlySnapshot = isOnlySnapshot

        self._request = self._create_request()

    def __iter__(self):
        self._initialize()
        return self

    def __next__(self):
        self.ws.send(self._request)
        return self.ws.recv()

    async def __aiter__(self):
        async with websockets.connect(self.WSS_URI) as ws:
            while True:
                await ws.send(self._request)
                response = await ws.recv()
                yield response

    def subscribe(self):
        self._initialize()
        return next(self)

    def _initialize(self):
        if self.ws is None:
            self.ws = create_connection(self.WSS_URI)

    def _create_request(self) -> str:
        return json.dumps([
            {"ticket": str(uuid.uuid4())[:5]},
            {
                "type": self.type,
                "codes": self.codes,
                "isOnlyRealtime": self.isOnlyRealtime,
                "isOnlySnapshot": self.isOnlySnapshot
            }
        ])


class UpbitSnapshotTradeFinder:
    """ upbit 서버에 현재 시각 기준 스냅샷 결제 정보를 가져오는 클래스
    """
    CANDLE_URL = "https://api.upbit.com/v1/candles/minutes/{}"

    def __init__(self, unit=1, code="KRW-BTC"):
        """
        :param unit: 분 간격 (1, 3, 5, 10, 30, 60)
        :param codes: 수신할 시세 종목 정보 (codes 필드에 명시되는 종목들은 대문자로 요청)
        """
        self.unit = unit
        self.code = code

    def find(self, count) -> List[SnapShotTrade]:
        """ 현재 시각 기준으로 count만큼의 스냅샷 정보를 가져오는 함수

        :param count:
        :return:
        """
        candle = self._get_latest_candle()
        if count == 1:
            return [candle]

        result = []
        to = datetime.now(pytz.timezone("Asia/Seoul"))
        for _ in range(0, count, 200):
            # upbit에서는 최대 한번에 200개의 row만 제공하고 있으므로, 200건씩 나누어서 호출해야 함
            result.extend(sorted(self._get(count, to), key=lambda x: x.candle_date_time_kst, reverse=True))
            kst = pytz.timezone("Asia/Seoul")
            # 약간의 시간 차이를 빼내어서 경계시간에 대한 값이 포함되지 않도록 함
            to = kst.localize(result[-1].candle_date_time_kst) - timedelta(microseconds=1)
        return result[:count]

    def _get(self, count: int, dt: datetime) -> List[SnapShotTrade]:
        """ 업비트의 candle 정보를 요청하여 가져오기

        :param count: 갯수
        :param dt: 시각
        :return:
        """
        response = requests.get(self.CANDLE_URL.format(self.unit),
                                params={"market": self.code,
                                        "count": count,
                                        "to": dt.strftime("%Y-%m-%dT%H:%M:%S") + "+09:00"})
        return [SnapShotTrade(**row) for row in json.loads(response.content)]

    def _get_latest_candle(self) -> SnapShotTrade:
        """ 업비트의 candle 정보가 현재 시점 기준으로 업데이트되었는지를 확인
        :return:
        """
        candle = self._get(1, datetime.now(pytz.timezone("Asia/Seoul")))[0]
        while not candle.is_recent():
            time.sleep(.1)
            candle = self._get(1, datetime.now(pytz.timezone("Asia/Seoul")))[0]
        return candle
