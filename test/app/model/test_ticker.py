import json
from unittest import TestCase

from app.model import UpbitTicker


class TestUpbitTicker(TestCase):
    def test_parsing(self):
        """실패하면 ValidationError 반환"""
        data = '{"type":"ticker","code":"KRW-BTC","opening_price":49080000.00000000,"high_price":49260000.00000000,"low_price":43957000.0,"trade_price":46810000.0,"prev_closing_price":49112000.00000000,"acc_trade_price":660440684062.676560000,"change":"FALL","change_price":2302000.00000000,"signed_change_price":-2302000.00000000,"change_rate":0.0468724548,"signed_change_rate":-0.0468724548,"ask_bid":"BID","trade_volume":0.0047861,"acc_trade_volume":14163.64845603,"trade_date":"20210522","trade_time":"153106","trade_timestamp":1621697466000,"acc_ask_volume":7813.15032634,"acc_bid_volume":6350.49812969,"highest_52_week_price":81994000.00000000,"highest_52_week_date":"2021-04-14","lowest_52_week_price":10507000.00000000,"lowest_52_week_date":"2020-05-25","trade_status":null,"market_state":"ACTIVE","market_state_for_ios":null,"is_trading_suspended":false,"delisting_date":null,"market_warning":"NONE","timestamp":1621697466678,"acc_trade_price_24h":1016673124418.02839000,"acc_trade_volume_24h":21625.36474921,"stream_type":"REALTIME"}'

        UpbitTicker(**json.loads(data))
