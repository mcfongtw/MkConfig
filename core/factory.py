
class TemplateEngineFactory(object):
    _factories = {}

    @staticmethod
    def addFactory(id, shapeFactory):
        TemplateEngineFactory._factories[id] = shapeFactory


    # A Template Method:
    @staticmethod
    def createEngine(id):
        if id not in TemplateEngineFactory._factories:
            TemplateEngineFactory._factories[id] = eval(id + '.Factory()')
        return TemplateEngineFactory._factories[id].create()