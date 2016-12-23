from core.cli import MkConfigApp
import logging
import env
from cement.utils import test

logger = logging.getLogger(__name__)

class TestMkConfigApp(test.CementTestCase):
    app_class =  MkConfigApp

    def setUp(self):
        logger.info('Unit Test [{}] Start'.format(self.id()))

    def tearDown(self):
        logger.info('Unit Test [{}] Stop'.format(self.id()))

    def test_normal_start_and_stop(self):
        app = self.make_app(argv=['-pcassandra.properties.yaml', '-mcassandra_mbean.yaml', '-tcollectd_jmx.template', '-otest.output'])
        app.setup()
        app.run()
        app.close()

    def test_normal_with_default_template(self):
        app3 = self.make_app(argv=['-pcassandra.properties.yaml', '-mcassandra_mbean.yaml', '-otest.output'])
        app3.setup()
        app3.run()
        app3.close()

    def test_file_not_found_1(self):
        app1 = self.make_app(argv=['-pnot_exist.yaml', '-o1', '-t1', '-m1'])
        app1.setup()
        with self.assertRaises(IOError):
            app1.run()
        app1.close()

    def test_file_not_found_2(self):
        app2 = self.make_app(argv=['-mnot_exist.yaml', '-p1', '-t1', '-o1'])
        app2.setup()
        with self.assertRaises(IOError):
            app2.run()
        app2.close()


