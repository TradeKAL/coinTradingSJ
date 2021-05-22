import asyncio
import json
from unittest import TestCase

from app.exchange import UpbitRealTimeTradeSubscriber


class TestUpbitRealTimeTradeSubscriber(TestCase):
    subscriber = None

    def test_subscribe_method(self):
        subscriber = UpbitRealTimeTradeSubscriber("trade", isOnlyRealtime=True)

        message = subscriber.subscribe()

        self.assertIsInstance(message, bytes)
        self.assertContentsOfResponse(message)

    def test_sync_generator(self):
        subscriber = UpbitRealTimeTradeSubscriber("trade", isOnlyRealtime=True)

        for message in subscriber:
            self.assertIsInstance(message, bytes)
            self.assertContentsOfResponse(message)
            break

    def test_async_generator(self):
        asyncio.get_event_loop().run_until_complete(self.async_loop())

    async def async_loop(self):
        subscriber = UpbitRealTimeTradeSubscriber("trade", isOnlyRealtime=True)

        async for message in subscriber:
            self.assertIsInstance(message, bytes)
            self.assertContentsOfResponse(message)
            break

    def assertContentsOfResponse(self, message):
        response = json.loads(message)
        self.assertIn("type", response)
        self.assertIn("code", response)
        self.assertIn("timestamp", response)
        self.assertIn("trade_price", response)
        self.assertIn("trade_volume", response)
