import time
from unittest import TestCase

import pika

from app.publisher import RabbitMQPublisher


class TestRabbitMQPublisher(TestCase):
    def test_publish(self):
        exchange_name = "hello"
        message = b"hello"

        # 메시지를 받을 queue를_생성한다
        channel = self.get_channel(exchange_name)
        queue_name = self.create_queue(channel)

        # RabbitMQ에 퍼블리싱한다
        publisher = RabbitMQPublisher(exchange_name)
        publisher.publish(message)

        # 0.001초를 기다려서, rabbitMQ가 메시지를 받을때까지 기다려준다
        time.sleep(0.001)

        # 큐에서 메시지를 가져온다
        _, _, response = channel.basic_get(queue_name)
        self.assertEqual(message, response)

    def get_channel(self, exchange_name):
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()
        result = channel.queue_declare(queue="", exclusive=True)
        channel.queue_bind(exchange="hello", queue=result.method.queue)
        return channel

    def create_queue(self, channel):
        result = channel.queue_declare(queue="", exclusive=True)
        channel.queue_bind(exchange="hello", queue=result.method.queue)
        return result.method.queue
