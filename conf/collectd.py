from core.chain import DependentTransfiguration
from core.factory import TemplateEngineFactory
from core.jinja2 import Jinja2Engine
from env import Configurations
from core.chain import ChainOfTransfiguration
import yaml
import logging
import env


logger = logging.getLogger(__name__)


class JmxTransfiguration(DependentTransfiguration):

    _engine = None
    _input = None
    _output = None

    def __init__(self):
        super().__init__()
        self._engine = TemplateEngineFactory.createEngine(Jinja2Engine.__name__)
        self._engine.init()

    def perform(self, context):
        super().perform(context)
        self._engine.apply(context, self._input, self._output)


class YamlReadTransfiguration(DependentTransfiguration):

    _key_file_path = None

    def __init__(self, keyName):
        super().__init__()
        self._key_file_path = keyName

    def perform(self, context):
        super().perform(context)
        file_path = context[self._key_file_path]
        try:
            file = open(file_path, 'r')
        except IOError as e:
            errno, strerror = e.args
            print("I/O error({0}): {1}".format(errno, strerror))
            raise
        else:
            yaml_content = yaml.load(file)
            file.close()

            for key, value in yaml_content.items():
                context[key] = value


class JmxTransReadPropertiesFromYaml(YamlReadTransfiguration):
    def __init__(self, keyName = '_collectd_jmx_yaml_props_file'):
        super().__init__(keyName)


class JmxTransReadMbeansFromYaml(YamlReadTransfiguration):

    def __init__(self, keyName = '_collectd_jmx_yaml_mbeans_file'):
        super().__init__(keyName)

    def perform(self, context):
        #FIXME: resolve this inheritance issue
        logger.info('Transfiguration performing :[{}]'.format(self.__class__.__name__))
        file_path = context[self._key_file_path]
        mbeans = []

        try:
            file = open(file_path, 'r')

        except IOError as e:
            errno, strerror = e.args
            print("I/O error({0}): {1}".format(errno, strerror))
            raise
        else:
            raw_content = file.read()
            for block in raw_content.split('---'):
                try:
                    mbeans.append(yaml.load(block))
                except SyntaxError:
                    mbeans.append(block)

            context['mbeans'] = mbeans


class JmxTransTemplateToStub(JmxTransfiguration):

    def __init__(self):
        super().__init__()

    def perform(self, context):
        input = context['_collectd_jmx_input']
        intermediate_template = '_' + input + '.tmp'

        self._input = input
        self._output = Configurations.getTemplateFile(intermediate_template)
        super().perform(context)


class JmxTransStubToConfiguration(JmxTransfiguration):

    def __init__(self):
        super().__init__()

    def perform(self, context):
        input = context['_collectd_jmx_input']
        intermediate_template = '_' + input + '.tmp'
        output = context['_collectd_jmx_output']

        self._input = intermediate_template
        self._output = Configurations.getOutputFile(output)
        super().perform(context)


class JmxTransifgurationChain(ChainOfTransfiguration):

    def __init__(self):
        super().__init__()
        TemplateEngineFactory.addFactory('Jinja2Engine', Jinja2Engine.Factory)

        self._step1 = JmxTransReadPropertiesFromYaml()
        self._step2 = JmxTransReadMbeansFromYaml()
        self._step3 = JmxTransTemplateToStub()
        self._step4 = JmxTransStubToConfiguration()

        self.add(self._step1)
        self.add(self._step2)
        self.add(self._step3)
        self.add(self._step4)


