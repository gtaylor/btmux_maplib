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

    def _get_modified_seed_val(self, seed_val, seed_mul):
        """
        If you want people to be able to stack multiple calls of the modifier,
        but with different seed values, this will calculate said modified seed.

        :param float seed_val: The seed value to modify.
        :type seed_mul: float or None
        :param seed_mul: Multiply the seed by this. If None, don't modify seed.
        :rtype: float
        :returns: A modified seed value.
        """

        if not seed_mul:
            return seed_val
        return seed_val * seed_mul
