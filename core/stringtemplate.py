from core.engine import TemplateEngine
from env import Configurations
from string import Template
import logging
import env


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
        logger.debug('PythonSTEngine.init()')
        self._template = Template(line)

    def apply(self, context, outputFile, isInMemory=False):
        logger.debug('PythonSTEngine.generate()')

        result = self._template.safe_substitute(context)
        if isInMemory:
            return result
        else:
            with open(Configurations.getTemplateFile(outputFile), 'w') as file:
                file.write(result)

    class Factory(object):
        """
        Inner Factory class to fulfill the binding from TemplateEngineFactory
        """
        @staticmethod
        def create(): return PySTEngine()