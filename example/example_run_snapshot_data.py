from apscheduler.schedulers.blocking import BlockingScheduler

from app.exchange import UpbitSnapshotTradeSubscriber
from app.publisher import RabbitMQPublisher

scheduler = BlockingScheduler()


def subscribe_and_publish_worker(unit=1, code="KRW-BTC"):
    """
    업비트 서버에서 웹소켓을 통해 스냅샷 정보를 받아와서, RabbitMQ까지 보내는 워커
        [ Upbit 서버 ] ---> [ UpbitSnapshotTradeSubscriber ] -- 메시지 전달 --> [ RabbitMQ ("snapshot.ohlcv-{unit}.{code}") ]
    """
    # (1) 업비트에서 스냅샷 정보를 구독하는 subscriber 생성
    subscriber = UpbitSnapshotTradeSubscriber(unit, code=code)

    # (2) 메시지 큐 생성
    publisher = RabbitMQPublisher(exchange_name=f"snapshot.ohlcv-{unit}.{code}")

    # (3) 구독 후 발송
    trade = subscriber.subscribe()
    publisher.publish(trade.json())


if __name__ == "__main__":
    unit = 1
    code = 'KRW-BTC'

    scheduler.add_job(lambda: subscribe_and_publish_worker(unit, code),
                      'cron', second=0, id='snapshot-scheduler')
    scheduler.start()
