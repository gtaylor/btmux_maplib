"""
This is an example of how to open a map file, return a MuxMap object, and
export the map to a new file. This is equivalent to copying the file, but
provides a good example of how to export maps to MUX .map files.
"""

from btmux_maplib.map_parser.fileobj import MapFileObjParser
from btmux_maplib.map_exporters.muxmap import MuxMapExporter 

# Open the original map for reading. This can be a file object via open(), or
# something like StringIO().
parser = MapFileObjParser(open('../sample_data/sample.map', 'r'))
# Show some verbose output.
parser.debug = True
# This is our new MuxMap object.
the_map = parser.get_muxmap()
# Pass the map and a file-like object to be written to. This doesn't have
# to be done with file(), it can be something else like StringIO().
exporter = MuxMapExporter(the_map, open('sample2.map', 'w'))
# Show some verbose output.
exporter.debug = True
exporter.write()
