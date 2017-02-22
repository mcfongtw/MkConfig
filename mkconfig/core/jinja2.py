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

    def init(self, init_loader):
        """
        Initialize the Jinja2 environment

        :param init_loader: The template loader for Jinja2 environment
        """
        logger.debug('Jinja2.init()')

        self._engine = Environment(
            autoescape=False,
            loader=init_loader,
            trim_blocks=False)

    def apply(self, context, template_name, output_file, is_in_memory=False):
        """
        Apply the template with Jinja2 environment.

        :param context: A map of key-value attribute defined variables to be applied with template
        :param template_name: name of template to apply with
        :param output_file: file name to the substitution result.
        :param isInMemory (bool):  whether to perform templateing in-memory or in-file.
        """
        logger.debug('Jinja2.generate()')

        if is_in_memory :
            result = self._engine.get_template(template_name).render(context)
            return result
        else:
            result = self._engine.get_template(template_name).render(context)
            with open(Configurations.getTemplateFile(output_file), 'w') as file:
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