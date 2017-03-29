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
    example_dir = Configurations.getProjectRootDir() + '/examples/'

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

    #########################################################################################
    # Default Behavior
    #########################################################################################

    def test_normal_with_default_template(self):
        config_control_string = """
        app_list :
            - cassandra
        app_conf_dir : """ + self.example_dir

        app = self.make_app(argv=['-d'+ config_control_string, '-i ',  '-otest.output'])
        app.setup()
        app.run()

        self.assertEqual(app.pargs.transf_desc_file, ' ')
        self.assertEqual(app.pargs.transf_desc_string, config_control_string)
        self.assertEqual(app.pargs.type, 'collectd_genericjmx')
        self.assertEqual(app.pargs.output, 'test.output')

        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'cassandra.mbean.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'cassandra.connection.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_genericjmx.mbean.inc.stub')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_genericjmx.connection.inc.stub')))

        app.close()

    def test_file_not_found_1(self):
        app1 = self.make_app(argv=['-o1', '-t1', '-i1'])
        app1.setup()
        with self.assertRaises(IOError):
            app1.run()
        app1.close()

    #########################################################################################
    # Collectd-GenericJmx specific
    #########################################################################################

    def test_normal_start_and_stop_on_jenkins_with_genericjmx(self):
        config_control_string = """
        app_list :
            - jenkins
        app_conf_dir : """ + self.example_dir

        app = self.make_app(
            argv=['-tcollectd_genericjmx', '-otest.output', '-i ', '-d'+ config_control_string,])
        app.setup()
        app.run()

        self.assertEqual(app.pargs.transf_desc_file, ' ')
        self.assertEqual(app.pargs.transf_desc_string, config_control_string)
        self.assertEqual(app.pargs.type, 'collectd_genericjmx')
        self.assertEqual(app.pargs.output, 'test.output')

        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'jenkins.mbean.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'jenkins.connection.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_genericjmx.mbean.inc.stub')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_genericjmx.connection.inc.stub')))

        app.close()

    def test_normal_start_and_stop_on_cassandra_with_genericjmx(self):
        config_control_string = """
        app_list :
            - cassandra
        app_conf_dir : """ + self.example_dir

        app = self.make_app(
            argv=['-tcollectd_genericjmx', '-otest.output', '-i ', '-d'+ config_control_string,])
        app.setup()
        app.run()

        self.assertEqual(app.pargs.transf_desc_file, ' ')
        self.assertEqual(app.pargs.transf_desc_string, config_control_string)
        self.assertEqual(app.pargs.type, 'collectd_genericjmx')
        self.assertEqual(app.pargs.output, 'test.output')

        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'cassandra.mbean.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'cassandra.connection.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_genericjmx.mbean.inc.stub')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_genericjmx.connection.inc.stub')))

        app.close()

    def test_normal_start_and_stop_with_apps_list_with_genericjmx(self):
        config_control_string = """
        app_list :
            - cassandra
            - jenkins
        app_conf_dir : """ + self.example_dir

        app = self.make_app(
            argv=['-tcollectd_genericjmx', '-otest.output', '-i ', '-d'+ config_control_string,])
        app.setup()
        app.run()

        self.assertEqual(app.pargs.transf_desc_file, ' ')
        self.assertEqual(app.pargs.transf_desc_string, config_control_string)
        self.assertEqual(app.pargs.output, 'test.output')

        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'cassandra.mbean.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'cassandra.connection.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'jenkins.mbean.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'jenkins.connection.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_genericjmx.mbean.inc.stub')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_genericjmx.connection.inc.stub')))

        app.close()

    def test_normal_start_and_stop_with_all_exampl_apps_with_genericjmx(self):
        config_control_string = """
        app_list :
            - cassandra
            - jenkins
            - jira
        app_conf_dir : """ + self.example_dir

        app = self.make_app(
            argv=['-tcollectd_genericjmx', '-otest.output', '-i ', '-d'+ config_control_string])
        app.setup()
        app.run()

        self.assertEqual(app.pargs.transf_desc_file, ' ')
        self.assertEqual(app.pargs.transf_desc_string, config_control_string)
        self.assertEqual(app.pargs.output, 'test.output')

        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'cassandra.mbean.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'cassandra.connection.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'jenkins.mbean.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'jenkins.connection.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'jira.mbean.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'jira.connection.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_genericjmx.mbean.inc.stub')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_genericjmx.connection.inc.stub')))

        app.close()

    #########################################################################################
    # Collectd-FastJmx specific
    #########################################################################################

    def test_normal_start_and_stop_on_jenkins_with_fastjmx(self):
        config_control_string = """
        app_list :
            - jenkins
        app_conf_dir : """ + self.example_dir

        app = self.make_app(
            argv=['-tcollectd_fastjmx', '-otest.output', '-i ', '-d'+ config_control_string])
        app.setup()
        app.run()

        self.assertEqual(app.pargs.transf_desc_file, ' ')
        self.assertEqual(app.pargs.transf_desc_string, config_control_string)
        self.assertEqual(app.pargs.type, 'collectd_fastjmx')
        self.assertEqual(app.pargs.output, 'test.output')

        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'jenkins.mbean.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'jenkins.connection.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_fastjmx.mbean.inc.stub')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_fastjmx.connection.inc.stub')))

        app.close()

    def test_normal_start_and_stop_on_cassandra_with_fastjmx(self):
        config_control_string = """
        app_list :
            - cassandra
        app_conf_dir : """ + self.example_dir

        app = self.make_app(
            argv=['-tcollectd_fastjmx', '-otest.output', '-i ', '-d'+ config_control_string])
        app.setup()
        app.run()

        self.assertEqual(app.pargs.transf_desc_file, ' ')
        self.assertEqual(app.pargs.transf_desc_string, config_control_string)
        self.assertEqual(app.pargs.type, 'collectd_fastjmx')
        self.assertEqual(app.pargs.output, 'test.output')

        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'cassandra.mbean.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'cassandra.connection.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_fastjmx.mbean.inc.stub')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_fastjmx.connection.inc.stub')))

        app.close()

    def test_normal_start_and_stop_with_apps_list_with_fastjmx(self):
        config_control_string = """
        app_list :
            - cassandra
            - jenkins
        app_conf_dir : """ + self.example_dir

        app = self.make_app(
            argv=['-tcollectd_fastjmx', '-otest.output', '-i ', '-d'+ config_control_string])
        app.setup()
        app.run()

        self.assertEqual(app.pargs.transf_desc_file, ' ')
        self.assertEqual(app.pargs.transf_desc_string, config_control_string)
        self.assertEqual(app.pargs.output, 'test.output')

        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'cassandra.mbean.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'cassandra.connection.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'jenkins.mbean.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'jenkins.connection.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_fastjmx.mbean.inc.stub')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_fastjmx.connection.inc.stub')))

        app.close()

    def test_normal_start_and_stop_with_all_exampl_apps_with_fastjmx(self):
        config_control_string = """
        app_list :
            - cassandra
            - jenkins
            - jira
        app_conf_dir : """ + self.example_dir

        app = self.make_app(
            argv=['-tcollectd_fastjmx', '-otest.output', '-i ', '-d'+ config_control_string])
        app.setup()
        app.run()

        self.assertEqual(app.pargs.transf_desc_file, ' ')
        self.assertEqual(app.pargs.transf_desc_string, config_control_string)
        self.assertEqual(app.pargs.output, 'test.output')

        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'cassandra.mbean.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'cassandra.connection.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'jenkins.mbean.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'jenkins.connection.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'jira.mbean.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            'jira.connection.blocks.inc')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_fastjmx.mbean.inc.stub')))
        self.assertTrue(Utils.is_file_exist(Configurations.getTmpTemplateFile(
            '_collectd_fastjmx.connection.inc.stub')))

        app.close()

