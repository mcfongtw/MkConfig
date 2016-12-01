from core.engine import TemplateEngine
from env import Configurations
from string import Template

class PySTEngine(TemplateEngine):
    _engine = None;
    _template = None

    def __init__(self):
        super().__init__()
        print('PythonSTEngine.init()')

    def init(self, line):
        super().init()
        print('PythonSTEngine.init()')
        self._template = Template(line)


    def apply(self, context, outputFile, isInMemory=False):
        super().apply()
        print('PythonSTEngine.generate()')

        result = self._template.safe_substitute(context)
        if isInMemory:
            return result
        else:
            with open(Configurations.getTemplateFile(outputFile), 'w') as file:
                file.write(result)


    class Factory(object):
        @staticmethod
        def create(): return PySTEngine()