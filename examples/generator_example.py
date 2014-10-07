"""
This is an example of how to use the map generator.
"""

import random

from btmux_maplib.img_generator.mapimage import PixelHexMapImage
from btmux_maplib.map_generator.map_generator import MapGenerator
from btmux_maplib.map_generator.heightmap import SimplexHeightHeightMap


# The MapGenerator groups together a heightmap (which creates the basic
# topology of the map) and an optional set of modifier instances, which
# fill in forests, mountains, cities, roads, and whatever else you'd like to
# add to the barren map.
gen = MapGenerator(
    dimensions=(80, 80),
    seed_val=random.randint(0, 99999999),
    heightmap=SimplexHeightHeightMap(),
    modifiers=[],
)
new_map = gen.generate_map()

# Now we'll dump an image so we can see what was generated.
img = PixelHexMapImage(new_map)
img.generate_map()
img.show()
