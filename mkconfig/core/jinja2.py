from mkconfig.core.engine import TemplateEngine
from jinja2 import Environment
import logging
from mkconfig.env import Configurations
import mkconfig.env

logger = logging.getLogger(__name__)


class Jinja2Engine(TemplateEngine):
    """
    A concret TemplateEngine implementation based on Jinja2 framework.
    """
    _engine = None;

    def __init__(self):
        super().__init__()

    def init(self, initLoader):
        logger.debug('Jinja2.init()')

        self._engine = Environment(
            autoescape=False,
            loader=initLoader,
            trim_blocks=False)

    def apply(self, context, templateName, outputFile, isInMemory=False):
        logger.debug('Jinja2.generate()')

        if isInMemory :
            result = self._engine.get_template(templateName).render(context)
            return result
        else:
            result = self._engine.get_template(templateName).render(context)
            with open(Configurations.getTemplateFile(outputFile), 'w') as file:
                file.write(result)

    class Factory(object):
        """
        Inner Factory class to fulfill the binding from TemplateEngineFactory
        """
        @staticmethod
        def create(): return Jinja2Engine()