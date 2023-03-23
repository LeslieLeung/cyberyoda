import os

from pymongo import MongoClient

from cyberyoda.bot.preference.base import Preference


class MongoPreference(Preference):
    client: MongoClient
    db: str

    def __init__(self, user_id):
        super().__init__(user_id)
        mongo_urn = os.environ["MONGODB_URN"]
        self.db = os.environ["MONGODB_DB"]
        self.client = MongoClient(mongo_urn)

    def __del__(self):
        self.client.close()

    def load(self):
        tb = self.client[self.db]["user_preference"]
        query = {"userid": self.user_id}
        rs = tb.find_one(query)
        if rs:
            self.temperature = rs["temperature"]
        else:
            self.temperature = 0.9

    def save(self):
        tb = self.client[self.db]["user_preference"]
        query = {"userid": self.user_id}
        update = {"$set": {"temperature": self.temperature}}
        rs = tb.update_one(query, update)
        if rs.modified_count > 0:
            return True
        rs = tb.insert_one(
            {"userid": self.user_id, "temperature": self.temperature}
        )
        return rs.inserted_id is not None
