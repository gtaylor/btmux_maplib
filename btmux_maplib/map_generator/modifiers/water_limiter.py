from btmux_maplib.map_generator.modifiers.base import BaseMapModifier


class WaterLimiterModifier(BaseMapModifier):
    """
    This modifier clamps the max water depth to a certain elevation.
    """

    def __init__(self, max_water_depth):
        """

        :keyword int max_water_depth: Clamp the water at depth at this level.
        """

        assert 0 <= max_water_depth <= 9, \
            "max_water_depth must be between 0 and 9."
        self.max_water_depth = abs(max_water_depth)

    def modify_map(self, seed_val, mmap):
        """
        Override this in your sub-class.

        :param float seed_val: An value between 0.0 and 1.0 that serves as the
            map's seed. This gets passed to the heightmap and all modifiers.
        :param MuxMap mmap: The map to modify.
        """

        for y in range(0, mmap.get_map_height()):
            for x in range(0, mmap.get_map_width()):
                if mmap.terrain_list[y][x] != '~':
                    continue

                if mmap.elevation_list[y][x] > self.max_water_depth:
                    mmap.elevation_list[y][x] = self.max_water_depth
