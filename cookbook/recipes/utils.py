import re


def kebabcase(s):
    """ Convert string to kebabcase. """

    return re.sub(r'([_ ])', '-', s).lower()
