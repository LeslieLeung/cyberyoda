import os

from pymongo import MongoClient

from cyberyoda.storage.base import StorageBase


class Mongo(StorageBase):
    conn: MongoClient
    db: str

    def __init__(self):
        super().__init__()
        self._connect()

    def __del__(self):
        self._close()

    def _connect(self):
        mongo_urn = os.environ["MONGODB_URN"]
        self.db = os.environ["MONGODB_DB"]
        self.conn = MongoClient(mongo_urn)

    def _close(self):
        self.conn.close()

    def save(self, userid: str, data: list) -> bool:
        tb = self.conn[self.db]["chat_history"]
        query = {"userid": userid, "is_current": True}
        update = {"$set": {"history": data}}
        rs = tb.update_one(query, update)
        return rs.modified_count > 0

    def get(self, userid: str) -> list:
        tb = self.conn[self.db]["chat_history"]
        query = {"userid": userid, "is_current": True}
        rs = tb.find_one(query)
        if rs:
            return rs["history"]
        return []

    def delete(self, userid: str) -> bool:
        tb = self.conn[self.db]["chat_history"]
        query = {"userid": userid, "is_current": True}
        update = {"$set": {"is_current": False}}
        rs = tb.update_one(query, update)
        return rs.modified_count > 0

    def create(self, userid: str) -> bool:
        tb = self.conn[self.db]["chat_history"]
        query = {"userid": userid, "is_current": True}
        rs = tb.find_one(query)
        if rs:
            return False
        rs = tb.insert_one({"userid": userid, "is_current": True, "history": {}})
        return rs.inserted_id is not None
