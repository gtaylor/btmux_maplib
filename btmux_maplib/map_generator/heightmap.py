"""
The classes in this module are for generating the initial MuxMap instance.
It won't have any terrain aside from clear/grass and water.
"""

import logging
import math

import noise

from btmux_maplib.map import MuxMap

logger = logging.getLogger(__name__)


class BaseHeightMap(object):
    """
    Don't use this class directly! This serves as our protocol for height map
    classes.
    """

    def generate_height_map(self, dimensions, seed_val):
        """
        Override this in your sub-class.

        :param tuple dimensions: A (width, height) tuple that determines the
            dimensions of the generated map.
        :param int seed_val: An integer value that seeds the heightmap generator.
        :rtype: MuxMap
        :returns: The newly generated map.
        """

        raise NotImplementedError()


class SimplexHeightHeightMap(BaseHeightMap):
    """
    Uses the 'noise' module's Simplex Noise algorithm to generator a basic
    heightmap. All hexes will either be Clear or Water, based on elevation.
    """

    def __init__(self, frequency=100.0, octaves=3, watertable_mod=-0.5):
        """

        :keyword float frequency: Adjusts the frequency of the simplex noise.
            A higher value here will result in smoother terrain.
        :keyword int octaves: The number of noise passes to make on each hex.
            Additional passes may lead to more erratic looking shapes.
        :keyword float watertable_mod: A value between -1.0 and 1.0. This
            causes the water table to lower (lower numbers) or rise (higher
            numbers). The default favors more land mass than water.
        :return:
        """

        self.frequency = frequency
        self.octaves = octaves
        # Invert this so it ends up being a value that we can add to the
        # generated hex elevations.
        self.watertable_mod = watertable_mod * -1
        
    def _val_to_elev(self, value, land_elev_divisor):
        """
        Simplex Noise is in the range of -1.0 to 1.0. This leads to around a
        50% water to land ratio. We typically need more land than water for
        most BTMuxs. Any value >= 0.0 is dry land, and anything below
        less is water.

        To make sure we are ending up with more land, we have a notion of
        a water table modifier. This is a value that gets added directly
        to the noise value for each hex. This extends our maximum range
        past 1.0, but we account for that by adjusting our division for
        any hexes above 0.0 (dry land).

        Our math remains simple, but we reduce the depth and quantity of
        any water bodies.

        :param float value: A noise value, between -1.0 and 1.0.
        :param float land_elev_divisor: If the value is >= 0.0 (dry land),
            divide by this amount to see what Z elevation the hex is.
        :rtype: int
        :returns: The height of the hex.
        """

        value += self.watertable_mod
        if value < 0.0:
            elev = math.floor(value / 0.1)
        else:
            elev = math.floor(value / land_elev_divisor)

        return min(9, max(-9, elev))
        
    def generate_height_map(self, dimensions, seed_val):
        """
        Generates a height map in the form of a MuxMap with nothing but clear
        hexes and water.

        :keyword tuple dimensions: A (width, height) tuple that determines the
            dimensions of the generated map.
        :param int seed_val: An integer value that serves as the map's seed.
        :rtype: MuxMap
        :returns: A heightmap in the form of a MuxMap.
        """

        max_elev = 1.0 + self.watertable_mod
        land_elev_divisor = max_elev / 9.0

        mmap = MuxMap(dimensions=dimensions)
        for y in range(0, mmap.get_map_height()):
            for x in range(0, mmap.get_map_width()):
                h = noise.snoise3(
                    x=x / self.frequency,
                    y=y / self.frequency,
                    z=seed_val,
                    octaves=self.octaves,
                )
                elev = self._val_to_elev(h, land_elev_divisor)
                #print "%d,%d -> %d" % (x,y,elev)
                mmap.set_hex_elevation(x, y, elev)
                #print "N%d" %self.map.get_hex_elevation(x, y, )
                #time.sleep(0.01)
        return mmap
