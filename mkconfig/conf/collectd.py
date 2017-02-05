from mkconfig.core.transfig import ContextAwareTransfiguration, Jinja2FileTemplateTransfiguration, \
    YamlFileReaderToContextTransfiguration
from mkconfig.conf.context import CTX_KEY_COLLECTD_JMX_APP_CONF_DIR, \
    CTX_KEY_COLLECTD_JMX_CONF_YAML_FILE, CTX_KEY_COLLECTD_JMX_APP_PREFIX, \
    CTX_KEY_COLLECTD_JMX_FINAL_OUTPUT, CTX_KEY_COLLECTD_JMX_TEMPLATE_FILE, \
    CTX_KEY_COLLECTD_JMX_USER_SELECTED_APP_LIST
from mkconfig.core.factory import TemplateEngineFactory
from mkconfig.core.jinja2 import Jinja2Engine
from mkconfig.env import Configurations
from mkconfig.core.chain import ChainOfTransfiguration
from mkconfig.conf.utils import Utils
import os.path
import yaml
import logging


logger = logging.getLogger(__name__)


class PrepareAppConfTransfiguration(ContextAwareTransfiguration):
    """
    A context-enabled Transifguration that prepares the associated configuration file path for given a app name
    """

    def perform(self, context):
        appName = context[CTX_KEY_COLLECTD_JMX_APP_PREFIX]

        appConfYamlFile = context[CTX_KEY_COLLECTD_JMX_APP_CONF_DIR] + "collectd.jmx." + appName + '.conf.yaml'
        PrepareAppConfTransfiguration.validate_file_exist(appConfYamlFile)
        context[CTX_KEY_COLLECTD_JMX_CONF_YAML_FILE] = appConfYamlFile
        logger.info('Set the conf file for app [%s] at [%s]', appName, appConfYamlFile)

        logger.debug("======================================================================")
        logger.debug('PrepareAppConf Transifiguration w/ appName [%s]', appName)
        logger.debug("======================================================================")


    @staticmethod
    def validate_file_exist(file_path):
        if not os.path.isfile(file_path):
            raise IOError('File [{0}] not found !'.format(file_path))


class CollectdJmxConfToContextTransfiguration(YamlFileReaderToContextTransfiguration):
    """
    A YamlToContextTransfiguration that reads yaml file with respect to attr : _collectd_jmx_conf_yaml_file
    """

    def __init__(self, keyName = CTX_KEY_COLLECTD_JMX_CONF_YAML_FILE):
        super().__init__(keyName)

    def read_content(self, context):
        yaml_content = yaml.load(self._file)

        for key, value in yaml_content.items():
            context[key] = value

        for idx, mbean in enumerate(context['mbeans']):
            self.patch_mbean_table_value(mbean)
            #mbean is updated
            context['mbeans'][idx] = mbean


    def patch_mbean_table_value(self, mbean):
        for attribute in mbean['attributes']:
            if 'Table' in attribute:
                value = attribute['Table']
                attribute['Table'] = Utils.boolean_to_lowercase_literal(value)

        logger.debug(mbean)


class CollectdJmxTransTemplateToStubJinja2(Jinja2FileTemplateTransfiguration):
    """
    The first phase of  CollectdJmxTransfiguration to transform from input yaml files to stub configuration file (half-product)
    """

    def __init__(self):
        super().__init__(Configurations.getTemplateDir())

    def perform(self, context):
        input = context[CTX_KEY_COLLECTD_JMX_TEMPLATE_FILE]
        intermediate_template = '_' + input + '.tmp'

        self._input = input
        self._output = Configurations.getTempFile(intermediate_template)
        super().perform(context)

        logger.debug("======================================================================")
        logger.debug('CollectdJmx Transifig Template[%s]->Stub @ [%s]', self._input, self._output)
        logger.debug("======================================================================")




class CollectdJmxTransStubToConfiguration(Jinja2FileTemplateTransfiguration):
    """
    The second phase of CollectdJmxTransfiguration to transform from the stub file to a partial configuration for a specific appliation
    """

    def __init__(self):
        super().__init__(Configurations.getTempDir())

    def perform(self, context):
        intermediate_template = '_' + context[CTX_KEY_COLLECTD_JMX_TEMPLATE_FILE] + '.tmp'

        output_filename = context[CTX_KEY_COLLECTD_JMX_APP_PREFIX] + '.output.partial'

        self._input = intermediate_template
        self._output = Configurations.getOutputFile(output_filename)
        super().perform(context)

        logger.debug("======================================================================")
        logger.debug('CollectdJmx Transifig Stub->Output @ [%s]', self._output)
        logger.debug("======================================================================")


