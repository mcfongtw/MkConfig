import logging
import env

logger = logging.getLogger(__name__)

class ConfigTemplateFactory(object):

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
