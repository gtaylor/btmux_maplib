"""
Map generator base classes and other foundational stuff.
"""


class BaseMapGenerator(object):

    map_dimensions = (75, 75)

    def __init__(self):
        pass

    def generate_map(self):
        """
        Override this in your sub-class.

        :rtype: MuxMap
        :returns: The newly generated map.
        """

        raise NotImplementedError
