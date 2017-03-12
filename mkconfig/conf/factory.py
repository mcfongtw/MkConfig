import logging
from enum import Enum

logger = logging.getLogger(__name__)


class ConfigurationType(Enum):
    """
    An enumeration for configuration type
    """
    COLLECTD_GENERIC_JMX = ('collectd_genericjmx.$attribute.inc', 'collectd',
                            'genericjmx', 'collectd_genericjmx.template')

    COLLECTD_FAST_JMX = ('collectd_fastjmx.$attribute.inc', 'collectd',
                            'fastjmx', 'collectd_fastjmx.template')

    def __init__(self, attribute_template_file, supertype, subtype, full_template_file):
        self._attr_template_file = attribute_template_file
        self._supertype = supertype
        self._subtype = subtype
        self._full_template_file = full_template_file

    def get_attribute_template_file(self):
        """
        Retrieve the attribute template file name associated with this configuration type
        """
        return self._attr_template_file

    def get_full_template_file(self):
        """
        Retrieve the attribute template file name associated with this configuration type
        """
        return self._full_template_file

    def get_supertype(self):
        """
        Retrieve the super-type name associated with this configuration type
        """
        return self._supertype

    def get_subtype(self):
        """
        Retrieve the subtype name associated with this configuration type
        """
        return self._subtype


class ConfigurationTypeFactory(object):
    """
    A Factory method that returns type of Configuration. Internal logics would retrive the associated template given a
    known type
    """

    @staticmethod
    def get_config_type(cli_attr) :
        """
        Retrieve the template type, given a cli input
        :param cli_attr: type of template to perform with

        :return: the name of template file
        """
        default_config_template = ConfigurationType.COLLECTD_GENERIC_JMX
        result = None

        if cli_attr is None:
            result = default_config_template
            logger.warning("Unsupported config type [%s]. Fall back with [%s] as default",
                           cli_attr, result)
        elif cli_attr == 'collectd_genericjmx':
            result = ConfigurationType.COLLECTD_GENERIC_JMX
            logger.debug("Located for type [%s] | templates[%s/%s]", cli_attr,
                         result.get_attribute_template_file(), result.get_full_template_file())
        elif cli_attr == 'collectd_fastjmx':
            result = ConfigurationType.COLLECTD_FAST_JMX
            logger.debug("Located for type [%s] | templates[%s/%s]", cli_attr,
                         result.get_attribute_template_file(), result.get_full_template_file())
        else:
            #default
            result = default_config_template
            logger.warning("Unsupported config type [%s]. Fall back with [%s] as default",
                           cli_attr, result)

        return result