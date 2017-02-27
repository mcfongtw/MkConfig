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

    @staticmethod
    def is_string_type(obj):
        """
        Check if given object is of string type.
        :param obj: object to check against its type
        :return: True if obj is str; False otherwise.
        """
        return isinstance(obj, str)