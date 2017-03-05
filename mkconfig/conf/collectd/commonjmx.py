import logging

import yaml

from mkconfig.conf.collectd.context import CTX_KEY_COLLECTD_COMMON_JMX_APP_CONF_DIR, \
    CTX_KEY_COLLECTD_COMMON_JMX_CONF_YAML_FILE, CTX_KEY_COLLECTD_COMMON_JMX_APP_PREFIX, \
    CTX_KEY_COLLECTD_COMMON_JMX_MBEANS_SET, \
    CTX_KEY_COLLECTD_COMMON_JMX_TYPE
from mkconfig.conf.utils import Utils
from mkconfig.core.transfig import ContextAwareTransfiguration, YamlFileReaderToContextTransfiguration

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
        appName = context[CTX_KEY_COLLECTD_COMMON_JMX_APP_PREFIX]
        jmxType = context[CTX_KEY_COLLECTD_COMMON_JMX_TYPE]

        appConfYamlFile = context[CTX_KEY_COLLECTD_COMMON_JMX_APP_CONF_DIR] + "collectd." + jmxType + "." + appName + '.conf.yaml'
        self.validate_file_exist(appConfYamlFile)
        context[CTX_KEY_COLLECTD_COMMON_JMX_CONF_YAML_FILE] = appConfYamlFile
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

    def __init__(self, keyName = CTX_KEY_COLLECTD_COMMON_JMX_CONF_YAML_FILE):
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

        for idx, mbean in enumerate(context[CTX_KEY_COLLECTD_COMMON_JMX_MBEANS_SET]):
            self.patch_mbean_table_value(mbean)
            #mbean is updated
            context[CTX_KEY_COLLECTD_COMMON_JMX_MBEANS_SET][idx] = mbean

    def patch_mbean_table_value(self, mbean):
        """
        Patch the specific mbean attribute

        :param mbean: mbean attribute to be patched
        """
        for attribute in mbean['attributes']:
            if 'Table' in attribute:
                value = attribute['Table']
                attribute['Table'] = Utils.boolean_to_lowercase_literal(value)

        logger.debug(mbean)
