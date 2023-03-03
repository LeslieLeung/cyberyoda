from cyberyoda.storage.base import StorageBase


class ChatHistory:
    history: list
    storage: StorageBase
    userid: str

    def __init__(self, storage: StorageBase, userid: str):
        self.storage = storage
        self.userid = userid
        self.load()

    def load(self):
        self.history = self.storage.get(self.userid)
        if not self.history:
            self.history = []

    def save(self):
        h = self.storage.get(self.userid)
        if not h:
            self.storage.create(self.userid)
        self.storage.save(self.userid, self.history)

    def reset(self):
        if not self.history:
            return
        self.storage.delete(self.userid)

    def add(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def prompt_system(self, content: str):
        self.add("system", content)

    def log_assistant(self, content: str):
        self.add("assistant", content)

    def log_user(self, content: str):
        self.add("user", content)
