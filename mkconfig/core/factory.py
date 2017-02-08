import logging

logger = logging.getLogger(__name__)


class TemplateEngineFactory(object):
    """
    A factory method implementation that returns a TemplateEngine
    """
    _factories = {}

    @staticmethod
    def register_factory(entity, factory):
        """
        Register a subtype of TempalteEngine.Factory via entity
        :param entity: a subtype of TemplateEngine
        :param factory: a TemplateEngine.Factory

        """
        logger.debug('[Factory] Loading Factory [%s] for [%s]', factory, entity)
        TemplateEngineFactory._factories[entity] = factory

    @staticmethod
    def unregister_all_factories():
        """
        Unregistered all known TempalteEngine.Factory
        """
        logger.debug('[Factory] Clear all factories')
        TemplateEngineFactory._factories={}


    # A Template Method:
    @staticmethod
    def create_engine(entity):
        """
        Create a TempalteEngine via associated TempalteEngine.Factory
        :param entity: a subtype of TempalteEngine
        :return: TemplateEngine created via associated TempalteEngine.Factory
        """
        if entity not in TemplateEngineFactory._factories:
            TemplateEngineFactory._factories[entity] = eval(entity + '.Factory()')

        logger.debug('[Factory] Invoke [%s].Factory()', entity)
        return TemplateEngineFactory._factories[entity].create()