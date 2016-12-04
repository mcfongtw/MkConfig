from abc import ABCMeta, abstractmethod
import logging
import env

logger = logging.getLogger(__name__)


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
        super().perform(context)
        logger.debug('Transfiguration performed w/ Context : [{}]'.format(context))
        return context;


class ChainOfTransfiguration(object):

    _chain = []

    _context = {}

    def __init__(self):
        pass

    def add(self, transfiguration):
        logger.info('Adding transfiguration : [{}]'.format(transfiguration.__class__))
        self._chain.append(transfiguration)

    def get(self, index):
        return self._chain[index]

    def size(self):
        return len(self._chain)

    def execute(self, context = None):
        for transfiguration in self._chain :
            transfiguration.perform(context)


