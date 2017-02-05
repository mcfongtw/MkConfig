import logging

logger = logging.getLogger(__name__)


class TemplateEngineFactory(object):
    """
    A factory method implementation that returns a TemplateEngine, given a name
    """
    _factories = {}

    @staticmethod
    def add_factory(entity, factory):
        logger.info('Add Factory {}'.format(entity))
        TemplateEngineFactory._factories[entity] = factory

    @staticmethod
    def clear_all():
        logger.info('Clear all factories')
        TemplateEngineFactory._factories={}


    # A Template Method:
    @staticmethod
    def create_engine(entity):
        if entity not in TemplateEngineFactory._factories:
            TemplateEngineFactory._factories[entity] = eval(entity + '.Factory()')

        logger.debug('Invoke {}.Factory()'.format(entity))
        return TemplateEngineFactory._factories[entity].create()