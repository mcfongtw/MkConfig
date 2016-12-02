from core.engine import TemplateEngine, TemplateEngineEnum
from core.factory import TemplateEngineFactory
from core.jinja2 import Jinja2Engine
import unittest

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

    def test_unit_template_engine_enum(self):
        self.assertEqual('TestEngine1', TemplateEngineEnum.valueOf('TestEngine1'))
        self.assertEqual('TestEngine2', TemplateEngineEnum.valueOf(TestEngine2.__name__))
        self.assertEqual(['Jinja2Engine', 'TestEngine1', 'TestEngine2'], TemplateEngineEnum.getAllShapes())

    def test_unit_tempalte_engine_factory_not_register(self):
        with self.assertRaises(NameError):
            TemplateEngineFactory.createEngine('TestEngine1')

    def test_unit_template_engine_factory_1(self):
        TemplateEngineFactory.addFactory('TestEngine1', TestEngine1.Factory)
        test_engine = TemplateEngineFactory.createEngine('TestEngine1')
        self.assertEqual('TestEngine1.init()', test_engine.init())
        self.assertEqual('TestEngine1.apply()', test_engine.apply(None, None, None))

    def test_unit_template_engine_factory_for_jinja2_engine(self):
        TemplateEngineFactory.addFactory('Jinja2Engine', Jinja2Engine.Factory)
        test_engine = TemplateEngineFactory.createEngine('Jinja2Engine')
        test_engine.init()