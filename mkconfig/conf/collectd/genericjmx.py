import logging

from mkconfig.conf.collectd.commonjmx import PrepareAppConfTransfiguration,  \
    ConfReaderToContextTransfiguration
from mkconfig.conf.collectd.context import CTX_KEY_COMMON_COLLECTD_JMX_APP_PREFIX, \
    CTX_KEY_COMMON_COLLECTD_JMX_FINAL_OUTPUT, CTX_KEY_COMMON_COLLECTD_JMX_TEMPLATE_FILE, \
    CTX_KEY_COMMON_COLLECTD_JMX_USER_SELECTED_APP_LIST, \
    CTX_KEY_COLLECTD_GENERIC_JMX_TEMPLATE_FILE, CTX_KEY_COLLECTD_GENERIC_JMX_ATTRIBUTE_BLOCK
from mkconfig.conf.utils import Utils
from mkconfig.core.factory import TemplateEngineFactory
from mkconfig.core.jinja2 import Jinja2Engine
from mkconfig.core.stringtemplate import PySTEngine
from mkconfig.core.transfig import ContextAwareTransfiguration, Jinja2FileTemplateTransfiguration, \
    ChainedTransfiguration
from mkconfig.env import Configurations

logger = logging.getLogger(__name__)


class GenericJmxGenerateTemplateNameWithPyST(ContextAwareTransfiguration):
    """
    The first phase of GenericJmxAttributeChainedTransfiguration to retrieve the
    template-file-name via substituting the given attribute name
    """

    def __init__(self, attr):
        """
        prepare the transiguration

        :param attr: A given attribute to replace the template-file-name string
        """
        super().__init__()
        self._attribute = attr

    def perform(self, context):
        """
        To transfigurate while retrieving template-file-name via replacing the given attribute
        name via PySTEngine (Python string template engine)

        :param context: A key-value paired map that stores attributes carried throughput the
        whole lifecycle
        """

        engine = PySTEngine()
        engine.init(context[CTX_KEY_COMMON_COLLECTD_JMX_TEMPLATE_FILE])
        replaced_template_name = engine.apply({'attribute':self._attribute}, None, True)
        context[CTX_KEY_COLLECTD_GENERIC_JMX_TEMPLATE_FILE] = replaced_template_name
        context[CTX_KEY_COLLECTD_GENERIC_JMX_ATTRIBUTE_BLOCK] = self._attribute

        super().perform(context)

        logger.debug("======================================================================")
        logger.debug('[Transifig] Collectd-GenericJmx replaced template name [%s]',
                     replaced_template_name)
        logger.debug("======================================================================")


class GenericJmxInputToStubWithJinja2(Jinja2FileTemplateTransfiguration):
    """
    The second phase of GenericJmxAttributeChainedTransfiguration to transform from input yaml
    files to stub configuration file (half-product)
    """

    def __init__(self):
        """
        prepare the transiguration
        """
        super().__init__([Configurations.getTemplateDir()])

    def perform(self, context):
        """
        To transfigurate while converting template to stub configuration

        :param context: A key-value paired map that stores attributes carried throughput the
        whole lifecycle
        """

        template_name_by_attr = context[CTX_KEY_COLLECTD_GENERIC_JMX_TEMPLATE_FILE]
        stub_template_name = '_' + template_name_by_attr + '.stub'

        self._input = template_name_by_attr
        self._output = Configurations.getTmpTemplateFile(stub_template_name)
        super().perform(context)

        logger.debug("======================================================================")
        logger.debug('[Transifig] Collectd-GenericJmx Template [%s] -> Stub [%s]', self._input,
                     self._output)
        logger.debug("======================================================================")


