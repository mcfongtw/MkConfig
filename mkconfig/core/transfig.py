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
        """
        prepare the transiguration
        """
        pass

    @abstractmethod
    def perform(self, context):
        """
        Abstract function to perform transfiguration

        :param context: A key-value paired map that stores attributes carried throughput the whole lifecycle
        """
        logger.debug("======================================================================")
        logger.debug('[Transifig] being performed:[%s]', self.__class__.__name__)
        logger.debug("======================================================================")
        pass


class ContextAwareTransfiguration(Transfiguration):
    """
    A type of Trasnfiguration that depends on a customizable key-value mapping
    """

    def __init__(self):
        """
        prepare the transiguration
        """
        super().__init__()

    def perform(self, context):
        """
        To perform transfiguration with context

        :param context: A key-value paired map that stores attributes carried throughput the whole lifecycle
        """
        super().perform(context)

        logger.debug("======================================================================")
        logger.debug('[Transifig] performed w/ Context : [%s]', context)
        logger.debug("======================================================================")


class Jinja2InMemoryTemplateTransfiguration(ContextAwareTransfiguration):
    """
    A context-enabled transfiguration that transform with respect to given template name and return output string
    """

    _engine = None
    _input = None
    _output = None

    def __init__(self, search_path):
        """
        prepare the transiguration

        :param search_path: file path of the template to search for
        """
        super().__init__()
        self._engine = TemplateEngineFactory.create_engine(Jinja2Engine.__name__)
        self._engine.init(FileSystemLoader(search_path))

    def perform(self, context):
        """
        To transfigurate while applying Jinja2 templating in-memory

        :param context: A key-value paired map that stores attributes carried throughput the whole lifecycle
        """
        super().perform(context)
        self._engine.apply(context, self._input, None, True)

        logger.debug("======================================================================")
        logger.debug('[Transifig] Jinja2 Template [%s] performed in-memory', self._input)
        logger.debug("======================================================================")


class Jinja2FileTemplateTransfiguration(ContextAwareTransfiguration):
    """
    A context-enabled transfiguration that transform with respect to given template name and write to output file
    """

    _engine = None
    _input = None
    _output = None

    def __init__(self, search_path):
        """
        prepare the transiguration

        :param search_path: file path of the template to search for
        """
        super().__init__()
        self._engine = TemplateEngineFactory.create_engine(Jinja2Engine.__name__)
        self._engine.init(FileSystemLoader(search_path))

    def perform(self, context):
        """
        To transfigurate while applying Jinja2 templating in-file

        :param context: A key-value paired map that stores attributes carried throughput the whole lifecycle
        """
        super().perform(context)
        self._engine.apply(context, self._input, self._output)

        logger.debug("======================================================================")
        logger.debug('[Transifig] Jinja2 Template [%s] performed in-file', self._input)
        logger.debug("======================================================================")


class FileReaderToContextTransfiguration(ContextAwareTransfiguration):
    """
    A context-enabled transfiguration that opens file
    """

    _ctx_key_file_path = None

    _file = None

    def __init__(self, ctx_key):
        """
        prepare the transiguration

        :param ctx_key: A context key referring to as path of the file being read
        """
        super().__init__()
        self._ctx_key_file_path = ctx_key

    def perform(self, context):
        """
        To transfigurate while reading file to context

        :param context: A key-value paired map that stores attributes carried throughput the whole lifecycle
        """
        super().perform(context)

        file_path = context[self._ctx_key_file_path]

        try:
            self._file = open(file_path, 'r')
        except IOError as e:
            errno, strerror = e.args
            logger.error("I/O error[%s] at [%s]: %s", errno, file_path, strerror)
            raise

        logger.debug("======================================================================")
        logger.debug('[Transifig] FileReader performed from [%s]', file_path)
        logger.debug("======================================================================")


class YamlFileReaderToContextTransfiguration(FileReaderToContextTransfiguration):
    """
    A context-enabled transfiguration that reads data from yaml and persists the result back into context map
    """

    def __init__(self, keyName):
        """
        prepare the transiguration

        :param keyName: A context key referring to as path of the YAML file being read
        """
        super().__init__(keyName)

    def perform(self, context):
        """
        To transfigurate while reading Yaml file to context

        :param context: A key-value paired map that stores attributes carried throughput the whole lifecycle
        """
        super().perform(context)
        self.read_content(context)
        self._file.close()

        logger.debug("======================================================================")
        logger.debug('[Transifig] YamlFileReader performed', context)
        logger.debug("======================================================================")

    def read_content(self, context):
        yaml_content = yaml.load(self._file)

        for key, value in yaml_content.items():
            context[key] = value