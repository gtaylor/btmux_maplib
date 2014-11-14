import logging

from btmux_maplib.map import MuxMap

logger = logging.getLogger(__name__)


class MapFileObjParser(object):
    """
    This class parses a map from any file-like Python object that supports
    readlines(). The most common usage is with open() or StringIO(). 
    From here you may return a MuxMap with get_muxmap().
    """

    # Stores the map data as a string.
    map_string = None
    # Reference to the file-like object to save to.
    fobj = None
    # A tuple of the map's dimensions (X,Y).
    dimensions = None
    # When True, print debug stuff to stdio.
    debug = False
    
    def __init__(self, fileobj):
        """
        Pass a file-like Python object that supports readlines() in, and
        set the parser up for parsing.
        """

        self.fobj = fileobj
        self.map_string = fileobj.readlines()
        # Dimensions are on the first line of the map file.
        dimensions_str = self.map_string[0].split()
        # Store the dimensions in a tuple to prevent tampering.
        self.dimensions = (int(dimensions_str[0]), int(dimensions_str[1]))
               
    def get_map_dimensions(self):
        return self.dimensions
    
    def get_map_width(self):
        return self.get_map_dimensions()[0]
    
    def get_map_height(self):
        return self.get_map_dimensions()[1]
        
    def get_hex_terrain(self, x, y):
        return self.map_string[y + 1][x * 2]
    
    def get_hex_elevation(self, x, y):
        return int(self.map_string[y + 1][(x * 2) + 1])
    
    def get_muxmap(self):
        """
        Returns a MuxMap object with the terrain/hexes populated.
        """

        mmap = MuxMap()
        mmap.dimensions = self.get_map_dimensions()

        if getattr(self.fobj, "name"):
            logger.debug("Parsing MUX map from %s", self.fobj.name)
        else:
            logger.debug("Parsing MUX map")
            
        # Iterate through our string map data and set up the Lists on the
        # new map object.
        for y in range(0, self.get_map_height()):
            mmap.terrain_list.append([])
            mmap.elevation_list.append([])
            for x in range(self.get_map_width()):
                mmap.terrain_list[y].append(self.get_hex_terrain(x, y))
                mmap.elevation_list[y].append(self.get_hex_elevation(x, y))

        logger.debug("Parsing completed. Map dimensions are %dx%d.",
            mmap.get_map_width(), mmap.get_map_height())
            
        # Done parsing and storing, bombs away.
        return mmap
