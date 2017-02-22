from mkconfig.core.engine import TemplateEngine
from mkconfig.env import Configurations
from string import Template
import logging

logger = logging.getLogger(__name__)


class PySTEngine(TemplateEngine):
    """
    A concret TemplateEngine implementation based on plain old Python String Template
    """
    _engine = None;
    _template = None

    def __init__(self):
        super().__init__()
        logger.debug('PythonSTEngine.init()')

    def init(self, line):
        """
        initialize paramters

        :param line: line of string containing templates
        """
        logger.debug('PythonSTEngine.init()')
        self._template = Template(line)

    def apply(self, context, output_file, is_in_memory=False):
        """
        Apply the template with python string template engine.

        :param context: A map of key-value attribute defined variables to be applied with template
        :param output_file: file name to the substitution result.
        :param isInMemory (bool):  whether to perform templateing in-memory or in-file.
        """
        logger.debug('PythonSTEngine.generate()')

        result = self._template.safe_substitute(context)
        if is_in_memory:
            return result
        else:
            with open(Configurations.getTemplateFile(output_file), 'w') as file:
                file.write(result)

    class Factory(object):
        """
        Inner Factory class to fulfill the binding from TemplateEngineFactory
        """
        @staticmethod
        def create():
            """
            A factory method to create an associated PySTEngine instance
            :return: the associated PySTEngine object
            """
            return PySTEngine()