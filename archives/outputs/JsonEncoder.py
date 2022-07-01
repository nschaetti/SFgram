# -*- coding: utf-8 -*-
#

# Imports
from json import JSONEncoder


# My JSON encoder
class JsonEncoder(JSONEncoder):
    """
    My JSON encoder
    """

    # Default encoding
    def default(self, o):
        """
        default encoding
        :param o:
        :return:
        """
        return o.__dict__
    # end default

# end JsonEncoder
