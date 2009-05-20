"""
 BattletechMUX Map Library (btmux_maplib) 
 Copyright (C) 2008  Gregory Taylor

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from btmux_maplib.exceptions import *
from btmux_maplib.constants import TERRAIN_NAMES

class MuxMap(object):
    """
    The MuxMap class is intended to be a very minimalistic container for map
    data. It is advisable to either to push any code that does not fit into
    the 'raw map data' category into another class or sub-class.
    """
    # Dimensions tuple
    dimensions = None
    # List of hex terrain [y][x]
    terrain_list = []
    # List of hex elevations [y][x]
    elevation_list = []
    
    def __init__(self, dimensions=None):
        """
        Args:
        * size: (tuple) A tuple in the form of (width, height). If specified,
                initializes a map of this size that is all level 0 clear hexes.
                If none specified, you'll need to populate the map's data
                structures by another means (a map parser).
        """
        self.clear_map()
        if dimensions:
            self.dimensions = dimensions
            
            for y in range(0, self.get_map_height()):
                self.terrain_list.append([])
                self.elevation_list.append([])
                for x in range(0, self.get_map_width()):
                    self.terrain_list[y].append('.')
                    self.elevation_list[y].append('0')

    def clear_map(self):
        """
        Re-sets the map to its original, empty state.
        """
        self.dimensions = None
        self.terrain_list = []
        self.elevation_list = []
                  
    def get_map_dimensions(self):
        """
        Returns an (X,Y) tuple of the map's dimensions.
        """
        if not self.dimensions:
            raise MapDimsNotSet
        
        return self.dimensions
    
    def get_map_width(self):
        try:
            return self.dimensions[0]
        except TypeError:
            raise MapDimsNotSet
    
    def get_map_height(self):
        try:
            return self.dimensions[1]
        except TypeError:
            raise MapDimsNotSet
        
    def is_terrain_list_ready(self):
        """
        Returns True if the terrain list appears to be ready.
        """
        return len(self.terrain_list) > 0
    
    def is_elevation_list_ready(self):
        """
        Returns True if the elevation list appears to be ready.
        """
        return len(self.elevation_list) > 0
        
    def set_hex_terrain(self, x, y, terrain_char):
        """
        Sets a hex's terrain character.
        """
        if not self.is_terrain_list_ready():
            raise TerrainListNotSet
        
        try:
            self.terrain_list[y][x] = terrain_char
            return terrain_char
        except IndexError:
            raise InvalidHex(x, y)
        
    def set_hex_elevation(self, x, y, elevation):
        """
        Sets a hex's elevation.
        """
        if not self.is_elevation_list_ready():
            raise ElevationListNotSet
        
        try:
            if elevation < 0:
                elevation = abs(elevation)
                self.set_hex_terrain(x, y, '~')
            if elevation > 9:
                elevation = 9
            self.elevation_list[y][x] = elevation
            return elevation
        except IndexError:
            raise InvalidHex(x, y)
        
    def set_hex(self, x, y, terrain, elevation):
        """
        Sets a hex's terrain and elevation at the same time.
        """
        self.set_hex_terrain(x, y, terrain)
        self.set_hex_elevation(x, y, elevation)
    
    def get_hex_terrain(self, x, y):
        """
        Returns a hex's terrain character given an X and Y value.
        """
        if not self.is_terrain_list_ready():
            raise TerrainListNotSet
        
        try:
            return self.terrain_list[y][x]
        except IndexError:
            raise InvalidHex(x, y)
        
    def get_hex_terrain_name(self, x, y, safe_formatted=False):
        """
        Returns the full text name for the terrain.
        IE: Grassland, Mountain, etc.
        
        safe_formatted: (bool) When True, strip spaces and convert everything to
        lowercase. This is useful for retrieving graphical tiles by filename
        and other similar things.
        """
        terrain = self.get_hex_terrain(x, y)
        terrain_name = TERRAIN_NAMES.get(terrain, "Unknown")
        
        if safe_formatted:
            # Strip spaces and lowercase it.
            terrain_name = terrain_name.lower().replace(' ','')
            
        return terrain_name
        
    def get_hex_elevation(self, x, y):
        """
        Returns a hex's elevation given an X and Y value.
        """
        if not self.is_elevation_list_ready():
            raise ElevationListNotSet
        
        try:
            return int(self.elevation_list[y][x])
        except IndexError:
            raise InvalidHex(x, y)
        
    def get_hex(self, x, y):
        """
        Returns a (terrain, elevation) tuple.
        """
        return (self.get_hex_terrain(x,y),
                self.get_hex_elevation(x,y))
    
    def get_viewport(self, x, y, view_width, view_height):
        """
        Returns the upper left coordinates for a 'viewport' that
        looks at only a portion of the map. This is similar to BTMux's tactical
        map that only shows you hexes that are in your nearby vicinity.
        
        x: (int) The X coordinate that the viewport will center on.
        y: (int) The Y coordinate that the viewport will center on.
        view_width: (int) How wide the viewport should be (even number).
        view_height: (int) How high the viewport should be (even number).
        """
        try:
            # Do this for the purpose of checking hex validity.
            self.terrain_list[y][x]
        except IndexError:
            raise InvalidHex(x, y)
        
        if view_width > self.get_map_width():
            raise ViewportWidthTooBig()
        if view_height > self.get_map_height():
            raise ViewportHeightTooBig()
        
        half_w = view_width / 2
        half_h = view_height / 2
        
        x_offset = 0
        if x - half_w < 0:
            print "* Overflowed X bounds: Negative"
            x_offset = x - half_w
        elif (x + half_w) > self.get_map_width():
            print "* Overflowed X bounds: Positive"
            x_offset = (self.get_map_width() - (x + half_w) - 1) * -1
            
        y_offset = 0
        if y - half_h < 0:
            print "* Overflowed Y bounds: Negative"
            y_offset = y - half_w
        elif (y + half_h) > self.get_map_height():
            print "* Overflowed Y bounds: Positive"
            y_offset = (self.get_map_height() - (y + half_h) - 1) * -1
            
        upper_x = x - x_offset - half_w
        upper_y = y - y_offset - half_h
        
        #print "WIDTH", view_width
        #print "HEIGHT", view_height
        #print "X OFFSET", x_offset
        #print "Y OFFSET", y_offset
        #print "CENTER COORD", x, y
        #print "UPPER COORD", upper_x, upper_y
        
        return (upper_x, upper_y)