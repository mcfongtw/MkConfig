from mkconfig.conf.collectd.context import CTX_KEY_COMMON_COLLECTD_JMX_ATTR_TEMPLATE_FILE
from mkconfig.conf.factory import ConfigurationType
from mkconfig.env import setup_logging_with_details
import logging
setup_logging_with_details()
logger = logging.getLogger(__name__)
from mkconfig.core.stringtemplate import PySTEngine
import unittest



class TestStringTemplateEngine(unittest.TestCase):

    def setUp(self):
        logger.info('Unit Test [{}] Start'.format(self.id()))

    def tearDown(self):
        logger.info('Unit Test [{}] Stop'.format(self.id()))

    def test_unit_basic_pything_string_template(self):
        context = {'name' : 'John'}
        engine = PySTEngine()
        engine.init('Hello World, $name')

        result = engine.apply(context, None, True)
        self.assertEqual("Hello World, John", result)

    def test_unit_collectd_genericjmx_template_string(self):
        engine = PySTEngine()
        engine.init(ConfigurationType.COLLECTD_GENERIC_JMX.get_attribute_template_file())

        context = {'attribute': 'mbean'}
        result = engine.apply(context, None, True)
        self.assertEqual('collectd_genericjmx.mbean.inc', result)

        context = {'attribute': 'connection'}
        result = engine.apply(context, None, True)
        self.assertEqual('collectd_genericjmx.connection.inc', result)

if __name__ == '__main__':
    unittest.main()