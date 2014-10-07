class BaseMapModifier(object):

    def modify_map(self, seed_val, mmap):
        """
        Override this in your sub-class.

        :rtype: MuxMap
        :returns: The newly generated map.
        """

        raise NotImplementedError()
