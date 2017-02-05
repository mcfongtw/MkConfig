import logging

logger = logging.getLogger(__name__)


class ChainOfTransfiguration(object):
    """
    A chain of responsibility implementation that channel through a series of transifgurations. One may depend
    on previous step with respect to Context
    """

    _chain = []

    _context = {}

    def __init__(self):
        self._chain = []
        self._context = {}

    def add(self, transfiguration):
        self._chain.append(transfiguration)
        logger.debug('Add transfiguration : [{}] to chain'.format(transfiguration.__class__))

    def get(self, index):
        return self._chain[index]

    def size(self):
        return len(self._chain)

    def execute(self, context = None):
        for transfiguration in self._chain :
            logger.info("Performing Transfiguration [{}]".format(transfiguration.__class__))
            transfiguration.perform(context)


