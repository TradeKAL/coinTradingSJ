import json

from app.model import CurrentTrade
from app.repository import CurrentTradeRepository


class CurrentTradeWriteConsumer:
    """ 실시간 정보를 repository에 저장하는 consumer 클래스
    """

    def __init__(self, repository: CurrentTradeRepository):
        self.repository = repository

    def __call__(self, message: bytes):
        # (1) bytes -> dict
        value = json.loads(message)
        # (2) dict -> domain object : 이 과정에서 validation이 진행
        trade = CurrentTrade(**value)
        # (3) domain object save
        self.repository.write(trade)
