import logging

from mkconfig.conf.collectd.commonjmx import PrepareAppConfTransfiguration,  \
    ConfReaderToContextTransfiguration
from mkconfig.conf.collectd.context import CTX_KEY_COLLECTD_COMMON_JMX_APP_PREFIX, \
    CTX_KEY_COLLECTD_COMMON_JMX_FINAL_OUTPUT, CTX_KEY_COLLECTD_COMMON_JMX_TEMPLATE_FILE, \
    CTX_KEY_COLLECTD_COMMON_JMX_USER_SELECTED_APP_LIST
from mkconfig.conf.utils import Utils
from mkconfig.core.factory import TemplateEngineFactory
from mkconfig.core.jinja2 import Jinja2Engine
from mkconfig.core.transfig import ContextAwareTransfiguration, Jinja2FileTemplateTransfiguration, \
    ChainedTransfiguration
from mkconfig.env import Configurations

logger = logging.getLogger(__name__)


class GenericJmxTransTemplateToStubJinja2(Jinja2FileTemplateTransfiguration):
    """
    The first phase of GenericJmxPartialChainedTransfiguration to transform from input yaml
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
        input = context[CTX_KEY_COLLECTD_COMMON_JMX_TEMPLATE_FILE]
        intermediate_template = '_' + input + '.stub'

        self._input = input
        self._output = Configurations.getTmpTemplateFile(intermediate_template)
        super().perform(context)

        logger.debug("======================================================================")
        logger.debug('[Transifig] CollectdJmx Template[%s]->Stub @ [%s]', self._input, self._output)
        logger.debug("======================================================================")


class GenericJmxTransStubToConfiguration(Jinja2FileTemplateTransfiguration):
    """
    The second phase of GenericJmxPartialChainedTransfiguration to transform from the stub file
    to a partial configuration for a specific appliation
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
        intermediate_template = '_' + context[CTX_KEY_COLLECTD_COMMON_JMX_TEMPLATE_FILE] + '.stub'

        output_filename = context[CTX_KEY_COLLECTD_COMMON_JMX_APP_PREFIX] + '.output.partial'

        self._input = intermediate_template
        self._output = Configurations.getTmpTemplateFile(output_filename)
        super().perform(context)

        logger.debug("======================================================================")
        logger.debug('[Transifig] CollectdJmx Stub [%s] ->Output @ [%s]', self._input, self._output)
        logger.debug("======================================================================")


class GenericJmxPartialChainedTransfiguration(ChainedTransfiguration):
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
        self._step2 = GenericJmxTransTemplateToStubJinja2()
        self._step3 = GenericJmxTransStubToConfiguration()

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
        logger.info("///////////////////////////////////////////////////////////////////////")
        logger.info("[Chain] PerAPP CollectdJmx Transfiguration BEGINS")
        logger.info("///////////////////////////////////////////////////////////////////////")

        super().execute(context)

        logger.info("///////////////////////////////////////////////////////////////////////")
        logger.info("[Chain] PerAPP CollectdJmx Transfiguration COMPLETES")
        logger.info("///////////////////////////////////////////////////////////////////////")

class SplitAppConfTransfiguration(ContextAwareTransfiguration):
    """
    A outer chain that controls the whole process of performing config generation for each
    applicaiton and merge the partial results into a final output
    """
    def perform(self, context):
        """
        To transfigurate while parsing the list of applications to be processed

        :param context: A key-value paired map that stores attributes carried throughput the
        whole lifecycle
        """
        listOfAppNames = context[CTX_KEY_COLLECTD_COMMON_JMX_USER_SELECTED_APP_LIST].split()

        #distinguish between string object and list
        if Utils.is_string_type(listOfAppNames):
            logger.info('Processing ONE app [%s]' %listOfAppNames)
            listOfAppNames = [listOfAppNames]

        for appName in listOfAppNames:
            self.generateAppPartialConfiguration(context, appName)

        logger.debug("======================================================================")
        logger.debug('[Transifig] Split app configuration w/ app list [%s]', listOfAppNames)
        logger.debug("======================================================================")

    def generateAppPartialConfiguration(self, context, app_name):
        """
        Create a CollectdJmxPartialTransifgurationChain to perform config generation with a
        specific application

        :param context: A key-value paired map that stores attributes carried throughput the
        whole lifecycle
        :param app_name: the name of application to generate configuration with
        """
        logger.info('Spliting the partial configuraiton for [%s]' % app_name)

        context[CTX_KEY_COLLECTD_COMMON_JMX_APP_PREFIX] = app_name
        inner_chain = GenericJmxPartialChainedTransfiguration()
        inner_chain.execute(context)

class GenericJmxTransConsolidationToFinalOutput(Jinja2FileTemplateTransfiguration):
    """
    The last phase of CollectdJmxTransfiguration to consolidate all partial output into a final
    output.
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
        self._output = Configurations.getOutputFile(context[CTX_KEY_COLLECTD_COMMON_JMX_FINAL_OUTPUT])
        super().perform(context)

        logger.debug("======================================================================")
        logger.debug('[Transifig] CollectdJmx Consolidation[%s]->Final output @ [%s]',
                     self._input,
                     self._output)
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

        self._step0 = SplitAppConfTransfiguration()
        self._step1 = GenericJmxTransConsolidationToFinalOutput()

        self.add(self._step0)
        self.add(self._step1)

    def execute(self, context):
        """
        To execute the whole series of transfiguration execution

        :param context: A key-value paired map that stores attributes carried throughput the
        whole lifecycle
        """
        logger.info("///////////////////////////////////////////////////////////////////////")
        logger.info("[Chain] COMPLETE CollectdJmx Transfiguration BEGINS")
        logger.info("///////////////////////////////////////////////////////////////////////")

        super().execute(context)

        logger.info("///////////////////////////////////////////////////////////////////////")
        logger.info("[Chain] COMPLETE CollectdJmx Transfiguration COMPLETES")
        logger.info("///////////////////////////////////////////////////////////////////////")
