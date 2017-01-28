from conf.collectd import CollectdJmxPartialTransifgurationChain, YamlFileReaderToContextTransfiguration
from unittest import TestCase
from core.factory import TemplateEngineFactory
from core.jinja2 import Jinja2Engine
from conf.factory import ConfigTemplateFactory
import logging
import env


logger = logging.getLogger(__name__)

class TestConfigTemplateFactory(TestCase):

    def setUp(self):
        print('Unit Test [{}] Start'.format(self.id()))

    def tearDown(self):
        print('Unit Test [{}] Stop'.format(self.id()))

    def test_default_config_template_factory(self):
        self.assertEqual('collectd_jmx.template', ConfigTemplateFactory.get_config_tempalte(None))
        self.assertEqual('collectd_jmx.template', ConfigTemplateFactory.get_config_tempalte('rubbish'))

    def test_collectd_jmx_config_template_factory(self):
        self.assertEqual('collectd_jmx.template', ConfigTemplateFactory.get_config_tempalte('collectd_jmx'))




class TestCollectdJmxTransfiguration(TestCase):

    def setUp(self):
        print('Unit Test [{}] Start'.format(self.id()))

    def tearDown(self):
        print('Unit Test [{}] Stop'.format(self.id()))

    def test_functional_YamlReadTransfiguration(self):
        context = {
            'test_input' : 'test.basics.properties.yaml'
        }
        TemplateEngineFactory.add_factory('Jinja2Engine', Jinja2Engine.Factory)

        reader = YamlFileReaderToContextTransfiguration('test_input')
        reader.perform(context)

        self.assertEqual(context['test1'], 123)
        self.assertEqual(context['test2'], 'abc')

    def test_functional_YamlReadTransfiguration_FileNotFound(self):
        context = {
            'test_input' : 'test.basics.properties.yaml1'
        }
        TemplateEngineFactory.add_factory('Jinja2Engine', Jinja2Engine.Factory)

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