from core.stringtemplate import PySTEngine
import unittest


class TestStringTemplateEngine(unittest.TestCase):

    def setUp(self):
        super(TestStringTemplateEngine, self).setUp()


    def test_unit_basic_pything_string_template(self):
        context = {'name' : 'John'}
        engine = PySTEngine()
        engine.init('Hello World, $name')

        result = engine.apply(context, None, True)
        self.assertEqual("Hello World, John", result)

if __name__ == '__main__':
    unittest.main()