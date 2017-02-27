import os
from logging.config import dictConfig
import logging


def setup_logging_with_details():
    setup_logging(True)


def setup_logging(is_test = False) :

    if is_test:
        default_log_lvl = logging.DEBUG
    else:
        default_log_lvl = logging.INFO

    logging_config = dict(
        version = 1,
        formatters =
        {
            'default':
                {
                    'format' : '%(asctime)s %(name)-25s %(levelname)-8s %(message)s'
                }
        },
        handlers =
        {
            'default':
                {
                    'class': 'logging.StreamHandler',
                    'formatter': 'default',
                    'level': default_log_lvl
                }
        },
        root =
        {
            'handlers': ['default'],
            'level': default_log_lvl,
            'propagate': True
        },
    )

    dictConfig(logging_config)


###########################################

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_DIR_NAME="templates"

TEST_DIR_NAME="tests"

OUTPUT_DIR_NAME="output/"

TEMP_DIR_NAME="/tmp"

logger = logging.getLogger(__name__)

class Configurations(object):
    """
    A class that defines all type of configurations or global (env) settings.
    """
    def __init__(self):
        pass

    @staticmethod
    def getProjectRootDir():
        """
        Get the dir path of this project/
        """
        return ROOT_DIR

    @staticmethod
    def getProjectRootFile(fname):
        """
        Get the file path under project/
        :param fname: name of file under specific dir
        """
        return os.path.join(Configurations.getProjectRootDir(), fname)

    @staticmethod
    def getTemplateDir():
        """
        Get the dir path of templates, project/templates/
        """
        return os.path.join(Configurations.getProjectRootDir(), TEMPLATE_DIR_NAME)

    @staticmethod
    def getTemplateFile(fname):
        """
        Get the file path under project/templates/
        :param fname: name of file under specific dir
        """
        return os.path.join(Configurations.getTemplateDir(), fname)


    @staticmethod
    def getOutputDir():
        """
        Get the dir path of project/tests/
        """
        directory = os.path.join(Configurations.getProjectRootDir(), OUTPUT_DIR_NAME)
        if not os.path.exists(directory):
            logger.warning('Directory %s not exist, CREATE!', directory)
            os.makedirs(directory)

        return directory

    @staticmethod
    def getOutputFile(fname):
        """
        Get the file path under /project/tests/
        :param fname: name of file under specific dir
        """
        return os.path.join(Configurations.getOutputDir(), fname)

    @staticmethod
    def getSystemTmpDir():
        """
        Get the dir pth of system temp, /tmp/
        """
        return os.path.join(Configurations.getProjectRootDir(), TEMP_DIR_NAME)

    @staticmethod
    def getTmpTemplateDir():
        """
        Get the temporary templates dir path, /tmp/templates/
        """
        directory = os.path.join(Configurations.getSystemTmpDir(), TEMPLATE_DIR_NAME);
        if not os.path.exists(directory):
            logger.warning('Directory %s not exist, CREATE!', directory)
            os.makedirs(directory)
        return directory

    @staticmethod
    def getTmpTemplateFile(fname):
        """
        Get the file path under /tmp/templates/
        :param fname: name of file under specific dir
        """
        return os.path.join(Configurations.getTmpTemplateDir(), fname)

