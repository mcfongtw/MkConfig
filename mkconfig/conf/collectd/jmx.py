import logging

import yaml

from mkconfig.conf.collectd.context import CTX_KEY_COMMON_COLLECTD_JMX_APP_CONF_DIR, \
    CTX_KEY_COMMON_COLLECTD_JMX_CONF_YAML_FILE, CTX_KEY_COMMON_COLLECTD_JMX_MBEANS_SET, \
    CTX_KEY_COMMON_COLLECTD_JMX_TYPE
from mkconfig.conf.collectd.context import CTX_KEY_COMMON_COLLECTD_JMX_APP_PREFIX, \
    CTX_KEY_COMMON_COLLECTD_JMX_FINAL_OUTPUT, CTX_KEY_COMMON_COLLECTD_JMX_ATTR_TEMPLATE_FILE, \
    CTX_KEY_COMMON_COLLECTD_JMX_USER_SELECTED_APP_LIST, \
    CTX_KEY_COLLECTD_GENERIC_JMX_TEMPLATE_FILE, CTX_KEY_COLLECTD_GENERIC_JMX_ATTRIBUTE_BLOCK, \
    CTX_KEY_COMMON_COLLECTD_JMX_MBEANS_HIERARCHY, CTX_KEY_COMMON_COLLECTD_JMX_COLLECTIONS_SET, \
    CTX_KEY_COMMON_COLLECTD_JMX_COLLECTIONS_ENTRY_VALIDATED, \
    CTX_KEY_COMMON_COLLECTD_JMX_FULL_TEMPLATE_FILE
from mkconfig.conf.utils import Utils
from mkconfig.core.factory import TemplateEngineFactory
from mkconfig.core.jinja2 import Jinja2Engine
from mkconfig.core.stringtemplate import PySTEngine
from mkconfig.core.transfig import ContextAwareTransfiguration, Jinja2FileTemplateTransfiguration, \
    ChainedTransfiguration
from mkconfig.core.transfig import YamlFileReaderToContextTransfiguration
from mkconfig.env import Configurations

logger = logging.getLogger(__name__)


class PrepareAppConfTransfiguration(ContextAwareTransfiguration):
    """
    A context-enabled Transifguration that prepares the associated collectd jmx configuration file
    path for given an application name
    """

    def perform(self, context):
        """
        To transfigurate while preparing configuration meta

        :param context: A key-value paired map that stores attributes carried throughput the
        whole lifecycle
        """
        appName = context[CTX_KEY_COMMON_COLLECTD_JMX_APP_PREFIX]
        jmxType = context[CTX_KEY_COMMON_COLLECTD_JMX_TYPE]

        appConfYamlFile = context[CTX_KEY_COMMON_COLLECTD_JMX_APP_CONF_DIR] + "collectd." + jmxType + "." + appName + '.conf.yaml'
        self.validate_file_exist(appConfYamlFile)
        context[CTX_KEY_COMMON_COLLECTD_JMX_CONF_YAML_FILE] = appConfYamlFile
        logger.info('Set the conf file for app [%s] at [%s]', appName, appConfYamlFile)

        logger.debug("======================================================================")
        logger.debug('[Transifig] Prepare conf meta for application [%s]', appName)
        logger.debug("======================================================================")


    def validate_file_exist(self, file_path):
        if not Utils.is_file_exist(file_path):
            raise IOError('File [{0}] not found !'.format(file_path))