class CollectdJmxPartialTransifgurationChain(ChainOfTransfiguration):
    """
    An (inner) chain of transfiguration that transform input to a partial collectd jmx configuration
    """

    def __init__(self):
        super().__init__()
        TemplateEngineFactory.add_factory('Jinja2Engine', Jinja2Engine.Factory)

        self._step0 = PrepareAppConfTransfiguration()
        self._step1 = CollectdJmxConfToContextTransfiguration()
        self._step2 = CollectdJmxTransTemplateToStubJinja2()
        self._step3 = CollectdJmxTransStubToConfiguration()

        self.add(self._step0)
        self.add(self._step1)
        self.add(self._step2)
        self.add(self._step3)

        logger.info("PARTIAL CollectdJmx Transfiguration Chain COMPLETE")


class SplitAppConfTransfiguration(ContextAwareTransfiguration):
    """
    A outer chain that controls the whole process of performing config generation for each applicaiton and merge the partial results into a final output
    """
    def perform(self, context):
        listOfAppNames = context[CTX_KEY_COLLECTD_JMX_USER_SELECTED_APP_LIST].split()

        #FIXME: The distinguishment might not be necessary, as above always return a list of 0 or 1 element
        #distinguish between string object and list
        if isinstance(listOfAppNames, str):
            logger.info('Processing ONE app [%s]' %listOfAppNames)
            self.generateAppPartialConfiguration(context, listOfAppNames)
        else :
            logger.info('Processing list of apps [%s]' % listOfAppNames)
            for appName in listOfAppNames:
                self.generateAppPartialConfiguration(context, appName)

        logger.debug("======================================================================")
        logger.debug('Split app configuration w/ app list [%s]', listOfAppNames)
        logger.debug("======================================================================")

    def generateAppPartialConfiguration(self, context, appName):
        logger.info('Spliting the partial configuraiton for [%s]' % appName)

        context[CTX_KEY_COLLECTD_JMX_APP_PREFIX] = appName
        inner_chain = CollectdJmxPartialTransifgurationChain()
        inner_chain.execute(context)


class CollectdJmxConsolidatePartialConfigurations(ContextAwareTransfiguration):
    """
    The final phase of CollectdJmxTransfiguration to consolidated a complete Collectd-Jmx configuration.
    """
    def __init__(self):
        super().__init__()

    def perform(self, context):

        header = """
LoadPlugin java

<Plugin "java">
    #JVMARG "-verbose:jni"
    #JVMARG "-Xmx128m"
    JVMArg "-Djava.class.path=/usr/share/collectd/java/collectd-api.jar:/usr/share/collectd/java/generic-jmx.jar"

    LoadPlugin "org.collectd.java.GenericJMX"
        """

        footer = """


</Plugin>
        """

        content = header
        partial_files = []

        listOfAppNames = context[CTX_KEY_COLLECTD_JMX_USER_SELECTED_APP_LIST].split()

        # Retreive list of partial files based on user selected apps under output/
        for appName in listOfAppNames :
            file_name = appName + ".output.partial"
            partial_files.append(Configurations.getOutputFile(file_name))


        for partial_file_path in partial_files:
            if partial_file_path.endswith('.partial'):
                try:
                    file = open(partial_file_path, "r")
                except IOError as e:
                    errno, strerror = e.args
                    logger.error("I/O error[%s] at [%s]: %s", errno, partial_file_path, strerror)
                    raise
                else:
                    partial_content = file.read()
                    content += partial_content
                    file.close()
                    logger.info("Read partial content fromm [%s]" % partial_file_path)


        content += footer

        output_filename = Configurations.getOutputFile(context[CTX_KEY_COLLECTD_JMX_FINAL_OUTPUT])

        try:
            file = open(output_filename, "w")
        except IOError as e:
            errno, strerror = e.args
            logger.error("I/O error[{0}] at [%s]: %s", errno, output_filename, strerror)
            raise
        else:
            file.write(content)
            file.close()
            logger.info("Final collectd jmx configuration output @ [%s]" % output_filename)

            logger.debug("======================================================================")
            logger.debug('CollectdJmx merge all partial output @ [%s]', output_filename)
            logger.debug("======================================================================")


class CollectdJmxTransfigurationChain(ChainOfTransfiguration):
    """
    An (outer) chain of transfiguration that consolidate all partial pieces to a complete collectd jmx configuration
    """

    def __init__(self):
        super().__init__()

        self._step0 = SplitAppConfTransfiguration()
        self._step1 = CollectdJmxConsolidatePartialConfigurations()

        self.add(self._step0)
        self.add(self._step1)

        logger.info("CollectdJmx Transfiguration Chain COMPLETE")




