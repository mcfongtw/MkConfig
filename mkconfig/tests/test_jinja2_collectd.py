from mkconfig.env import setup_logging_with_details
import logging
setup_logging_with_details()
logger = logging.getLogger(__name__)

from mkconfig.conf.collectd import CollectdJmxPartialTransifgurationChain, YamlFileReaderToContextTransfiguration
from unittest import TestCase
from mkconfig.core.factory import TemplateEngineFactory
from mkconfig.core.jinja2 import Jinja2Engine
from mkconfig.conf.factory import ConfigurationTypeFactory


class TestConfigTemplateFactory(TestCase):

    def setUp(self):
        print('Unit Test [{}] Start'.format(self.id()))

    def tearDown(self):
        print('Unit Test [{}] Stop'.format(self.id()))

    def test_default_config_template_factory(self):
        self.assertEqual('collectd_jmx.template', ConfigurationTypeFactory.get_config_tempalte(None))
        self.assertEqual('collectd_jmx.template', ConfigurationTypeFactory.get_config_tempalte('rubbish'))

    def test_collectd_jmx_config_template_factory(self):
        self.assertEqual('collectd_jmx.template', ConfigurationTypeFactory.get_config_tempalte('collectd_jmx'))




class TestCollectdJmxTransfiguration(TestCase):

    def setUp(self):
        print('Unit Test [{}] Start'.format(self.id()))

    def tearDown(self):
        print('Unit Test [{}] Stop'.format(self.id()))

    def test_functional_YamlReadTransfiguration(self):
        context = {
            'test_input' : 'test.basics.properties.yaml'
        }
        TemplateEngineFactory.register_factory('Jinja2Engine', Jinja2Engine.Factory)

        reader = YamlFileReaderToContextTransfiguration('test_input')
        reader.perform(context)

        self.assertEqual(context['test1'], 123)
        self.assertEqual(context['test2'], 'abc')

    def test_functional_YamlReadTransfiguration_FileNotFound(self):
        context = {
            'test_input' : 'test.basics.properties.yaml1'
        }
        TemplateEngineFactory.register_factory('Jinja2Engine', Jinja2Engine.Factory)

        reader = YamlFileReaderToContextTransfiguration('test_input')

        with self.assertRaises(IOError):
            reader.perform(context)

    def test_integration_collectd_jmx_trans_chain(self):
        #init context
        context =  {
            '_collectd_jmx_app_conf_dir' : '../examples/',
            '_collectd_jmx_app_prefix': 'cassandra',
            '_collectd_jmx_input' : 'collectd_jmx.template',
            '_collectd_jmx_output' : 'test.output',
        }
        chain = CollectdJmxPartialTransifgurationChain()
        chain.execute(context)