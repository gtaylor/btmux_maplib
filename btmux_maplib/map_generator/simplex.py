import noise

from btmux_maplib.map import MuxMap
from btmux_maplib.img_generator.mapimage import PixelHexMapImage
from btmux_maplib.map_generator.base import BaseMapGenerator


class SimplexMapGenerator(BaseMapGenerator):
    oct = 1
    freq = 90.0
    seed_val = 900
        
    def _val_to_elev(self, value):
        val = value + 1.0
        val /= 0.2
        return int(val)
        
    def generate_map(self):
        mmap = MuxMap(dimensions=self.map_dimensions)
        min_val = 0
        max_val = 0
        for y in range(0, mmap.get_map_height()):
            for x in range(0, mmap.get_map_width()):
                h = noise.snoise3(
                    x=x / self.freq,
                    y=y / self.freq,
                    z=self.seed_val,
                    octaves=self.oct
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

gen = SimplexMapGenerator()
new_map = gen.generate_map()

#print "50,50 -> %d" % map.get_hex_elevation(50,10)

img = PixelHexMapImage(new_map)
#img.debug = True
img.generate_map()
img.show()
