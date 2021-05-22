from unittest import TestCase

from app.model import CurrentTrade
from app.repository import CurrentTradeRepository


class TestCurrentTradeRepository(TestCase):
    repository: CurrentTradeRepository

    def setUp(self) -> None:
        self.repository = CurrentTradeRepository()

    def test_write_and_read(self):
        trade = CurrentTrade(code="KRW-BTC",
                             trade_timestamp=1234,
                             trade_price=1000.,
                             trade_volume=1000.)

        self.repository.write(trade)

        result = self.repository.read("KRW-BTC")

        self.assertEqual(trade, result)

        self.repository.clear_all()