class ConfReaderToContextTransfiguration(YamlFileReaderToContextTransfiguration):
    """
    A YamlToContextTransfiguration that reads yaml file with respect to attr :
    _collectd_jmx_conf_yaml_file
    """

    def __init__(self, keyName = CTX_KEY_COMMON_COLLECTD_JMX_CONF_YAML_FILE):
        """
        prepare the transiguration
        """
        super().__init__(keyName)

    def read_content(self, context):
        """
        Read content of a Yaml file

        :param context: A key-value paired map that stores attributes carried throughput the
        whole lifecycle
        """
        yaml_content = yaml.load(self._file)

        for key, value in yaml_content.items():
            context[key] = value
            #memoize mbean hierarchy
            logger.debug('Update Context[%s]=[%s]', key, value)
            if key == CTX_KEY_COMMON_COLLECTD_JMX_MBEANS_SET:
                if not CTX_KEY_COMMON_COLLECTD_JMX_MBEANS_HIERARCHY in context:
                    logger.info("Init context[%s]", CTX_KEY_COMMON_COLLECTD_JMX_MBEANS_HIERARCHY)
                    context[CTX_KEY_COMMON_COLLECTD_JMX_MBEANS_HIERARCHY] = {}

                app_name = context[CTX_KEY_COMMON_COLLECTD_JMX_APP_PREFIX]
                context[CTX_KEY_COMMON_COLLECTD_JMX_MBEANS_HIERARCHY][app_name] = value
                logger.debug("Update context[%s][%s]=[%s]", CTX_KEY_COMMON_COLLECTD_JMX_MBEANS_HIERARCHY, app_name, value)

        for idx, mbean in enumerate(context[CTX_KEY_COMMON_COLLECTD_JMX_MBEANS_SET]):
            self.patch_mbean_table_value(mbean)
            #mbean is updated
            context[CTX_KEY_COMMON_COLLECTD_JMX_MBEANS_SET][idx] = mbean

    def patch_mbean_table_value(self, mbean):
        """
        Patch the specific mbean attribute

        :param mbean: mbean attribute to be patched
        """
        for attribute in mbean['attributes']:
            if 'Table' in attribute:
                value = attribute['Table']
                attribute['Table'] = Utils.boolean_to_lowercase_literal(value)

        logger.debug('MBean patched result : [%s]', mbean)


class GenerateTemplateFileNameViaPyST(ContextAwareTransfiguration):
    """
    The first phase of AttributeChainedTransfiguration to retrieve the
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
        engine.init(context[CTX_KEY_COMMON_COLLECTD_JMX_ATTR_TEMPLATE_FILE])
        replaced_template_name = engine.apply({'attribute':self._attribute}, None, True)
        context[CTX_KEY_COLLECTD_GENERIC_JMX_TEMPLATE_FILE] = replaced_template_name
        context[CTX_KEY_COLLECTD_GENERIC_JMX_ATTRIBUTE_BLOCK] = self._attribute

        super().perform(context)

        jmxType = context[CTX_KEY_COMMON_COLLECTD_JMX_TYPE]
        logger.debug("======================================================================")
        logger.debug('[Transifig] Collectd-[%s] replaced template name [%s]', jmxType,
                     replaced_template_name)
        logger.debug("======================================================================")


class GenerateTemplateStubViaJinja2(Jinja2FileTemplateTransfiguration):
    """
    The second phase of AttributeChainedTransfiguration to transform from input yaml
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

        self._template_file_name = template_name_by_attr
        self._output_file_path = Configurations.getTmpTemplateFile(stub_template_name)
        super().perform(context)

        jmxType = context[CTX_KEY_COMMON_COLLECTD_JMX_TYPE]
        logger.debug("======================================================================")
        logger.debug('[Transifig] Collectd-[%s] Template [%s] -> Stub [%s]', jmxType, self._template_file_name,
                     self._output_file_path)
        logger.debug("======================================================================")


