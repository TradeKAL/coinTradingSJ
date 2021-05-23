from multiprocessing import Process

from app.consumer import CurrentTradeWriteConsumer
from app.consumer import RabbitMQConsumerConnector
from app.exchange import UpbitRealTimeTradeSubscriber
from app.publisher import RabbitMQPublisher
from app.repository import CurrentTradeRepository


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


def consume_and_write_worker(category="trade", code="KRW-BTC"):
    """
    rabbitMQ로부터 받은 실시간 정보 중에서 현재 정보를 파싱해서 repository에 저장하는 워커를 구성
        [ RabbitMQ ("<category>.<code>") ] --> [ CurrentTradeConsumer ]   ---> [ Repository(redis) ]
    """
    # (1) 현재 가격을 관리하는 repository 구성
    repository = CurrentTradeRepository()

    # (2) broker에서 현재 가격을 받아서 repository에 저장하는 consumer 구성
    consumer = CurrentTradeWriteConsumer(repository)

    # (3) 브로커에 consumer를 연결한 후, 실행 ( exchange_name에 의해 연결되므로, 올바르게 설정되었는지 확인해야 함)
    RabbitMQConsumerConnector(consumer, exchange_name=f"{category}.{code}").start()


def visualize_live_plot(code, interval=0.1):
    """
    repository에서 현재가격을 읽어서 실시간 움직임을 보기
        [ Repository(redis) ] --> [ monitor ]
    """

    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    import pandas as pd

    # 현재 가격을 관리하는 repository 구성
    repository = CurrentTradeRepository()

    # 현재 가격정보를 출력
    queue = list()  # 데이터를 담을 큐 생성
    while True:
        trade = repository.read(code)

        queue.append(trade.dict())
        df = pd.DataFrame(queue)
        plt.plot(df.trade_timestamp.values, df.trade_price.values, color="black")
        plt.pause(interval)
    plt.show()


if __name__ == "__main__":
    category = "trade"
    code = "KRW-ETH"

    print("subscribe_and_publish_worker START!")
    subscriber_worker = Process(target=subscribe_and_publish_worker, args=(category, code))
    subscriber_worker.start()

    print("consume_and_write_worker START!")
    consumer_worker = Process(target=consume_and_write_worker, args=(category, code))
    consumer_worker.start()

    print("RealTime Trading Visualization START!")
    try:
        visualize_live_plot(code, 0.5)
    finally:
        subscriber_worker.terminate()
        consumer_worker.terminate()
