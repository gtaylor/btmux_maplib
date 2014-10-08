
class MapGenerator(object):
    """
    This class organizes a map generation run. You pass in a heightmap that
    determines the starting set of elevations (water and clear), then we
    run through whatever modifier instances are specified (in order). The
    modifier instances add stuff like forests, mountains, cities, valleys,
    and whatever else you can think of.
    """

    def __init__(self, dimensions, seed_val, heightmap, modifiers=None):
        """
        :param tuple dimensions: A (width, height) tuple that determines the
            dimensions of the generated map.
        :param float seed_val: An value between 0.0 and 1.0 that serves as the
            map's seed. This gets passed to the heightmap and all modifiers.
        :param heightmap: One of the BaseHeightMap sub-classe instances.
            This establishes the basic topology of the map.
        :param list modifiers: A list of BaseMapModifier sub-class instances.
        """

        self.dimensions = dimensions
        self.seed_val = seed_val
        self.heightmap = heightmap
        self.modifiers = modifiers or []

    def generate_map(self):
        """
        :rtype: MuxMap
        :returns: The newly generated map.
        """

        mmap = self.heightmap.generate_height_map(self.dimensions, self.seed_val)
        for modifier in self.modifiers:
            modifier.modify_map(self.seed_val, mmap)
        return mmap
