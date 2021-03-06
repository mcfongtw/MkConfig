from mkconfig.env import setup_logging_with_details
import logging
setup_logging_with_details()
logger = logging.getLogger(__name__)

from mkconfig.conf.utils import Utils
import unittest

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

    def test_utilities_is_type_string(self):
        #string
        self.assertTrue(Utils.is_string_type('abc'))
        test = "abc"
        self.assertTrue(Utils.is_string_type(test))

        #list
        self.assertFalse(Utils.is_string_type([1,2,3]))
        list = [1,2,3]
        self.assertFalse(Utils.is_string_type(list))

        #tuple
        self.assertFalse(Utils.is_string_type((1,2,3)))
        tuple = (1,2,3)
        self.assertFalse(Utils.is_string_type(tuple))


if __name__ == '__main__':
    unittest.main()