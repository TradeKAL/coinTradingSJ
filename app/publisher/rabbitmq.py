import pika
from pika import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel
from pika.exchange_type import ExchangeType


class RabbitMQPublisher:
    """ RabbitMQ 메시지큐에 publishing하는 클래스
    """
    connection: BlockingConnection = None
    channel: BlockingChannel = None

    def __init__(self,
                 exchange_name,
                 exchange_type=ExchangeType.fanout,
                 routing_key="",
                 host="localhost",
                 port=5672):
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self.routing_key = routing_key
        self.host = host
        self.port = port

    def publish(self, message: bytes):
        if self.channel is None or self.channel.is_closed:
            self._open_channel()
        self.channel.basic_publish(self.exchange_name, self.routing_key, body=message)

    def _open_channel(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host, self.port))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(self.exchange_name, self.exchange_type)
