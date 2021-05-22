from app.exchange import UpbitRealTimeTradeSubscriber
from app.publisher import RabbitMQPublisher

"""
업비트 서버에서 웹소켓을 통해 실시간 정보를 받아와서, RabbitMQ까지 보내는 워커 구성하는 로직

[ Upbit 서버 ] ---> [ UpbitRealTimeTradeSubscriber ] -- 메시지 전달 --> [ RabbitMQ ("<category>.<code>") ] 
"""

if __name__ == "__main__":
    category = "trade"
    code = "KRW-BTC"

    # 업비트에서 실시간 정보를 구독하는 subscriber 생성
    subscriber = UpbitRealTimeTradeSubscriber("trade", codes=[code], isOnlyRealtime=True)
    # 메시지 큐 생성
    publisher = RabbitMQPublisher(f"{category}.{code}")

    while True:
        # 구독
        message = subscriber.subscribe()
        # 발송
        publisher.publish(message)
