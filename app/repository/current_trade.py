from pydantic import ValidationError
from redis import StrictRedis

from app.model import CurrentTrade


class CurrentTradeRepository:
    HEADER = "current-trade"
    VOLUME = "trade_volume"
    PRICE = "trade_price"
    TIMESTAMP = "trade_timestamp"

    def __init__(self,
                 host="localhost",
                 port=6379,
                 db=0):
        self.r = StrictRedis(host, port, db)

    def write(self, trade: CurrentTrade):
        with self.r.pipeline(transaction=True) as pipe:
            for key, value in self._to_items(trade):
                pipe.set(key, value)
            pipe.execute()

    def read(self, code: str):
        try:
            volume = float(self.r.get(f"{self.HEADER}:{code}:{self.VOLUME}"))
            price = float(self.r.get(f"{self.HEADER}:{code}:{self.PRICE}"))
            timestamp = int(self.r.get(f"{self.HEADER}:{code}:{self.TIMESTAMP}"))

            return CurrentTrade(
                code=code,
                trade_volume=volume,
                trade_price=price,
                trade_timestamp=timestamp
            )
        except ValidationError:
            # TODO LOGGING 필요
            return None

    def read_all(self):
        return [self.read(code) for code in self._all_codes()]

    def clear(self, code: str):
        self.r.delete(
            f"{self.HEADER}:{code}:{self.VOLUME}",
            f"{self.HEADER}:{code}:{self.PRICE}",
            f"{self.HEADER}:{code}:{self.TIMESTAMP}"
        )

    def clear_all(self):
        for code in self._all_codes():
            self.clear(code)

    def _to_items(self, value: CurrentTrade):
        return {
            f"{self.HEADER}:{value.code}:{self.VOLUME}": value.trade_volume,
            f"{self.HEADER}:{value.code}:{self.PRICE}": value.trade_price,
            f"{self.HEADER}:{value.code}:{self.TIMESTAMP}": value.trade_timestamp,
        }.items()

    def _all_codes(self):
        return {str(key).split(':')[1] for key in self.r.scan_iter(f"{self.HEADER}:*:*")}
