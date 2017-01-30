import logging
import mkconfig.env

logger = logging.getLogger(__name__)

#TODO: rename to something like ConfigurationTypeFactory
class ConfigTemplateFactory(object):
    """
    A Factory method that returns type of Configuration. Internal logics would retrive the associated template given a
    known type
    """
    @staticmethod
    def get_config_tempalte(type) :
        default_config_template = 'collectd_jmx.template'

        if type is None:
            return default_config_template
        if type == 'collectd_jmx':
            return 'collectd_jmx.template'
        else:
            #default
            return default_config_template
