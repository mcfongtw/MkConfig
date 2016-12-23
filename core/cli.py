from conf.collectd import JmxTransifgurationChain
from conf.factory import ConfigTemplateFactory
import logging
import env
from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from cement.utils.misc import init_defaults
import os.path

logger = logging.getLogger(__name__)


class CliController(CementBaseController):
    class Meta:
        label = "base"
        description = "Make Configuration"

        # add arguments to the parser
        arguments = [
            (['-p', '--props'],
                dict(action='store', metavar='File', help='Input to properties.yaml', required=True)),
            (['-m', '--mbeans'],
                dict( action='store', metavar='File', help='Input to mbeans.yaml', required=True)),
            #TODO: Make this arg optional and provide a factory method to retrieve this with alias
            (['-t', '--template'],
                dict(action='store', metavar='STR', help='Type of configuration template', default="collectd_jmx.template")),
            (['-o', '--output'],
                dict(action='store', metavar='File', help='Path to output file', required=True)),
        ]

    @expose(hide=True, help="Generate configuration", aliases=['run'])
    def default(self):
        config_template_file = ConfigTemplateFactory.get_config_tempalte(self.app.pargs.template)

        context = {
            '_collectd_jmx_yaml_props_file': self.app.pargs.props,
            '_collectd_jmx_yaml_mbeans_file': self.app.pargs.mbeans,
            '_collectd_jmx_input': config_template_file,
            '_collectd_jmx_output': self.app.pargs.output
        }
        chain = JmxTransifgurationChain()
        chain.execute(context)


# define the application class
class MkConfigApp(CementApp):

    class Meta(object):
        # define any hook functions here
        def pre_setup_hook(self):
            logger.debug("pre_setup hook")

        def post_setup_hook(self):
            logger.debug("post_setup hook")

        def pre_run_hook(self):
            logger.debug("pre_run hook")

        def post_run_hook(self):
            logger.debug("post_run hook")

        def pre_argument_parsing_hook(self):
            logger.debug("pre_argument_parsing hook")

        @staticmethod
        def validate_file_exist(file_path):
            if not os.path.isfile(file_path):
                raise IOError('File [{0}] not found !'.format(file_path))

        def pre_render_hook(self):
            logger.debug("pre_render hook")

        def post_render_hook(self):
            logger.debug("post_render hook")

        def pre_close_hook(self):
            logger.debug("pre_close hook")

        def post_close_hook(self):
            logger.debug("post_close hook")

        def post_argument_parsing_hook(self):
            logger.debug("post_argument_parsing hook")

            logger.info("Received option: props => %s" % self.pargs.props)
            logger.info("Received option: mbeans => %s" % self.pargs.mbeans)
            logger.info("Received option: template => %s" % self.pargs.template)
            logger.info("Received option: output => %s" % self.pargs.output)

            # argument validation
            MkConfigApp.Meta.validate_file_exist(self.pargs.props)
            MkConfigApp.Meta.validate_file_exist(self.pargs.mbeans)

        #application settings
        label = 'mkconfig'
        base_controller = CliController

        # define our default configuration options
        config_defaults = init_defaults('mkconfig')
        config_defaults['mkconfig']['debug'] = False

        extensions = []
        hooks = [
            ('pre_setup', pre_setup_hook),
            ('post_setup', post_setup_hook),

            ('pre_run', pre_run_hook),
            ('post_run', post_run_hook),

            ('pre_argument_parsing', pre_argument_parsing_hook),
            ('post_argument_parsing', post_argument_parsing_hook),

            ('pre_render', pre_render_hook),
            ('post_render', post_render_hook),

            ('pre_close', pre_close_hook),
            ('post_close', post_close_hook),
        ]

    def go(self):
        try:
            self.setup()

            # log stuff
            logger.debug("About to run my mkconfig application!")

            # run the application
            self.run()

            logger.info("Make Config Complete!!");
        except Exception as e:
            logger.info("Caught exception [%s]" % e)
            raise e;
        finally:
            self.close()