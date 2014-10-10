import noise

from btmux_maplib.map_generator.modifiers.base import BaseMapModifier


class SimplexForestModifier(BaseMapModifier):
    """
    A simplex noise-based forest grower. This is very rudimentary. You'll
    probably get the best results by stacking multiple invocations of this
    with varying forest threses.
    """

    NOTOUCH_TERRAINS = ["^", "@", "~", "#", "-"]

    def __init__(self, frequency=20.0, octaves=3,
                 light_forest_thresh=0.2, heavy_forest_thresh=0.3,
                 seed_modifier=None):
        """

        :keyword float frequency: Adjusts the frequency of the simplex noise.
            Higher values will lead to larger chunks of forests. Smaller values
            will cause smaller clusters to be scattered all over the map.
        :keyword int octaves: The number of noise passes to make on each hex.
            Additional passes may lead to more erratic looking shapes.
        :keyword float light_forest_thresh: A float in the range of 0.0 to 1.0.
            Anything higher than this value but lower than ``heavy_forest_thresh``
            will end up a light forest.
        :param float heavy_forest_thresh: A float in the range of 0.0 to 1.0.
            Anything higher than this value will end up as a forest hex.
        :return:
        """

        self.frequency = frequency
        self.octaves = octaves
        self.light_forest_thresh = light_forest_thresh
        self.heavy_forest_thresh = heavy_forest_thresh
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
                h = noise.snoise3(
                    x=x / self.frequency,
                    y=y / self.frequency,
                    z=modded_seed,
                    octaves=self.octaves,
                )
                if h > self.heavy_forest_thresh:
                    mmap.set_hex_terrain(x, y, '"')
                elif h > self.light_forest_thresh:
                    mmap.set_hex_terrain(x, y, '`')
