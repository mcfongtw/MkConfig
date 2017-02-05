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

if __name__ == '__main__':
    unittest.main()