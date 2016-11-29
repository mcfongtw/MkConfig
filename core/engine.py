from abc import ABCMeta, abstractmethod


class TemplateEngine(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def __str__(self):
        return 'Abstract Engine class with file path {0}'.format(self._inputTemplatePath)

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def apply(self):
        pass


class TemplateEngineEnum(object) :

    @staticmethod
    def getAllShapes():
        classes = TemplateEngine.__subclasses__()
        values = []
        for clazz in classes:
            values.append(clazz.__name__)

        return values

    @staticmethod
    def valueOf(str):
        if str in TemplateEngineEnum.getAllShapes():
            return str
        else:
            return None