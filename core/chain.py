from abc import ABCMeta, abstractmethod

class Transfiguration(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def transfigure(self):
        pass


class ChainOfTransfiguration(object):

    _chain = []

    def __init__(self):
        pass

    def add(self, transfiguration):
        self._chain.append(transfiguration)

    def get(self, index):
        return self._chain[index]

    def size(self):
        return len(self._chain)

    def execute(self):
        for transfiguration in self._chain :
            transfiguration.transfigure()


