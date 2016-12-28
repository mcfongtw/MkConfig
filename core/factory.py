import logging
import env

logger = logging.getLogger(__name__)


class TemplateEngineFactory(object):
    """
    A factory method implementation that returns a TemplateEngine, given a name
    """
    _factories = {}

    @staticmethod
    def addFactory(entity, factory):
        logger.info('Add Factory {}'.format(entity))
        TemplateEngineFactory._factories[entity] = factory


    # A Template Method:
    @staticmethod
    def createEngine(entity):
        if entity not in TemplateEngineFactory._factories:
            TemplateEngineFactory._factories[entity] = eval(entity + '.Factory()')

        logger.debug('Invoke {}.Factory()'.format(entity))
        return TemplateEngineFactory._factories[entity].create()