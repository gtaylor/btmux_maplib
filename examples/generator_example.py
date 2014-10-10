"""
This is an example of how to use the map generator.
"""

import random

from btmux_maplib.img_generator.mapimage import PixelHexMapImage
from btmux_maplib.map_generator.map_generator import MapGenerator
from btmux_maplib.map_generator.heightmap import SimplexHeightHeightMap
from btmux_maplib.map_generator.modifiers.forests import SimplexForestModifier
from btmux_maplib.map_generator.modifiers.mountains import \
    SimplexMountainModifier
from btmux_maplib.map_generator.modifiers.water_limiter import \
    WaterLimiterModifier


# The MapGenerator groups together a heightmap (which creates the basic
# topology of the map) and an optional set of modifier instances, which
# fill in forests, mountains, cities, roads, and whatever else you'd like to
# add to the barren map.
gen = MapGenerator(
    dimensions=(100, 100),
    seed_val=random.random(),
    #seed_val=0.507391753985,
    heightmap=SimplexHeightHeightMap(),
    modifiers=[
        WaterLimiterModifier(max_water_depth=0),
        # The default values give us numerous, but smaller forest clusters.
        SimplexForestModifier(seed_modifier=0.4),
        # Do a second pass with a different seed and larger forests.
        SimplexForestModifier(
            frequency=40.0, seed_modifier=0.2, light_forest_thresh=0.1,
            heavy_forest_thresh=0.2
        ),
        # We'll make all hexes above elevation 6 in this case, but you can
        # elect to use the defaults for more randomized mountain conversions.
        SimplexMountainModifier(
            mountain_thresh=-1.0, minimum_elevation=6
        ),
    ],
)
new_map = gen.generate_map()

# Now we'll dump an image so we can see what was generated.
img = PixelHexMapImage(new_map)
img.generate_map()
img.show()
