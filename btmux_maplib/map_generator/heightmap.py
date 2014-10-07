import logging

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

    def __init__(self, frequency=90.0, octaves=1):
        self.frequency = frequency
        self.octaves = octaves
        
    def _val_to_elev(self, value):
        val = value + 1.0
        val /= 0.2
        return int(val)
        
    def generate_height_map(self, dimensions, seed_val):
        mmap = MuxMap(dimensions=dimensions)
        min_val = 0
        max_val = 0
        for y in range(0, mmap.get_map_height()):
            for x in range(0, mmap.get_map_width()):
                h = noise.snoise3(
                    x=x / self.frequency,
                    y=y / self.frequency,
                    z=seed_val,
                    octaves=self.octaves
                )
                if h < min_val:
                    min_val = h
                if h > max_val:
                    max_val = h
                elev = self._val_to_elev(h)
                #print "%d,%d -> %d" % (x,y,elev)
                mmap.set_hex_elevation(x, y, elev)
                #print "N%d" %self.map.get_hex_elevation(x, y, )
                #time.sleep(0.01)
        return mmap