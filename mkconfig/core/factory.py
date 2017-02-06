import logging

logger = logging.getLogger(__name__)


class TemplateEngineFactory(object):
    """
    A factory method implementation that returns a TemplateEngine, given a name
    """
    _factories = {}

    @staticmethod
    def add_factory(entity, factory):
        logger.debug('[Factory] Loading Factory [%s] for [%s]', factory, entity)
        TemplateEngineFactory._factories[entity] = factory

    @staticmethod
    def clear_all():
        logger.debug('[Factory] Clear all factories')
        TemplateEngineFactory._factories={}


    # A Template Method:
    @staticmethod
    def create_engine(entity):
        if entity not in TemplateEngineFactory._factories:
            TemplateEngineFactory._factories[entity] = eval(entity + '.Factory()')

        logger.debug('[Factory] Invoke [%s].Factory()', entity)
        return TemplateEngineFactory._factories[entity].create()