import logging


logger = logging.getLogger(__name__)


class Utils(object):
    """
    Utilities functions
    """

    @staticmethod
    def boolean_to_lowercase_literal(value):
        """
        Convert the boolean value into a lowercase literal value
        :param value: a boolean value to convert with
        :return: a lowercase literal value equivalent to value, if it is of type boolean
        """
        if isinstance(value, bool):
            value = str(value).lower()
        return value