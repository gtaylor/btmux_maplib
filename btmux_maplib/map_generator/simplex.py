import logging
import random

import noise

from btmux_maplib.map import MuxMap
from btmux_maplib.map_generator.base import BaseMapGenerator

logger = logging.getLogger(__name__)


class SimplexMapGenerator(BaseMapGenerator):

    def __init__(self, seed_val=None, frequency=90.0, octaves=1,
                 dimensions=(80, 80)):
        self.seed_val = seed_val or random.randint(0, 99999999)
        self.frequency = frequency
        self.octaves = octaves
        self.dimensions = dimensions
        
    def _val_to_elev(self, value):
        val = value + 1.0
        val /= 0.2
        return int(val)
        
    def generate_map(self):
        mmap = MuxMap(dimensions=self.dimensions)
        min_val = 0
        max_val = 0
        for y in range(0, mmap.get_map_height()):
            for x in range(0, mmap.get_map_width()):
                h = noise.snoise3(
                    x=x / self.frequency,
                    y=y / self.frequency,
                    z=self.seed_val,
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
