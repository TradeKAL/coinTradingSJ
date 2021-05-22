from unittest import TestCase

from app.consumer.factory import RabbitMQConsumerConnector
from app.publisher import RabbitMQPublisher


class TestRabbitMQConsumerFactory(TestCase):
    def test_consumer_factory(self):
        """항상 TestException을 반환하는 콜백을 등록하고, 정상적으로 콜백이 호출되었다면 TestException이 raise될 것이고, message을 반환할것"""
        exchange_name = "helloWorld"
        message = b"hello"

        publisher = RabbitMQPublisher(exchange_name)
        consumer = RabbitMQConsumerConnector(callback_exception, exchange_name)

        # publish에 message를 퍼블리싱해둔 상태
        publisher.publish(message)

        with self.assertRaises(TestException) as cm:
            consumer.start()
        self.assertEqual(message, cm.exception.message)


def callback_exception(message):
    """ 항상 Exception을 반환하는 테스트 코드"""
    raise TestException(message)


class TestException(Exception):
    message = ""

    def __init__(self, message):
        self.message = message
        super().__init__()
