import json
import uuid

import websockets
from websocket import WebSocket
from websocket import create_connection


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