class GenericJmxStubToOutputViaJinja2(Jinja2FileTemplateTransfiguration):
    """
    The third phase of GenericJmxAttributeChainedTransfiguration to transform from the stub file
    to a partial configuration for a specific application
    """

    def __init__(self):
        """
        prepare the transiguration

        """
        super().__init__([Configurations.getTmpTemplateDir()])

    def perform(self, context):
        """
        To transfigurate while converting stub configuration to partial configuration for an
        application

        :param context: A key-value paired map that stores attributes carried throughput the
        whole lifecycle
        """

        template_name_by_attr = context[CTX_KEY_COLLECTD_GENERIC_JMX_TEMPLATE_FILE]
        attr = context[CTX_KEY_COLLECTD_GENERIC_JMX_ATTRIBUTE_BLOCK]

        stub_template_name = '_' + template_name_by_attr + '.stub'
        output_filename = context[CTX_KEY_COMMON_COLLECTD_JMX_APP_PREFIX] + '.' + attr + \
                          '.blocks.inc'

        self._input = stub_template_name
        self._output = Configurations.getTmpTemplateFile(output_filename)
        super().perform(context)

        logger.debug("======================================================================")
        logger.debug('[Transifig] Collectd-GenericJmx Stub [%s] ->Output [%s]', self._input,
                     self._output)
        logger.debug("======================================================================")


class GenericJmxAttributeChainedTransfiguration(ChainedTransfiguration):

    def __init__(self, attr):
        """
        prepare the chain of transfiguration

        :param attr: A given attribute to replace the template-file-name string
        """
        super().__init__()
        TemplateEngineFactory.register_factory('Jinja2Engine', Jinja2Engine.Factory)

        self._step1 = GenericJmxGenerateTemplateNameWithPyST(attr)
        self._step2 = GenericJmxInputToStubWithJinja2()
        self._step3 = GenericJmxStubToOutputViaJinja2()

        self.add(self._step1)
        self.add(self._step2)
        self.add(self._step3)
        self._attribute = attr

    def execute(self, context):
        """
        To execute the whole series of transfiguration execution

        :param context: A key-value paired map that stores attributes carried throughput the
        whole lifecycle
        """
        logger.info("///////////////////////////////////////////////////////////////////////")
        logger.info("[ChainedTransfig] Collectd-GenericJmx w/ Attribute-wise [%s] ...", self._attribute)
        logger.info("///////////////////////////////////////////////////////////////////////")

        super().execute(context)

        logger.info("///////////////////////////////////////////////////////////////////////")
        logger.info("[ChainedTransfig] Collectd-GenericJmx w/ Attribute-wise [%s] ... COMPLETES",
                    self._attribute)
        logger.info("///////////////////////////////////////////////////////////////////////")


class GenericJmxApplicationChainedTransfiguration(ChainedTransfiguration):
    """
    A chained transfiguration that transform input to a collectd genericjmx template for one
    specific application - incomplete still and need to consolidate all parts into one final
    output with CollectdJmxCompleteChainedTransfiguration
    """

    def __init__(self):
        """
        prepare the chain of transfiguration
        """
        super().__init__()
        TemplateEngineFactory.register_factory('Jinja2Engine', Jinja2Engine.Factory)

        self._step0 = PrepareAppConfTransfiguration()
        self._step1 = ConfReaderToContextTransfiguration()
        self._step2 = GenericJmxAttributeChainedTransfiguration('mbean')
        self._step3 = GenericJmxAttributeChainedTransfiguration('connection')

        self.add(self._step0)
        self.add(self._step1)
        self.add(self._step2)
        self.add(self._step3)

    def execute(self, context):
        """
        To execute the whole series of transfiguration execution

        :param context: A key-value paired map that stores attributes carried throughput the
        whole lifecycle
        """
        app = context[CTX_KEY_COMMON_COLLECTD_JMX_APP_PREFIX]
        logger.info("///////////////////////////////////////////////////////////////////////")
        logger.info("[ChainedTransfig] Collectd-GenericJmx w/ Application-wise [%s] ...", app)
        logger.info("///////////////////////////////////////////////////////////////////////")

        super().execute(context)

        logger.info("///////////////////////////////////////////////////////////////////////")
        logger.info("[ChainedTransfig] Collectd-GenericJmx w/ Application-wise [%s] ... "
                    "COMPLETES", app)
        logger.info("///////////////////////////////////////////////////////////////////////")


