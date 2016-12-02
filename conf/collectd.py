from core.chain import Transfiguration
from core.factory import TemplateEngineFactory
from core.jinja2 import Jinja2Engine
from env import Configurations
from core.chain import ChainOfTransfiguration
from abc import ABCMeta, abstractmethod
import yaml

class JmxTransfiguration(Transfiguration):

    _engine = None

    def __init__(self):
        super().__init__()
        TemplateEngineFactory.addFactory('Jinja2Engine', Jinja2Engine.Factory)
        self._engine = TemplateEngineFactory.createEngine(Jinja2Engine.__name__)
        self._engine.init()

    @abstractmethod
    def prepare(self, context, inputPath, outputPath):
        pass

    def transfigure(self):
        super().transfigure()
        self._engine.apply(self._context, self._input, self._output)


class JmxTransTemplateToStub(JmxTransfiguration):

    def __init__(self):
        super().__init__()

    def prepare(self, context, input, output):
        super().prepare()
        self._context = context
        self._input = input
        self._output = Configurations.getTemplateFile(output)


class JmxTransStubToConfiguration(JmxTransfiguration):

    def __init__(self):
        super().__init__()

    def prepare(self, context, input, output):
        super().prepare()
        self._context = context
        self._input = input
        self._output = Configurations.getOutputFile(output)


class JmxTransifgurationChain(ChainOfTransfiguration):

    def __init__(self):
        self._step1 = JmxTransTemplateToStub()
        self._step2 = JmxTransStubToConfiguration()

    def prepare(self, context1, context2, input, output):
        intermediate_template = '_' + input + '.tmp'
        self._step1.prepare(context1, input, intermediate_template)
        self._step2.prepare(context2, intermediate_template, output)

        self.add(self._step1)
        self.add(self._step2)


