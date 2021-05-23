from app.consumer import CurrentTradeWriteConsumer
from app.consumer import RabbitMQConsumerConnector
from app.repository import CurrentTradeRepository

"""
rabbitMQ로부터 받은 실시간 정보 중에서 현재 정보를 파싱해서 repository에 저장하는 워커를 구성

[ RabbitMQ ("<category>.<code>") ] --> [ CurrentTradeConsumer ]   ---> [ Repository(redis) ] 
"""

if __name__ == "__main__":
    category = "trade"
    code = "KRW-BTC"

    # 현재 가격을 저장하는 repository 구성
    repository = CurrentTradeRepository()

    # broker에서 현재 가격을 받아서 repository에 저장하는 consumer 구성
    consumer = CurrentTradeWriteConsumer(repository)

    # 브로커에 consumer를 연결한 후, 실행
    RabbitMQConsumerConnector(consumer, exchange_name=f"{category}.{code}").start()
