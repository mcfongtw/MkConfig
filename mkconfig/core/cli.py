import logging
import yaml

from cement.core.controller import CementBaseController, expose
from cement.core.foundation import CementApp
from cement.utils.misc import init_defaults

from mkconfig.conf.collectd.jmx import FullChainedTransfiguration
from mkconfig.conf.collectd.context import CTX_KEY_COMMON_COLLECTD_JMX_ATTR_TEMPLATE_FILE, \
    CTX_KEY_COMMON_COLLECTD_JMX_USER_SELECTED_APP_LIST, CTX_KEY_COMMON_COLLECTD_JMX_FINAL_OUTPUT, \
    CTX_KEY_COMMON_COLLECTD_JMX_APP_CONF_DIR, CTX_KEY_COMMON_COLLECTD_JMX_TYPE, \
    CTX_KEY_COMMON_COLLECTD_JMX_FULL_TEMPLATE_FILE
from mkconfig.conf.factory import ConfigurationTypeFactory, ConfigurationType
from mkconfig.core.error import IllegalStateException

logger = logging.getLogger(__name__)


class CliController(CementBaseController):
    """
    A Controller class to add arguments and linking commands with functions
    """
    class Meta:
        """
        Meta class that defines arguments.
        """
        label = "base"
        description = "Make Configuration"

        # add arguments to the parser
        arguments = [
            (['-i', '--transf_desc_file'],
             dict(action='store', metavar='File', help='Path to transformation descriptor file', default='',
                  required=True)),
            (['-d', '--transf_desc_string'],
             dict(action='store', metavar='STR', help='(Optional) yaml content of transformation descriptor', default='')),
            (['-t', '--type'],
                dict(action='store', metavar='STR', help='(Optional) Type of configuration', default="collectd_genericjmx")),
            (['-o', '--output'],
                dict(action='store', metavar='File', help='Path to output file', required=True)),
        ]

    @expose(hide=True, help="Generate configuration", aliases=['run'])
    def default(self):
        """
        A default command to execute. Internally, it will execute the chain of transfiguration that generates the
        configuration

        """

        config_template_type = ConfigurationTypeFactory.get_config_type(self.app.pargs.type)

        if config_template_type.get_supertype() == ConfigurationType.COLLECTD_GENERIC_JMX.get_supertype():
            attr_template_file = config_template_type.get_attribute_template_file()
            full_template_file = config_template_type.get_full_template_file()
            config_template_subtype = config_template_type.get_subtype()

            if self.app.pargs.transf_desc_string == '':
                logger.info("Read config control from file %s" % self.app.pargs.transf_desc_file)
                config_control_content = yaml.load(open(self.app.pargs.transf_desc_file, 'r'))
            else:
                logger.info("Read config control from string %s" % self.app.pargs.transf_desc_string)
                config_control_content = yaml.load(self.app.pargs.transf_desc_string)

            logger.info("config control content [%s]" % config_control_content)
            app_list = config_control_content['app_list']
            app_conf_dir = config_control_content['app_conf_dir']

            context = {
                CTX_KEY_COMMON_COLLECTD_JMX_APP_CONF_DIR: app_conf_dir,
                CTX_KEY_COMMON_COLLECTD_JMX_ATTR_TEMPLATE_FILE: attr_template_file,
                CTX_KEY_COMMON_COLLECTD_JMX_FULL_TEMPLATE_FILE : full_template_file,
                CTX_KEY_COMMON_COLLECTD_JMX_TYPE: config_template_subtype,
                CTX_KEY_COMMON_COLLECTD_JMX_FINAL_OUTPUT: self.app.pargs.output,
                CTX_KEY_COMMON_COLLECTD_JMX_USER_SELECTED_APP_LIST: app_list,
            }
            chain = FullChainedTransfiguration()
            chain.execute(context)
        else :
            raise IllegalStateException('Unknown config type [%d]' % config_template_type.get_supertype())

# define the application class
class MkConfigApp(CementApp):
    """
    An application class that define a life scope of MkConfig
    """
    class Meta(object):
        """
        A Meta class that defines hook
        """
        # define any hook functions here


        def pre_setup_hook(self):
            """
            a hook before setup()
            """
            logger.debug("pre_setup hook")

        def post_setup_hook(self):
            """
            a hook after setup()
            """
            logger.debug("post_setup hook")

        def pre_run_hook(self):
            """
            a hook before run()
            """
            logger.debug("pre_run hook")

        def post_run_hook(self):
            """
            a hook after run()
            """
            logger.debug("post_run hook")

        def pre_argument_parsing_hook(self):
            """
            a hook before parse_arg()
            """
            logger.debug("pre_argument_parsing hook")

        def pre_render_hook(self):
            """
            a hook before render()
            """
            logger.debug("pre_render hook")

        def post_render_hook(self):
            """
            a hook after render()
            """
            logger.debug("post_render hook")

        def pre_close_hook(self):
            """
            a hook before close()
            """
            logger.debug("pre_close hook")

        def post_close_hook(self):
            """
            a hook after close()
            """
            logger.debug("post_close hook")

        def post_argument_parsing_hook(self):
            """
            a hook after parse_arg()
            """
            logger.debug("post_argument_parsing hook")

            logger.info("Received option: (input) transf_desc_file => %s" % self.pargs.transf_desc_file)
            logger.info("Received option: (input) transf_desc_string => %s" % self.pargs.transf_desc_string)
            logger.info("Received option: type => %s" % self.pargs.type)
            logger.info("Received option: (output) config output => %s" % self.pargs.output)


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
        """
        Execute the cement application lifecycle.

        """
        try:
            self.setup()

            # run the application
            self.run()

            logger.info("Make Config Complete!!");
        except Exception as e:
            logger.info("Caught exception [%s]" % e)
            raise e;
        finally:
            self.close()