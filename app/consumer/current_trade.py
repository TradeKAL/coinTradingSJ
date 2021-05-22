import json

from app.model import CurrentTrade
from app.repository import CurrentTradeRepository


class CurrentTradeConsumer:
    def __init__(self, repository: CurrentTradeRepository):
        self.repository = repository

    def __call__(self, message: bytes):
        value = json.loads(message)
        trade = CurrentTrade(**value)
        self.repository.write(trade)
