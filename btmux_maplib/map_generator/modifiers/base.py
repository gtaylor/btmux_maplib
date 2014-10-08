class BaseMapModifier(object):
    """
    As the name infers, a modifier runs through all of the hexes in a map
    and may make modifications as it goes.
    """

    def modify_map(self, seed_val, mmap):
        """
        Override this in your sub-class.

        :param float seed_val: An value between 0.0 and 1.0 that serves as the
            map's seed. This gets passed to the heightmap and all modifiers.
        :param MuxMap mmap: The map to modify.
        """

        raise NotImplementedError()
