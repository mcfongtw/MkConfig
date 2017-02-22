

class IllegalStateException(Exception):
    """
    An error when program enter an unexpected state
    """
    def __init__(self, message):
        self.message = message