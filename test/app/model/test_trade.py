import json
from unittest import TestCase

from app.model import UpbitTrade


class TestUpbitTicker(TestCase):
    def test_parsing(self):
        """실패하면 ValidationError 반환"""
        data = '{"type":"trade","code":"KRW-BTC","timestamp":1621697844865,"trade_date":"2021-05-22","trade_time":"15:37:24","trade_timestamp":1621697844000,"trade_price":46769000.0,"trade_volume":0.00185096,"ask_bid":"BID","prev_closing_price":49112000.00000000,"change":"FALL","change_price":2343000.00000000,"sequential_id":1621697844000001,"stream_type":"REALTIME"}'

        UpbitTrade(**json.loads(data))
