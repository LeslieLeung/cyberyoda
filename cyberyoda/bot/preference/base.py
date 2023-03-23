class Preference:
    user_id: str
    temperature: float

    def __init__(self, user_id):
        self.user_id = user_id

    def load(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError
