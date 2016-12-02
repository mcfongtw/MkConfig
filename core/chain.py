from abc import ABCMeta, abstractmethod


class Transfiguration(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def perform(self, context):
        pass


class DependentTransfiguration(Transfiguration):

    def __init__(self):
        super().__init__()

    def perform(self, context):
        return context;


class ChainOfTransfiguration(object):

    _chain = []

    _context = {}

    def __init__(self):
        pass

    def add(self, transfiguration):
        self._chain.append(transfiguration)

    def get(self, index):
        return self._chain[index]

    def size(self):
        return len(self._chain)

    def execute(self, context = None):
        for transfiguration in self._chain :
            print(context)
            transfiguration.perform(context)


