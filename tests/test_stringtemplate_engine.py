from core.stringtemplate import PySTEngine
import unittest
import logging
import env


logger = logging.getLogger(__name__)


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