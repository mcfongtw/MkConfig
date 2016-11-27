import abc

class Transfiguration(object):
    def __init__(self):
        self._next = None

    def perform(self):
        self.transfigure()

        if self._next:
            self._next.perform()

    @abc.abstractmethod
    def transfigure(self):
        pass

    def set_next(self, next):
        self._next = next
        return self

    def get_next(self):
        return self._next


class ChainOfTransfiguration(object):

    def __init__(self, first):
        self._first = first

    def execute(self):
        self._first.perform()


