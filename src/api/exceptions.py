class InvalidPost(Exception):
    def __init__(self, message):
        self.message = message


class InvalidTokenId(Exception):
    def __init__(self, message):
        self.message = message
