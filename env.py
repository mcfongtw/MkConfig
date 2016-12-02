import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_DIR_NAME="templates"

TEST_DIR_NAME="tests"

OUTPUT_DIR_NAME="output/"

TEMP_DIR_NAME="/tmp"

class Configurations(object):

    def __init__(self):
        pass

    @staticmethod
    def getProjectRootDir():
        return ROOT_DIR

    @staticmethod
    def getProjectRootFile(fname):
        return os.path.join(Configurations.getProjectRootDir(), fname)

    @staticmethod
    def getTemplateDir():
        return os.path.join(Configurations.getProjectRootDir(), TEMPLATE_DIR_NAME)

    @staticmethod
    def getTemplateFile(fname):
        return os.path.join(Configurations.getTemplateDir(), fname)

    @staticmethod
    def getTestsDir():
        return os.path.join(Configurations.getProjectRootDir(), TEST_DIR_NAME)

    @staticmethod
    def getTestFile(fname):
        return os.path.join(Configurations.getTestsDir(), fname)

    @staticmethod
    def getOutputDir():
        return os.path.join(Configurations.getProjectRootDir(), OUTPUT_DIR_NAME)

    @staticmethod
    def getOutputFile(fname):
        return os.path.join(Configurations.getOutputDir(), fname)

    @staticmethod
    def getTempDir():
        return os.path.join(Configurations.getProjectRootDir(), TEMP_DIR_NAME)

    @staticmethod
    def getTempFile(fname):
        return os.path.join(Configurations.getTempDir(), fname)