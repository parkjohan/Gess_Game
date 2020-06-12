


class Piece:
    """A Piece class for making a piece object and its 3x3 footprint."""

    def __init__(self, center):
        self._center = center

    def get_piece_footprint(self):
        """A method that takes a location of a piece on the board, and returns a 3x3 footprint of the surrounding locations."""
        footprint = {}
        location_column = ord(self._center[0])
        location_row = int(self._center[1:])

        # Add each piece's coordinates to 'footprint' dictionary
        footprint['C'] = self._center
        footprint['NW'] = chr(location_column - 1) + str(location_row + 1)
        footprint['N'] = chr(location_column) + str(location_row + 1)
        footprint['NE'] = chr(location_column + 1) + str(location_row + 1)
        footprint['E'] = chr(location_column + 1) + str(location_row)
        footprint['SE'] = chr(location_column + 1) + str(location_row - 1)
        footprint['S'] = chr(location_column) + str(location_row - 1)
        footprint['SW'] = chr(location_column - 1) + str(location_row - 1)
        footprint['W'] = chr(location_column - 1) + str(location_row)

        return footprint

