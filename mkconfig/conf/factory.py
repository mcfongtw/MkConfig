import logging

logger = logging.getLogger(__name__)

class ConfigurationTypeFactory(object):
    """
    A Factory method that returns type of Configuration. Internal logics would retrive the associated template given a
    known type
    """
    @staticmethod
    def get_config_tempalte(type) :
        """
        Retrieve the template file name, given a tempalte type
        :param type: type of template to perform with

        :return: the name of template file
        """
        default_config_template = 'collectd_jmx.template'

        if type is None:
            return default_config_template
        if type == 'collectd_jmx':
            return 'collectd_jmx.template'
        else:
            #default
            return default_config_template
