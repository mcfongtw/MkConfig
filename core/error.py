

class IllegalStateException(Exception):

    def __init__(self, expression, message):
        self.message = message