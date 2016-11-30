from jinja2 import Environment, FileSystemLoader

from env import Configurations
from core.engine import TemplateEngine


class Jinja2Engine(TemplateEngine):

    _engine = None;


    def __init__(self):
        super().__init__()

    def init(self, initLoader=None):
        print('Jinja2.init()')
        if initLoader :
            jinjaLoader = initLoader
        else:
            jinjaLoader = FileSystemLoader(Configurations.getTemplateDir())
        self._engine = Environment(
            autoescape=False,
            loader=jinjaLoader,
            trim_blocks=False)

    def apply(self, context, templateName, outputFile, isInMemory=False):
        super().apply()

        print('Jinja2.generate()')


        if isInMemory :
            result = self._engine.get_template(templateName).render(context)
            return result
        else:
            result = self._engine.get_template(templateName).render(context)
            with open(Configurations.getTemplateFile(outputFile), 'w') as file:
                file.write(result)


    class Factory(object):
        @staticmethod
        def create(): return Jinja2Engine()