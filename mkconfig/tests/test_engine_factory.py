from mkconfig.env import setup_logging_with_details
import logging
from mkconfig.core.engine import TemplateEngine, TemplateEngineEnum
from mkconfig.core.factory import TemplateEngineFactory
from mkconfig.env import Configurations
import unittest
from mkconfig.core.stringtemplate import PySTEngine
setup_logging_with_details()
logger = logging.getLogger(__name__)


from mkconfig.core.jinja2 import Jinja2Engine



class TestEngine1(TemplateEngine):

    def __init__(self):
        super().__init__()

    def init(self, initLoader=None):
        return 'TestEngine1.init()'

    def apply(self, context, templateName, outputFile, isInMemory=False):
        return 'TestEngine1.apply()'

    class Factory(object):
        @staticmethod
        def create(): return TestEngine1()


class TestEngine2(TemplateEngine):

    def __init__(self):
        super().__init__()

    def init(self, initLoader=None):
        return 'TestEngine2.init()'

    def apply(self, context, templateName, outputFile, isInMemory=False):
        return 'TestEngine2.apply()'

    class Factory(object):
        @staticmethod
        def create(): return TestEngine2()


class TestTemplateEngineFactory(unittest.TestCase):

    def setUp(self):
        logger.info('Unit Test [{}] Start'.format(self.id()))

    def tearDown(self):
        logger.info('Unit Test [{}] Stop'.format(self.id()))

    def test_unit_template_engine_enum(self):
        self.assertEqual('TestEngine1', TemplateEngineEnum.valueOf('TestEngine1'))
        self.assertEqual('TestEngine2', TemplateEngineEnum.valueOf(TestEngine2.__name__))
        self.assertEqual('PySTEngine', TemplateEngineEnum.valueOf(PySTEngine.__name__))
        expectd = ['Jinja2Engine', 'TestEngine1', 'TestEngine2', 'PySTEngine']
        actual = TemplateEngineEnum.getAllShapes()
        self.assertEqual(len(expectd), len(actual))
        self.assertEqual(sorted(expectd), sorted(actual))

    def test_unit_tempalte_engine_factory_not_register(self):
        with self.assertRaises(NameError):
            TemplateEngineFactory.create_engine('TestEngine1')

    def test_unit_template_engine_factory_1(self):
        TemplateEngineFactory.add_factory('TestEngine1', TestEngine1.Factory)
        test_engine = TemplateEngineFactory.create_engine('TestEngine1')
        self.assertEqual('TestEngine1.init()', test_engine.init())
        self.assertEqual('TestEngine1.apply()', test_engine.apply(None, None, None))

    def test_unit_template_engine_factory_for_jinja2_engine(self):
        TemplateEngineFactory.add_factory('Jinja2Engine', Jinja2Engine.Factory)
        test_engine = TemplateEngineFactory.create_engine('Jinja2Engine')
        test_engine.init(Configurations.getTemplateDir())