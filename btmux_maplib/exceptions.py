
class MapException(Exception):
    """
    Generic MuxMap exception class.
    """

    def __init__(self, map, value):
        self.value = value
        self.map = map

    def __str__(self):
        return repr(self.value)


class InvalidHex(Exception):
    def __init__(self, x, y):
        self.hex_x = x
        self.hex_y = y

    def __str__(self):
        return repr("Hex out of bounds: %d,%d" % (self.hex_x, self.hex_y))
    

class ViewportWidthTooBig(Exception):
    def __str__(self):
        return repr("The width of your viewport exceeds the map's width.")
    

class ViewportHeightTooBig(Exception):
    def __str__(self):
        return repr("The height of your viewport exceeds the map's width.")
    

class MapDimsNotSet(Exception):
    def __str__(self):
        return repr("Map dimensions have not been set yet.")
    

class TerrainListNotSet(Exception):
    def __str__(self):
        return repr("The terrain list has not been populated yet.")
    

class ElevationListNotSet(Exception):
    def __str__(self):
        return repr("The elevation list has not been populated yet.")
