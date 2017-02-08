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
        """
        Add a transfiguration into the chain of execution.

        :param transfiguration: a transfiguration to be added

        """
        self._chain.append(transfiguration)
        logger.debug('Add transfiguration : [%s] to chain', transfiguration.__class__)

    def get(self, index):
        """
        Retrieve a transifguration in the chain at position [index]

        :param index: index from 0 to size-of-chain

        :return: the transfiguration at chain[index]
        """
        return self._chain[index]

    def size(self):
        """
        Retrieve the # of transigurations in chain.

        :return: length of chain
        """
        return len(self._chain)

    def execute(self, context = None):
        """
        Perform execution of transfiguration one-by-one in the chain

        :param context: a map of key-value attributes to perform

        """
        for transfiguration in self._chain :
            logger.info("Performing Transfiguration [%s]", transfiguration.__class__)
            transfiguration.perform(context)


