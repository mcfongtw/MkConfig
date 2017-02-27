import logging
import os

from mkconfig.conf.context import CTX_KEY_COLLECTD_JMX_APP_PREFIX, \
    CTX_KEY_COLLECTD_JMX_CONF_YAML_FILE, CTX_KEY_COLLECTD_JMX_APP_CONF_DIR, \
    CTX_KEY_COLLECTD_JMX_MBEANS_SET, CTX_KEY_COLLECTD_JMX_TEMPLATE_FILE, \
    CTX_KEY_COLLECTD_JMX_USER_SELECTED_APP_LIST
from mkconfig.conf.utils import Utils
from mkconfig.env import setup_logging_with_details, Configurations

setup_logging_with_details()
logger = logging.getLogger(__name__)

from mkconfig.conf.collectd import CollectdJmxPartialTransifgurationChain, \
    YamlFileReaderToContextTransfiguration, PrepareAppConfTransfiguration, \
    CollectdJmxConfToContextTransfiguration, SplitAppConfTransfiguration
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
        self.assertEqual('collectd_genericjmx.plugin.partial.template', ConfigurationTypeFactory.get_config_tempalte(None))
        self.assertEqual('collectd_genericjmx.plugin.partial.template', ConfigurationTypeFactory.get_config_tempalte('rubbish'))

    def test_collectd_jmx_config_template_factory(self):
        self.assertEqual('collectd_genericjmx.plugin.partial.template', ConfigurationTypeFactory.get_config_tempalte('collectd_jmx'))


class TestCollectdJmxTransfiguration(TestCase):

    def setUp(self):
        logger.info('Unit Test [{}] Start'.format(self.id()))

    def tearDown(self):
        folder = Configurations.getTmpTemplateDir()
        logger.info('Removing all files under %s', folder)
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        logger.info('Removing all files under %s ---- DONE', folder)
        logger.info('Unit Test [{}] Stop'.format(self.id()))

    def test_functional_YamlFileReaderToContextTransfiguration_normal(self):
        ctx_key = '_test_input_key'
        context = {
            ctx_key : 'collectd.jmx.test.conf.yaml'
        }
        TemplateEngineFactory.register_factory('Jinja2Engine', Jinja2Engine.Factory)

        reader = YamlFileReaderToContextTransfiguration(ctx_key)
        reader.perform(context)

        self.assertEqual(context['test1'], 123)
        self.assertEqual(context['test2'], 'abc')

    def test_functional_YamlFileReaderToContextTransfiguration_FileNotFound(self):
        ctx_key = '_test_input_key'
        context = {
            ctx_key : 'test.file.do.not.exist.yaml'
        }
        TemplateEngineFactory.register_factory('Jinja2Engine', Jinja2Engine.Factory)

        reader = YamlFileReaderToContextTransfiguration(ctx_key)

        with self.assertRaises(IOError):
            reader.perform(context)

    def test_functional_CollectdJmxConfToContextTransfiguration(self):
        context = {
            CTX_KEY_COLLECTD_JMX_CONF_YAML_FILE : 'examples/collectd.jmx.app1.conf.yaml'
        }
        TemplateEngineFactory.register_factory('Jinja2Engine', Jinja2Engine.Factory)

        reader = CollectdJmxConfToContextTransfiguration()
        reader.perform(context)

        self.assertEqual(context['progName'], 'app1')
        self.assertEqual(context['progPrefix'], 'APP1_')
        self.assertEqual(context[CTX_KEY_COLLECTD_JMX_MBEANS_SET][0]['attributes'][0][
                                                                      'Attribute'], 'HeapMemoryUsage')
        self.assertEqual(context[CTX_KEY_COLLECTD_JMX_MBEANS_SET][0]['attributes'][1][
                             'InstancePrefix'], 'Non_Heap_Memory_Usage_')
        self.assertEqual(context[CTX_KEY_COLLECTD_JMX_MBEANS_SET][1]['attributes'][0][
                             'Attribute'], 'Value')

    def test_functional_PrepareAppConfTransfiguration(self):
        context = {
            CTX_KEY_COLLECTD_JMX_APP_PREFIX : 'test',
            CTX_KEY_COLLECTD_JMX_APP_CONF_DIR : './'
        }

        transfig = PrepareAppConfTransfiguration()
        transfig.perform(context)
        self.assertEqual(context[CTX_KEY_COLLECTD_JMX_CONF_YAML_FILE],
                                 './collectd.jmx.test.conf.yaml')

    def test_functional_CollectdJmxPartialTransifgurationChain(self):
        #init context
        context =  {
            CTX_KEY_COLLECTD_JMX_APP_CONF_DIR : 'examples/',
            CTX_KEY_COLLECTD_JMX_APP_PREFIX: 'app1',
            CTX_KEY_COLLECTD_JMX_TEMPLATE_FILE : 'collectd_genericjmx.plugin.partial.template',
        }
        chain = CollectdJmxPartialTransifgurationChain()
        chain.execute(context)

        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'app1.output.partial')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_genericjmx.plugin.partial.template.tmp')))


    def test_functional_SplitAppConfTransfiguration_for_two_app(self):
        #init context
        context =  {
            CTX_KEY_COLLECTD_JMX_APP_CONF_DIR : 'examples/',
            CTX_KEY_COLLECTD_JMX_USER_SELECTED_APP_LIST : 'app1 app2',
            CTX_KEY_COLLECTD_JMX_TEMPLATE_FILE : 'collectd_genericjmx.plugin.partial.template',
        }
        transfig = SplitAppConfTransfiguration()
        transfig.perform(context)

        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'app1.output.partial')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'app2.output.partial')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_genericjmx.plugin.partial.template.tmp')))
