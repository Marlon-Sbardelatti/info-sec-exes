class Hmac:
    def __init__(self, key: str | bytes):
        if type(key) is str:
            key = key.encode('utf-8')

        self.key = key
