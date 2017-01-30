from mkconfig.conf.utils import Utils
import unittest
import logging
import mkconfig.env


logger = logging.getLogger(__name__)


class TestUtilFunctions(unittest.TestCase):

    def setUp(self):
        logger.info('Unit Test [{}] Start'.format(self.id()))

    def tearDown(self):
        logger.info('Unit Test [{}] Stop'.format(self.id()))

    def test_utilities_boolean_to_lowercase_literal(self):
        result = Utils.boolean_to_lowercase_literal(True)
        self.assertEqual(result, 'true')

        result = Utils.boolean_to_lowercase_literal(False)
        self.assertEqual(result, 'false')

        result = Utils.boolean_to_lowercase_literal('Abc')
        self.assertEqual(result, 'Abc')

if __name__ == '__main__':
    unittest.main()