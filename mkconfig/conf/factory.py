import logging
from enum import Enum

logger = logging.getLogger(__name__)


class ConfigurationType(Enum):
    """
    An enumeration for configuration type
    """
    COLLECTD_GENERIC_JMX = ('collectd_genericjmx.$attribute.inc', 'collectd',
                            'genericjmx')

    def __init__(self, template_file, supertype, subtype):
        self._template_file = template_file
        self._supertype = supertype
        self._subtype = subtype

    def get_template_file(self):
        """
        Retrieve the template file name associated with this configuration type
        """
        return self._template_file

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
        if cli_attr == 'collectd_genericjmx':
            result = ConfigurationType.COLLECTD_GENERIC_JMX
            logger.debug("Located config type [%s]")
        else:
            #default
            result = default_config_template
            logger.warning("Unsupported config type [%s]. Fall back with [%s] as default",
                           cli_attr, result)

        return result