class GenerateTemplateOutputViaJinja2(Jinja2FileTemplateTransfiguration):
    """
    The third phase of AttributeChainedTransfiguration to transform from the stub file
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

        self._template_file_name = stub_template_name
        self._output_file_path = Configurations.getTmpTemplateFile(output_filename)
        super().perform(context)

        jmxType = context[CTX_KEY_COMMON_COLLECTD_JMX_TYPE]
        logger.debug("======================================================================")
        logger.debug('[Transifig] Collectd-[%s] Stub [%s] ->Output [%s]', jmxType, self._template_file_name,
                     self._output_file_path)
        logger.debug("======================================================================")


class AttributeChainedTransfiguration(ChainedTransfiguration):
    """
    A chained transfiguration that transform input to a collectd genericjmx template for one
    specific attribute
    """

    def __init__(self, attr):
        """
        prepare the chain of transfiguration

        :param attr: A given attribute to replace the template-file-name string
        """
        super().__init__()
        TemplateEngineFactory.register_factory('Jinja2Engine', Jinja2Engine.Factory)

        step1 = GenerateTemplateFileNameViaPyST(attr)
        step2 = GenerateTemplateStubViaJinja2()
        step3 = GenerateTemplateOutputViaJinja2()

        self.add(step1)
        self.add(step2)
        self.add(step3)
        self._attribute = attr

    def execute(self, context):
        """
        To execute the whole series of transfiguration execution

        :param context: A key-value paired map that stores attributes carried throughput the
        whole lifecycle
        """
        logger.info("///////////////////////////////////////////////////////////////////////")
        logger.info("[ChainedTransfig] Collectd-Jmx w/ Attribute-wise [%s] ...", self._attribute)
        logger.info("///////////////////////////////////////////////////////////////////////")

        super().execute(context)

        logger.info("///////////////////////////////////////////////////////////////////////")
        logger.info("[ChainedTransfig] Collectd-Jmx w/ Attribute-wise [%s] ... COMPLETES",
                    self._attribute)
        logger.info("///////////////////////////////////////////////////////////////////////")


class ValidateCollectionTags(ContextAwareTransfiguration):
    """
    The third phase of ApplicationChainedTransfiguration to validate the collecting mbean names. This will
    invalidate the collection if the mbean name is incorrect.
    """

    def __init__(self):
        """
        prepare the transiguration

        """
        super().__init__()

    def perform(self, context):
        """
        To transfigurate while validating the mbean names out of collection list.

        :param context: A key-value paired map that stores attributes carried throughput the
        whole lifecycle
        """
        super().perform(context)

        collections = context[CTX_KEY_COMMON_COLLECTD_JMX_COLLECTIONS_SET]
        for idx, entry in enumerate(collections):
            mbean_name = entry['name']
            app_name = context[CTX_KEY_COMMON_COLLECTD_JMX_APP_PREFIX]

            if self.is_mbean_exist_in_hierarchy(
                    context[CTX_KEY_COMMON_COLLECTD_JMX_MBEANS_HIERARCHY], mbean_name, app_name):
                entry[CTX_KEY_COMMON_COLLECTD_JMX_COLLECTIONS_ENTRY_VALIDATED] = True
            elif self.is_mbean_exist_in_hierarchy(context[
                                                       CTX_KEY_COMMON_COLLECTD_JMX_MBEANS_HIERARCHY], mbean_name, 'common'):
                entry[CTX_KEY_COMMON_COLLECTD_JMX_COLLECTIONS_ENTRY_VALIDATED] = True
            else:
                entry[CTX_KEY_COMMON_COLLECTD_JMX_COLLECTIONS_ENTRY_VALIDATED] = False
                logger.warning("Collect [%s] does not exist!", mbean_name)

        jmxType = context[CTX_KEY_COMMON_COLLECTD_JMX_TYPE]
        logger.debug("======================================================================")
        logger.debug('[Transifig] Collectd-[%s] Collected mbean names validated', jmxType)
        logger.debug("======================================================================")

    def is_mbean_exist_in_hierarchy(self, hierarchy_dict, mbean_name, app_name):
        """
        Check whether mbean_name exist in hierarchy_dictionary
        :param hierarchy_dict: a dictionary that contains mbean hierarchy
        :param mbean_name: a mbean name to check against
        :param app_name: application name to look up for
        :return: True, if such mbean_name exists; False, otherwise.
        """
        if app_name in hierarchy_dict:
            lst = hierarchy_dict[app_name]
            for idx, entry in enumerate(lst):
                key = entry['name']
                if mbean_name == key:
                    logger.debug("Collect[%s] Found in [%s]", mbean_name, app_name)
                    return True
            return False
        else:
            logger.warning('dict[%s] does not exist', app_name)
            return False


class ApplicationChainedTransfiguration(ChainedTransfiguration):
    """
    A chained transfiguration that transform input to a collectd genericjmx template for one
    specific application - incomplete still and need to consolidate all parts into one final
    output with FullChainedTransfiguration
    """

    def __init__(self):
        """
        prepare the chain of transfiguration
        """
        super().__init__()
        TemplateEngineFactory.register_factory('Jinja2Engine', Jinja2Engine.Factory)

        step1 = PrepareAppConfTransfiguration()
        step2 = ConfReaderToContextTransfiguration()
        step3 = ValidateCollectionTags()
        step4 = AttributeChainedTransfiguration('mbean')
        step5 = AttributeChainedTransfiguration('connection')

        self.add(step1)
        self.add(step2)
        self.add(step3)
        self.add(step4)
        self.add(step5)


    def execute(self, context):
        """
        To execute the whole series of transfiguration execution

        :param context: A key-value paired map that stores attributes carried throughput the
        whole lifecycle
        """
        app = context[CTX_KEY_COMMON_COLLECTD_JMX_APP_PREFIX]
        logger.info("///////////////////////////////////////////////////////////////////////")
        logger.info("[ChainedTransfig] Collectd-Jmx w/ Application-wise [%s] ...", app)
        logger.info("///////////////////////////////////////////////////////////////////////")

        super().execute(context)

        logger.info("///////////////////////////////////////////////////////////////////////")
        logger.info("[ChainedTransfig] Collectd-Jmx w/ Application-wise [%s] ... "
                    "COMPLETES", app)
        logger.info("///////////////////////////////////////////////////////////////////////")


class CommonMBeansChainedTransfiguration(ChainedTransfiguration):
    """
    A chained transfiguration that transform to a collectd genericjmx template for common mbean
    definitions - incomplete still and need to consolidate all parts into one final output with
    FullChainedTransfiguration
    """

    def __init__(self):
        """
        prepare the chain of transfiguration
        """
        super().__init__()
        TemplateEngineFactory.register_factory('Jinja2Engine', Jinja2Engine.Factory)

        step1 = PrepareAppConfTransfiguration()
        step2 = ConfReaderToContextTransfiguration()
        step3 = AttributeChainedTransfiguration('mbean')

        self.add(step1)
        self.add(step2)
        self.add(step3)

    def execute(self, context):
        """
        To execute the whole series of transfiguration execution

        :param context: A key-value paired map that stores attributes carried throughput the
        whole lifecycle
        """
        logger.info("///////////////////////////////////////////////////////////////////////")
        logger.info("[ChainedTransfig] Collectd-Jmx w/ Common MBeans Generation...")
        logger.info("///////////////////////////////////////////////////////////////////////")

        #insert common to assemble collectd.genericjmx.common.conf in later step
        context[CTX_KEY_COMMON_COLLECTD_JMX_APP_PREFIX] = 'common'
        super().execute(context)

        logger.info("///////////////////////////////////////////////////////////////////////")
        logger.info("[ChainedTransfig] Collectd-Jmx w/ Common MBeans Generation... COMPLETES")
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
        inner_chain = ApplicationChainedTransfiguration()
        inner_chain.execute(context)


class ConsolidateToFinalOutput(Jinja2FileTemplateTransfiguration):
    """
    The last phase of FullChainedTransfiguration to consolidate all partial
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

        self._template_file_name = context[CTX_KEY_COMMON_COLLECTD_JMX_FULL_TEMPLATE_FILE]
        self._output_file_path = Configurations.getOutputFile(context[CTX_KEY_COMMON_COLLECTD_JMX_FINAL_OUTPUT])
        super().perform(context)

        jmxType = context[CTX_KEY_COMMON_COLLECTD_JMX_TYPE]
        logger.debug("======================================================================")
        logger.debug('[Transifig] Collectd-[%s] Consolidate [%s]->Final output [%s]',
                     jmxType, self._template_file_name, self._output_file_path)
        logger.debug("======================================================================")


class FullChainedTransfiguration(ChainedTransfiguration):
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

        step1 = CommonMBeansChainedTransfiguration()
        step2 = SpliByApplicationTransfiguration()
        step3 = ConsolidateToFinalOutput()

        self.add(step1)
        self.add(step2)
        self.add(step3)

    def execute(self, context):
        """
        To execute the whole series of transfiguration execution

        :param context: A key-value paired map that stores attributes carried throughput the
        whole lifecycle
        """
        logger.info("///////////////////////////////////////////////////////////////////////")
        logger.info("[ChainedTransfig] FULL Collectd-Jmx Transfiguration ...")
        logger.info("///////////////////////////////////////////////////////////////////////")

        super().execute(context)

        logger.info("///////////////////////////////////////////////////////////////////////")
        logger.info("[ChainedTransfig] FULL Collectd-Jmx Transfiguration ... COMPLETE")
        logger.info("///////////////////////////////////////////////////////////////////////")
