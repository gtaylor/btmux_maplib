"""
This is an example of how to open a map file, return a MuxMap object, and
get a few values.
"""

from btmux_maplib.map_parser.fileobj import MapFileObjParser

parser = MapFileObjParser(open('../sample_data/sample.map', 'r'))
# This is our new MuxMap object.
the_map = parser.get_muxmap()
print "Map width: %d" % the_map.get_map_width()
print "Map height: %d" % the_map.get_map_height()
print "Terrain at 158,54: %s (%s)" % (the_map.get_hex_terrain(158, 54),
                                      the_map.get_hex_terrain_name(158, 54))
print "Elevation at 158,54: %d" % the_map.get_hex_elevation(158, 54)
print "Window View - Upper Left Point: %s,%s" % the_map.get_viewport(0, 0, 10, 10)