class SpliByApplicationTransfiguration(ContextAwareTransfiguration):
    """
    A outer chain that controls the whole process of performing config generation for each
    application and merge the partial results into a final output
    """
    def perform(self, context):
        """
        To transfigurate while parsing the list of applications to be processed

        :param context: A key-value paired map that stores attributes carried throughput the
        whole lifecycle
        """
        listOfAppNames = context[CTX_KEY_COMMON_COLLECTD_JMX_USER_SELECTED_APP_LIST].split()

        #distinguish between string object and list
        if Utils.is_string_type(listOfAppNames):
            logger.info('Processing ONE app [%s]' %listOfAppNames)
            listOfAppNames = [listOfAppNames]

        for appName in listOfAppNames:
            self.perform_transfig_for_each_app(context, appName)

        logger.debug("======================================================================")
        logger.debug('[Transifig] Split via application from list[%s]', listOfAppNames)
        logger.debug("======================================================================")

    def perform_transfig_for_each_app(self, context, app_name):
        """
        Create a CollectdJmxPartialTransifgurationChain to perform config generation with a
        specific application

        :param context: A key-value paired map that stores attributes carried throughput the
        whole lifecycle
        :param app_name: the name of application to generate configuration with
        """
        logger.info('Spliting the partial configuraiton for [%s]' % app_name)

        context[CTX_KEY_COMMON_COLLECTD_JMX_APP_PREFIX] = app_name
        inner_chain = GenericJmxApplicationChainedTransfiguration()
        inner_chain.execute(context)


class GenericJmxConsolidateToFinalOutput(Jinja2FileTemplateTransfiguration):
    """
    The last phase of GenericJmxCompleteChainedTransfiguration to consolidate all partial
    output into a final output.
    """

    def __init__(self):
        """
        prepare the transiguration
        """
        super().__init__([Configurations.getTemplateDir(), Configurations.getTmpTemplateDir()])

    def perform(self, context):
        """
        To transfigurate while merging all partial output via Jinja2 inclusion.

        :param context: A key-value paired map that stores attributes carried throughput the
        whole lifecycle
        """

        final_template_file = 'collectd_genericjmx.template'

        self._input = final_template_file
        self._output = Configurations.getOutputFile(context[CTX_KEY_COMMON_COLLECTD_JMX_FINAL_OUTPUT])
        super().perform(context)

        logger.debug("======================================================================")
        logger.debug('[Transifig] Collectd-GenericJmx Consolidate [%s]->Final output [%s]',
                     self._input, self._output)
        logger.debug("======================================================================")


class GenericJmxCompleteChainedTransfiguration(ChainedTransfiguration):
    """
    A chained transfiguration that consolidate all partial pieces to a complete collectd jmx
    configuration
    """

    def __init__(self):
        """
        prepare the chain of transiguration
        """
        super().__init__()
        TemplateEngineFactory.register_factory('Jinja2Engine', Jinja2Engine.Factory)

        self._step0 = SpliByApplicationTransfiguration()
        self._step1 = GenericJmxConsolidateToFinalOutput()

        self.add(self._step0)
        self.add(self._step1)

    def execute(self, context):
        """
        To execute the whole series of transfiguration execution

        :param context: A key-value paired map that stores attributes carried throughput the
        whole lifecycle
        """
        logger.info("///////////////////////////////////////////////////////////////////////")
        logger.info("[ChainedTransfig] COMPLETE Collectd-GenericJmx Transfiguration ...")
        logger.info("///////////////////////////////////////////////////////////////////////")

        super().execute(context)

        logger.info("///////////////////////////////////////////////////////////////////////")
        logger.info("[ChainedTransfig] COMPLETE Collectd-GenericJmx Transfiguration ... COMPLETES")
        logger.info("///////////////////////////////////////////////////////////////////////")
