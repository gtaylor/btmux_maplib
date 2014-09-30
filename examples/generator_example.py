"""
This is an example of how to use the map generator.
"""

from btmux_maplib.img_generator.mapimage import PixelHexMapImage
from btmux_maplib.map_generator.simplex import SimplexMapGenerator

# This holds all of the generator settings.
gen = SimplexMapGenerator(seed_val=95)
gen.map_dimensions = (80, 80)
new_map = gen.generate_map()

# Now we'll dump an image so we can see what was generated.
img = PixelHexMapImage(new_map)
img.generate_map()
img.show()
