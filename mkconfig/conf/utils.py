import logging
import mkconfig.env


logger = logging.getLogger(__name__)


class Utils(object):
    """
    Utilities functions
    """

    @staticmethod
    def boolean_to_lowercase_literal(value):
        if isinstance(value, bool):
            value = str(value).lower()
        return value