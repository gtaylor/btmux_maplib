import noise

from btmux_maplib.map_generator.modifiers.base import BaseMapModifier


class SimplexMountainModifier(BaseMapModifier):
    """
    A simplex noise-based mountain setter. This is very rudimentary.
    """

    NOTOUCH_TERRAINS = ["@", "~", "#", "-"]

    def __init__(self, frequency=40.0, octaves=3,
                 mountain_thresh=0.2, minimum_elevation=6,
                 seed_modifier=None):
        """

        :keyword float frequency: Adjusts the frequency of the simplex noise.
            Higher values will lead to larger individual mountainous patches.
            Smaller values will cause smaller clusters to be scattered all
            over the map.
        :keyword int octaves: The number of noise passes to make on each hex.
            Additional passes may lead to more erratic looking shapes.
        :keyword float mountain_thresh: A float in the range of 0.0 to 1.0.
            Anything higher than this value will end up as a mountain hex.
        :param int minimum_elevation: Only hexes higher than this elevation
            will be considered for mountainizing.
        :return:
        """

        self.frequency = frequency
        self.octaves = octaves
        self.mountain_thresh = mountain_thresh
        self.minimum_elevation = minimum_elevation
        self.seed_modifier = seed_modifier

    def modify_map(self, seed_val, mmap):
        """
        :param float seed_val: An value between 0.0 and 1.0 that serves as the
            map's seed. This gets passed to the heightmap and all modifiers.
        :param MuxMap mmap: The map to modify.
        """

        modded_seed = self._get_modified_seed_val(seed_val, self.seed_modifier)

        for y in range(0, mmap.get_map_height()):
            for x in range(0, mmap.get_map_width()):
                if mmap.terrain_list[y][x] in self.NOTOUCH_TERRAINS:
                    continue
                if mmap.elevation_list[y][x] < self.minimum_elevation:
                    continue
                h = noise.snoise3(
                    x=x / self.frequency,
                    y=y / self.frequency,
                    z=modded_seed,
                    octaves=self.octaves,
                )
                if h > self.mountain_thresh:
                    mmap.set_hex_terrain(x, y, '^')
