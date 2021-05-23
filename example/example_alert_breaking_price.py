from multiprocessing import Process

from app.consumer import PriceRangeBreakTimeAlertingConsumer
from app.consumer import RabbitMQConsumerConnector
from app.exchange import UpbitRealTimeTradeSubscriber
from app.publisher import RabbitMQPublisher


def subscribe_and_publish_worker(category="trade", code="KRW-BTC"):
    """
    업비트 서버에서 웹소켓을 통해 실시간 정보를 받아와서, RabbitMQ까지 보내는 워커
        [ Upbit 서버 ] ---> [ UpbitRealTimeTradeSubscriber ] -- 메시지 전달 --> [ RabbitMQ ("<category>.<code>") ]
    """
    # (1) 업비트에서 실시간 정보를 구독하는 subscriber 생성
    subscriber = UpbitRealTimeTradeSubscriber(category, codes=[code], isOnlyRealtime=True)

    # (2) 메시지 큐 생성
    publisher = RabbitMQPublisher(exchange_name=f"{category}.{code}")

    # (3) 구독 후 발송
    for message in subscriber:
        publisher.publish(message)


def consume_and_alert_worker(category="trade", code="KRW-BTC", price_range=100000):
    """
    rabbitMQ로부터 받은 실시간 정보 중에서 현재 정보를 파싱해서 가격대 붕괴여부를 감지하는 로직
        [ RabbitMQ ("<category>.<code>") ] --> [ PriceRangeBreakTimeAlertingConsumer ]
    """
    # (1) broker에서 현재 가격을 받아서 repository에 저장하는 consumer 구성
    consumer = PriceRangeBreakTimeAlertingConsumer(price_range)

    # (2) 브로커에 consumer를 연결한 후, 실행 ( exchange_name에 의해 연결되므로, 올바르게 설정되었는지 확인해야 함)
    RabbitMQConsumerConnector(consumer, exchange_name=f"{category}.{code}").start()


if __name__ == "__main__":
    category = "trade"
    code = "KRW-ETH"

    print("subscribe_and_publish_worker START!")
    subscriber_worker = Process(target=subscribe_and_publish_worker, args=(category, code))
    subscriber_worker.start()

    print("consume_and_write_worker START!")
    consumer_worker = Process(target=consume_and_alert_worker, args=(category, code, 10000))
    consumer_worker.start()
