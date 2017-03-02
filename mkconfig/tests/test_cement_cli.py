import os

from mkconfig.conf.utils import Utils
from mkconfig.env import setup_logging_with_details, Configurations
import logging
from cement.utils import test
setup_logging_with_details()
logger = logging.getLogger(__name__)

from mkconfig.core.cli import MkConfigApp


class TestMkConfigApp(test.CementTestCase):
    app_class =  MkConfigApp

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

    def test_normal_start_and_stop(self):
        app = self.make_app(argv=['-tcollectd_genericjmx', '-otest.output', '-scassandra', '-d../examples/'])
        app.setup()
        app.run()

        self.assertEqual(app.pargs.app_conf_dir, '../examples/')
        self.assertEqual(app.pargs.template, 'collectd_genericjmx')
        self.assertEqual(app.pargs.output, 'test.output')
        self.assertEqual(app.pargs.apps_list, 'cassandra')

        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'cassandra.output.partial')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_genericjmx.plugin.partial.template.stub')))

        app.close()

    def test_normal_with_default_template(self):
        app3 = self.make_app(argv=['-scassandra', '-otest.output', '-d../examples/'])
        app3.setup()
        app3.run()

        self.assertEqual(app3.pargs.app_conf_dir, '../examples/')
        self.assertEqual(app3.pargs.template, 'collectd_genericjmx')
        self.assertEqual(app3.pargs.output, 'test.output')
        self.assertEqual(app3.pargs.apps_list, 'cassandra')

        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'cassandra.output.partial')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_genericjmx.plugin.partial.template.stub')))

        app3.close()

    def test_normal_start_and_stop_with_apps_list(self):
        app = self.make_app(argv=['-tcollectd_genericjmx.template', '-otest.output', '-scassandra jenkins', '-d../examples/'])
        app.setup()
        app.run()

        self.assertEqual(app.pargs.output, 'test.output')
        self.assertEqual(app.pargs.apps_list, 'cassandra jenkins')

        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'cassandra.output.partial')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'jenkins.output.partial')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_genericjmx.plugin.partial.template.stub')))

        app.close()

    def test_normal_start_and_stop_with_all_exampl_apps(self):
        app = self.make_app(argv=['-otest.output', '-scassandra jenkins jira', '-d../examples/'])
        app.setup()
        app.run()

        self.assertEqual(app.pargs.output, 'test.output')
        self.assertEqual(app.pargs.apps_list, 'cassandra jenkins jira')

        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'cassandra.output.partial')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'jenkins.output.partial')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'jira.output.partial')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_genericjmx.plugin.partial.template.stub')))

        app.close()


    def test_file_not_found_1(self):
        app1 = self.make_app(argv=['-o1', '-t1', '-sunknown', '-d1'])
        app1.setup()
        with self.assertRaises(IOError):
            app1.run()
        app1.close()


