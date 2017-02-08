from mkconfig.core.engine import TemplateEngine
from jinja2 import Environment
from mkconfig.env import Configurations
import logging

logger = logging.getLogger(__name__)


class Jinja2Engine(TemplateEngine):
    """
    A concret TemplateEngine implementation based on Jinja2 framework.
    """
    _engine = None;

    def __init__(self):
        super().__init__()

    def init(self, initLoader):
        """
        Initialize the jinja2 environment

        :param initLoader:
        """
        logger.debug('Jinja2.init()')

        self._engine = Environment(
            autoescape=False,
            loader=initLoader,
            trim_blocks=False)

    def apply(self, context, templateName, outputFile, isInMemory=False):
        """
        Apply the template with jinja2 engine.

        :param context: A map of key-value attribute defined variables to be applied with template
        :param templateName: name of template to apply with
        :param outputFile: file name to the substitution result.
        :param isInMemory (bool):  whether to perform templateing in-memory or in-file.
        """
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
        def create():
            """
            A factory method to create an associated Jinja2Engine instance

            :return: the associated Jinja2Engine object
            """
            return Jinja2Engine()