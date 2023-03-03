from typing import Any


class StorageBase:
    conn: Any

    def __init__(self):
        self.conn = self._connect()

    def __del__(self):
        self._close()

    def _connect(self):
        raise NotImplementedError

    def _close(self):
        raise NotImplementedError

    def save(self, userid: str, data: list) -> bool:
        raise NotImplementedError

    def get(self, userid: str) -> list:
        raise NotImplementedError

    def delete(self, userid: str) -> bool:
        raise NotImplementedError

    def create(self, userid: str) -> bool:
        raise NotImplementedError
