import logging

logger = logging.getLogger(__name__)


class MuxMapExporter(object):
    """
    Saves as map as a MUX .map file.
    """

    # Reference to the map object to save.
    map = None
    # Reference to the file-like object to save to.
    fobj = None
    # When True, print debug stuff to stdio.
    debug = False
    
    def __init__(self, mmap, fileobj):
        self.map = mmap
        self.fobj = fileobj
        
    def write(self):
        """
        Writes the map to the specified file.
        """
        if getattr(self.fobj, "name", None):
            logger.debug("Writing MUX map to: %s", self.fobj.name)
            
        self.fobj.writelines(self.map_lines())
        
    def close(self):
        """
        Closes the file descriptor.
        """

        self.fobj.close()
        
    def map_lines(self):
        """
        Returns a string containing what would be written to a .map file.
        """

        hex_rows = []
        for y in range(0, self.map.get_map_height()):
            hex_rows.append([])
            hex_rows[y] = ""
            for x in range(self.map.get_map_width()):
                hex_rows[y] += "%s%s" % (
                    self.map.get_hex_terrain(x, y),
                    self.map.get_hex_elevation(x, y))
            hex_rows[y] += "\n"
            
        hex_rows.insert(0, "%d %d\n" % (
            self.map.get_map_width(),
            self.map.get_map_height()))
        return hex_rows
