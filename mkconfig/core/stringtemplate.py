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

    def init(self, line):
        """
        initialize paramters

        :param line: line of string containing templates
        """
        logger.debug('PythonSTEngine.init()')
        self._template = Template(line)

    def apply(self, context, output_file_path, is_in_memory=False):
        """
        Apply the template with python string template engine.

        :param context: A map of key-value attribute defined variables to be applied with template
        :param output_file_path: file name to the substitution result.
        :param isInMemory (bool):  whether to perform templateing in-memory or in-file.
        """

        result = self._template.safe_substitute(context)
        logger.debug('PythonSTEngine.generate() w/ result [%s]', result)

        if is_in_memory:
            return result
        else:
            try:
                file = open(output_file_path, 'w')
                file.write(result)
                file.close()
            except IOError as e:
                errno, strerror = e.args
                logger.error("I/O error[%s] at [%s]: %s", errno, output_file_path, strerror)
                raise



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