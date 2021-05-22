from typing import Callable

import pika
from pika.adapters.blocking_connection import BlockingChannel


class RabbitMQConsumerConnector:
    """ RabbitMQ 메시지큐에 Callback Consumer를 연결하는 클래스
    """
    channel: BlockingChannel = None
    queue: str = None

    def __init__(self,
                 consumer: Callable[[bytes], None],
                 exchange_name: str,
                 host="localhost",
                 port=5672):
        self.exchange_name = exchange_name
        self.host = host
        self.port = port

        self._register_consumer(consumer)

    def start(self):
        self.channel.start_consuming()

    def _register_consumer(self, callback):
        self.channel = self._open_channel()
        self.queue = self._create_queue(self.channel)

        wrapped = lambda ch, method, properties, body: callback(body)
        self.channel.basic_consume(self.queue, wrapped, auto_ack=True)

    def _open_channel(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host, self.port))
        return connection.channel()

    def _create_queue(self, channel):
        result = channel.queue_declare(queue="", exclusive=True)
        channel.queue_bind(exchange=self.exchange_name, queue=result.method.queue)
        return result.method.queue
