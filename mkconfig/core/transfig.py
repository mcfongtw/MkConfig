from abc import ABCMeta, abstractmethod
from mkconfig.core.factory import TemplateEngineFactory
from mkconfig.core.jinja2 import Jinja2Engine
from jinja2 import FileSystemLoader
import yaml
import logging

logger = logging.getLogger(__name__)


class Transfiguration(object):
    """
    A change in form of configuration
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def perform(self, context):

        logger.debug("======================================================================")
        logger.debug('Transfiguration being performed:[{}]'.format(self.__class__.__name__))
        logger.debug("======================================================================")
        pass


class ContextAwareTransfiguration(Transfiguration):
    """
    A type of Trasnfiguration that depends on a customizable key-value mapping
    """

    def __init__(self):
        super().__init__()

    def perform(self, context):
        super().perform(context)

        logger.debug("======================================================================")
        logger.debug('Transfiguration performed w/ Context : [{}]'.format(context))
        logger.debug("======================================================================")
        return context;


class Jinja2InMemoryTemplateTransfiguration(ContextAwareTransfiguration):
    """
    A context-enabled transfiguration that transform with respect to given template name and return output string
    """

    _engine = None
    _input = None
    _output = None

    def __init__(self, searchPath):
        super().__init__()
        self._engine = TemplateEngineFactory.create_engine(Jinja2Engine.__name__)
        self._engine.init(FileSystemLoader(searchPath))

    def perform(self, context):
        super().perform(context)
        self._engine.apply(context, self._input, None, True)

        logger.debug("======================================================================")
        logger.debug('Jinja2 Template Transifiguration [{}] performed in-memory'.format(self._input))
        logger.debug("======================================================================")


class Jinja2FileTemplateTransfiguration(ContextAwareTransfiguration):
    """
    A context-enabled transfiguration that transform with respect to given template name and write to output file
    """

    _engine = None
    _input = None
    _output = None

    def __init__(self, searchPath):
        super().__init__()
        self._engine = TemplateEngineFactory.create_engine(Jinja2Engine.__name__)
        self._engine.init(FileSystemLoader(searchPath))

    def perform(self, context):
        super().perform(context)
        self._engine.apply(context, self._input, self._output)

        logger.debug("======================================================================")
        logger.debug('Jinja2 Template Transifiguration [{}] performed in-file'.format(self._input))
        logger.debug("======================================================================")


class FileReaderToContextTransfiguration(ContextAwareTransfiguration):
    """
    A context-enabled transfiguration that opens file
    """

    _ctx_key_file_path = None

    _file = None

    def __init__(self, ctx_key):
        super().__init__()
        self._ctx_key_file_path = ctx_key

    def perform(self, context):
        super().perform(context)

        file_path = context[self._ctx_key_file_path]

        try:
            self._file = open(file_path, 'r')
        except IOError as e:
            errno, strerror = e.args
            logger.error("I/O error[{0}] at [{1}]: {2}".format(errno, file_path, strerror))
            raise

        logger.debug("======================================================================")
        logger.debug('FileReader Transifiguration performed from [{}]'.format(file_path))
        logger.debug("======================================================================")


class YamlFileReaderToContextTransfiguration(FileReaderToContextTransfiguration):
    """
    A context-enabled transfiguration that reads data from yaml and persists the result back into context map
    """

    def __init__(self, keyName):
        super().__init__(keyName)

    def perform(self, context):
        super().perform(context)
        self.read_content(context)
        self._file.close()

        logger.debug("======================================================================")
        logger.debug('YamlFileReader Transifiguration performed'.format(context))
        logger.debug("======================================================================")

    def read_content(self, context):
        yaml_content = yaml.load(self._file)

        for key, value in yaml_content.items():
            context[key] = value