"""
Map generator base classes and other foundational stuff.
"""


class BaseMapGenerator(object):

    def generate_map(self):
        """
        Override this in your sub-class.

        :rtype: MuxMap
        :returns: The newly generated map.
        """

        raise NotImplementedError()
