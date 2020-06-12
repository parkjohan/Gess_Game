

from Piece import Piece
from Board import Board
from Player import Player
import pygame


class GessGame:
    """The main class that creates a game of Gess, and allows a user to play."""

    def __init__(self):
        self._board = Board()
        self._game_board = self._board.get_board()
        self._game_state = 'UNFINISHED'
        self._player_turn = "Black's move"

    def print_board(self):
        """Prints the current game board."""
        for i in self._game_board:
            print(i)

    def get_board(self):
        """Returns the current board."""
        return self._game_board

    def get_game_state(self):
        """Method that returns either UNFINISHED, BLACK_WON, or WHITE_WON"""
        return self._game_state

    def get_player_turn(self):
        """Returns the current player's turn."""
        return self._player_turn

    def change_player_turn(self):
        """Updates the current player's turn to the other player after each turn."""
        turn = self.get_player_turn()  # Get current player's turn
        # If Black just made a move, change to White
        if turn == "Black's move":
            self._player_turn = "White's move"
        else:
            self._player_turn = "Black's move"

    def make_move(self, curr, new):
        """Takes two parameters for current location and desired location.
        If the desired move is legal, the game updates, and returns True. If a move is illegal
        or game is already done, it returns False."""

        temp_board = []      # Holds a temporary version of the board, which you can use to revert back to its original state
        for i in self._game_board:
            temp_board.append(list(i))

        game_state = self.get_game_state()  # If game is already won, or unfinished
        player_turn = self.get_player_turn()  # Holds current player's turn to determine who makes a move
        curr_pieces = self.get_piece_values_dict()  # Holds a dictionary of each piece location and their values

        # If game has already been won, or neither player has a ring, return False
        if game_state != 'UNFINISHED':
            return False

        # If current location is the same as desired location, return False
        if curr == new:
            return False

        # If either curr or new location value is not in the index ranges, return False
        if curr[0] not in ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's'] or new[0] not in ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm','n', 'o', 'p', 'q', 'r', 's']:
            return False
        if int(curr[1:]) not in range(1, 21) or int(new[1:]) not in range(1, 21):
            print("Location not within board ranges")
            return False

        # --------------------------- BLACK'S MOVE -----------------------------
        if player_turn == "Black's move":
            directions = ['C', 'NW', 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W']
            footprint_values = []  # List with values at each location following the order of 'directions' list
            footprint_map = {}  # A dictionary for the board values ('B', 'W', '-') at each direction of a footprint
            piece = Piece(
                curr)  # Make a black piece for current location, and get its footprint to check for legal/illegal stuff
            footprint = piece.get_piece_footprint()  # Retrieve 3x3 dictionary footprint of string locations ('a17') from Piece class for current location

            for location in footprint.values():  # Append the piece's footprint values into an array going clock-wise starting from NW
                value = self.get_value_at_location(location)
                footprint_values.append(value)
            for i in range(9):  # Create a dictionary that maps each footprint value to a direction
                footprint_map[directions[i]] = footprint_values[i]

            # Use footprint_values to determine if there are stones of another color in the footprint
            if 'W' in footprint_values or self.get_value_at_location(curr) == 'W':  # If there are enemy stones in the footprint, or an attempt at moving an enemy piece, return False
                print("There are enemy stones in the footprint and therefore is not a legal 'piece'")
                return False

            # Compare footprints to see if the attempted move is within 1-3 squares, and has the appropriate stones to match a directions move
            # Check that each movement into the desired location does not hit any other stones
            # As soon as a footprint overlaps a stone, movement must stop
            row_count = int(new[1:]) - int(curr[1:])  # If positive, move is going North, if negative, move is going South
            column_count = ord(new[0]) - ord(curr[0])  # If positive, move is going East, if negative, move is going West

            if -3 > row_count > 3 or -3 > column_count > 3 and footprint_values[0] == '-':  # If desired move is greater than 3 squares, return False
                return False

            if curr[0] == new[0] and curr[1:] != new[1:]:  # (Vertical move) Attempted move is in same column, different row. 'a16', 'a17', 'a18'
                if (0 < row_count <= 3) or (row_count > 3 and footprint_values[0] == 'B'):  # North
                    print("move is attempting to go up")
                    if footprint_values[2] == 'B':     # If there is a stone in movement direction, then continue
                        for i in range(1, row_count + 1):  # Move up then check for overlaps
                            temp_ord = ord(curr[0])  # Get coordinates of next step in player's move [row][column]
                            temp_row = int(curr[1:]) + i
                            temp_center = chr(temp_ord) + str(temp_row)
                            temp_piece = curr_pieces[temp_center]  # Temp (next) piece's values
                            # Check for overlaps with another stone before completing a move, return False if there is overlap before reaching the end of a move
                            if i == row_count and (temp_piece[1] == 'B' or temp_piece[2] == 'B' or temp_piece[3] == 'B' or temp_piece[1] == 'W' or temp_piece[2] == 'W' or temp_piece[3] == 'W'):
                                self.update_footprint(curr, new, footprint_values, 'N', row_count)
                            elif i < row_count and (
                                    temp_piece[1] == 'B' or temp_piece[2] == 'B' or temp_piece[3] == 'B' or temp_piece[
                                1] == 'W' or temp_piece[2] == 'W' or temp_piece[3] == 'W'):
                                return False
                        self.update_footprint(curr, new, footprint_values, 'N', row_count)
                    elif footprint_values[2] != 'B':
                        return False
                    if self.check_for_rings('B') is False:
                        self._game_board = temp_board
                        return False
                    if self.check_for_rings('W') is False:
                        self._game_state = "BLACK_WON"
                        return True

                if (-3 <= row_count < 0) or (row_count < -3 and footprint_values[0] == 'B'):  # South
                    print("move is attempting to go down")
                    if footprint_values[6] == 'B':
                        for i in range(1, abs(row_count) + 1):  # Move south then check for overlaps
                            temp_ord = ord(curr[0])  # Get coordinates of next step in player's move [row][column]
                            temp_row = int(curr[1:]) - i
                            temp_center = chr(temp_ord) + str(temp_row)
                            temp_piece = curr_pieces[temp_center]  # Temp (next) piece's values
                            # Check for overlaps with another stone before completing a move, return False if there is overlap before reaching the end of a move
                            if i == abs(row_count) and (temp_piece[5] == 'B' or temp_piece[6] == 'B' or temp_piece[7] == 'B'
                                                        or temp_piece[5] == 'W' or temp_piece[6] == 'W' or temp_piece[
                                                            7] == 'W'):
                                self.update_footprint(curr, new, footprint_values, 'S', abs(
                                    row_count))  # There is overlap, but it is the final location of the piece, so override overlapped stones
                            elif i < abs(row_count) and (
                                    temp_piece[5] == 'B' or temp_piece[6] == 'B' or temp_piece[7] == 'B'
                                    or temp_piece[5] == 'W' or temp_piece[6] == 'W' or temp_piece[7] == 'W'):
                                return False
                        self.update_footprint(curr, new, footprint_values, 'S', abs(row_count))
                    elif footprint_values[6] != 'B':
                        return False
                    if self.check_for_rings('B') is False:
                        self._game_board = temp_board
                        return False
                    if self.check_for_rings('W') is False:
                        self._game_state = "BLACK_WON"
                        return True

            if curr[0] != new[0] and curr[1:] == new[1:]:  # (Horizontal move) Attempted move is in same row, different column. 'a14', 'b14', 'c14'
                if (0 < column_count <= 3) or (column_count > 3 and footprint_values[0] == 'B'):  # East
                    print("move is attempting to go right")
                    if footprint_values[4] == 'B':
                        for i in range(1, column_count + 1):  # Move right and check for overlaps
                            temp_ord = ord(curr[0]) + i
                            temp_center = chr(temp_ord) + str(curr[1:])
                            temp_piece = curr_pieces[temp_center]  # Temp (next) piece's values
                            # Check for overlaps with another stone before completing a move, return False if there is overlap before reaching the end of a move
                            if i == column_count and (temp_piece[3] == 'B' or temp_piece[4] == 'B' or temp_piece[5] == 'B'
                                                      or temp_piece[3] == 'W' or temp_piece[4] == 'W' or temp_piece[
                                                          5] == 'W'):
                                self.update_footprint(curr, new, footprint_values, 'E', column_count)
                            elif i < column_count and (temp_piece[3] == 'B' or temp_piece[4] == 'B' or temp_piece[5] == 'B'
                                                       or temp_piece[3] == 'W' or temp_piece[4] == 'W' or temp_piece[5] == 'W'):
                                return False
                        self.update_footprint(curr, new, footprint_values, 'E', column_count)
                    elif footprint_values[4] != 'B':
                        return False
                    if self.check_for_rings('B') is False:
                        self._game_board = temp_board
                        return False
                    if self.check_for_rings('W') is False:
                        self._game_state = "BLACK_WON"
                        return True

                if (-3 <= column_count < 0) or (column_count < -3 and footprint_values[0] == 'B'):  # West
                    print("move is attempting to go left")
                    if footprint_values[8] == 'B':
                        for i in range(1, abs(column_count) + 1):  # Move left and check for overlaps
                            temp_ord = ord(curr[0]) - i
                            temp_center = chr(temp_ord) + str(curr[1:])
                            temp_piece = curr_pieces[temp_center]  # Temp (next) piece's values
                            # Check for overlaps with another stone before completing a move, return False if there is overlap before reaching the end of a move
                            if i == abs(column_count) and (
                                    temp_piece[1] == 'B' or temp_piece[7] == 'B' or temp_piece[8] == 'B'
                                    or temp_piece[1] == 'W' or temp_piece[7] == 'W' or temp_piece[8] == 'W'):
                                self.update_footprint(curr, new, footprint_values, 'W', abs(column_count))
                            elif i < abs(column_count) and (
                                    temp_piece[1] == 'B' or temp_piece[7] == 'B' or temp_piece[8] == 'B' or
                                    temp_piece[1] == 'W' or temp_piece[7] == 'W' or temp_piece[8] == 'W'):
                                return False
                        self.update_footprint(curr, new, footprint_values, 'W', abs(column_count))
                    elif footprint_values[8] != 'B':
                        return False
                    if self.check_for_rings('B') is False:
                        self._game_board = temp_board
                        return False
                    if self.check_for_rings('W') is False:
                        self._game_state = "BLACK_WON"
                        return True

            if curr[0] != new[0] and curr[1:] != new[1:]:  # (Diagonal move) Attempted move is in different row, different column. 'a13', 'b14', 'c15'
                if (0 < column_count <= 3 and 0 < abs(row_count) <= 3) or (footprint_values[0] == 'B' and (column_count > 3 and abs(row_count) > 3)):  # NorthEast
                    print("move is attempting to go 'NE'")
                    if footprint_values[3] == 'B':
                        for i in range(1, column_count + 1):  # Move right and up then check for overlaps
                            temp_ord = ord(curr[0]) + i  # Get coordinates of next step in player's move [row][column]
                            temp_row = int(curr[1:]) + i
                            temp_center = chr(temp_ord) + str(temp_row)
                            temp_piece = curr_pieces[temp_center]  # Temp (next) piece's values
                            # Check for overlaps with another stone before completing a move, return False if there is overlap before reaching the end of a move
                            if i == column_count and (
                                    temp_piece[1] == 'B' or temp_piece[2] == 'B' or temp_piece[3] == 'B' or temp_piece[4] == 'B' or temp_piece[5] == 'B'
                                    or temp_piece[1] == 'W' or temp_piece[2] == 'W' or temp_piece[3] == 'W' or temp_piece[
                                        4] == 'W' or temp_piece[5] == 'W'):
                                self.update_footprint(curr, new, footprint_values, 'NE', column_count)
                            elif i < column_count and (
                                    temp_piece[1] == 'B' or temp_piece[2] == 'B' or temp_piece[3] == 'B' or temp_piece[4] == 'B' or temp_piece[5] == 'B'
                                    or temp_piece[1] == 'W' or temp_piece[2] == 'W' or temp_piece[3] == 'W' or temp_piece[
                                        4] == 'W' or temp_piece[5] == 'W'):
                                return False
                        self.update_footprint(curr, new, footprint_values, 'NE', column_count)
                    elif footprint_values[3] != 'B':
                        return False
                    if self.check_for_rings('B') is False:
                        self._game_board = temp_board
                        return False
                    if self.check_for_rings('W') is False:
                        self._game_state = "BLACK_WON"
                        return True

                if (0 < column_count <= 3 and 0 > row_count >= -3) or (footprint_values[0] == 'B' and (column_count > 3 and row_count < -3)):  # SouthEast
                    print("move is attempting to go 'SE'")
                    if footprint_values[5] == 'B':
                        for i in range(1, abs(column_count) + 1):  # Move right and down then check for overlaps
                            temp_ord = ord(curr[0]) + i  # Get coordinates of next step in player's move [row][column]
                            temp_row = int(curr[1:]) - i
                            temp_center = chr(temp_ord) + str(temp_row)
                            temp_piece = curr_pieces[temp_center]  # Temp (next) piece's values
                            # Check for overlaps with another stone before completing a move, return False if there is overlap before reaching the end of a move
                            if i == abs(column_count) and (
                                    temp_piece[3] == 'B' or temp_piece[4] == 'B' or temp_piece[5] == 'B' or temp_piece[
                                6] == 'B' or temp_piece[7] == 'B'
                                    or temp_piece[3] == 'W' or temp_piece[4] == 'W' or temp_piece[5] == 'W' or temp_piece[
                                        6] == 'W' or temp_piece[7] == 'W'):
                                self.update_footprint(curr, new, footprint_values, 'SE', abs(column_count))
                            elif i < abs(column_count) and (
                                    temp_piece[1] == 'B' or temp_piece[2] == 'B' or temp_piece[3] == 'B'
                                    or temp_piece[3] == 'W' or temp_piece[4] == 'W' or temp_piece[5] == 'W' or temp_piece[
                                        6] == 'W' or temp_piece[7] == 'W'):
                                return False
                        self.update_footprint(curr, new, footprint_values, 'SE', abs(column_count))
                    elif footprint_values[5] != 'B':
                        return False
                    if self.check_for_rings('B') is False:
                        self._game_board = temp_board
                        return False
                    if self.check_for_rings('W') is False:
                        self._game_state = "BLACK_WON"
                        return True

                if (0 > column_count >= -3 and 0 < row_count <= 3) or (footprint_values[0] == 'B' and (column_count < -3 and row_count > 3)):  # NorthWest
                    print("move is attempting to go 'NW'")
                    if footprint_values[1] == 'B':
                        for i in range(1, abs(column_count) + 1):  # Move left and up then check for overlaps
                            temp_ord = ord(curr[0]) - i  # Get coordinates of next step in player's move [row][column]
                            temp_row = int(curr[1:]) + i
                            temp_center = chr(temp_ord) + str(temp_row)
                            temp_piece = curr_pieces[temp_center]  # Temp (next) piece's values
                            # Check for overlaps with another stone, if there is overlap before reaching the destination, return False
                            if i == abs(column_count) and (
                                    temp_piece[1] == 'B' or temp_piece[2] == 'B' or temp_piece[3] == 'B' or temp_piece[
                                7] == 'B' or temp_piece[8] == 'B'
                                    or temp_piece[1] == 'W' or temp_piece[2] == 'W' or temp_piece[3] == 'W' or temp_piece[
                                        7] == 'W' or temp_piece[8] == 'W'):
                                self.update_footprint(curr, new, footprint_values, 'NW', abs(column_count))
                            elif i < abs(column_count) and (
                                    temp_piece[1] == 'B' or temp_piece[2] == 'B' or temp_piece[3] == 'B' or temp_piece[
                                7] == 'B' or temp_piece[8] == 'B'
                                    or temp_piece[1] == 'W' or temp_piece[2] == 'W' or temp_piece[3] == 'W' or temp_piece[
                                        7] == 'W' or temp_piece[8] == 'W'):
                                return False
                        self.update_footprint(curr, new, footprint_values, 'NW', abs(column_count))
                    elif footprint_values[1] != 'B':
                        return False
                    if self.check_for_rings('B') is False:
                        self._game_board = temp_board
                        return False
                    if self.check_for_rings('W') is False:
                        self._game_state = "BLACK_WON"
                        return True

                if (0 > column_count >= -3 and 0 > row_count >= -3) or (footprint_values[0] == 'B' and (column_count < -3 and row_count < -3)):  # SouthWest
                    print("move is attempting to go 'SW'")
                    if footprint_values[7] == 'B':
                        for i in range(1, abs(column_count) + 1):  # Move left and down then check for overlaps
                            temp_ord = ord(curr[0]) - i  # Get coordinates of next step in player's move [row][column]
                            temp_row = int(curr[1:]) - i
                            temp_center = chr(temp_ord) + str(temp_row)
                            temp_piece = curr_pieces[temp_center]  # Temp (next) piece's values
                            # Check for overlaps with another stone before completing a move, return False if there is overlap before reaching the end of a move
                            if i == abs(column_count) and (
                                    temp_piece[1] == 'B' or temp_piece[5] == 'B' or temp_piece[6] == 'B' or temp_piece[7] == 'B' or temp_piece[8] == 'B'
                                    or temp_piece[1] == 'W' or temp_piece[5] == 'W' or temp_piece[6] == 'W' or temp_piece[
                                        7] == 'W' or temp_piece[8] == 'W'):
                                self.update_footprint(curr, new, footprint_values, 'SW', abs(column_count))
                            elif i < abs(column_count) and (
                                    temp_piece[1] == 'B' or temp_piece[5] == 'B' or temp_piece[6] == 'B' or temp_piece[7] == 'B' or temp_piece[8] == 'B'
                                    or temp_piece[1] == 'W' or temp_piece[5] == 'W' or temp_piece[6] == 'W' or temp_piece[
                                        7] == 'W' or temp_piece[8] == 'W'):
                                return False
                        self.update_footprint(curr, new, footprint_values, 'SW', abs(column_count))
                    elif footprint_values[7] != 'B':
                        return False
                    if self.check_for_rings('B') is False:
                        self._game_board = temp_board
                        return False
                    if self.check_for_rings('W') is False:
                        self._game_state = "BLACK_WON"
                        return True

            self.change_player_turn()
            return True

        # --------------------------- WHITE'S MOVE -----------------------------
        if player_turn == "White's move":
            directions = ['C', 'NW', 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W']
            footprint_values = []
            footprint_map = {}
            piece = Piece(curr)
            footprint = piece.get_piece_footprint()
            for location in footprint:
                value = self.get_value_at_location(footprint[location])
                footprint_values.append(value)
            for i in range(9):
                footprint_map[directions[i]] = footprint_values[i]

            # Use footprint_values to determine if there are stones of another color in the footprint
            if 'B' in footprint_values or self.get_value_at_location(
                    curr) == 'B':  # If there are enemy stones in the footprint, or an attempt at moving an enemy piece, return False
                print("There are enemy stones in the footprint and therefore is not a legal 'piece'")
                return False

            # Compare footprints to see if the attempted move is within 1-3 squares, and has the appropriate stones to match a directions move
            # Check that each movement into the desired location does not hit any other stones
            # As soon as a footprint overlaps a stone, movement must stop
            row_count = int(new[1:]) - int(curr[1:])  # If positive, move is going North, if negative, move is going South
            column_count = ord(new[0]) - ord(curr[0])  # If positive, move is going East, if negative, move is going West

            if -3 > row_count > 3 or -3 > column_count > 3 and footprint_values[0] == '-':  # If desired move is greater than 3 squares, return False
                return False

            # (Vertical move) Attempted move is in same column, different row. 'a16', 'a17', 'a18'
            if curr[0] == new[0] and curr[1:] != new[1:]:
                if (0 < row_count <= 3) or ((row_count > 3) and footprint_values[0] == 'W'):  # North
                    print("move is attempting to go up")
                    if footprint_values[2] == 'W':  # If there is a stone in movement direction, then continue
                        for i in range(1, row_count + 1):  # Move up then check for overlaps
                            temp_ord = ord(curr[0])  # Get coordinates of next step in player's move [row][column]
                            temp_row = int(curr[1:]) + i
                            temp_center = chr(temp_ord) + str(temp_row)
                            temp_piece = curr_pieces[temp_center]  # Temp (next) piece's values
                            # Check for overlaps with another stone before completing a move, return False if there is overlap before reaching the end of a move
                            if i == row_count and (
                                    temp_piece[1] == 'B' or temp_piece[2] == 'B' or temp_piece[3] == 'B' or temp_piece[
                                1] == 'W' or temp_piece[2] == 'W' or temp_piece[3] == 'W'):
                                self.update_footprint(curr, new, footprint_values, 'N', row_count)
                            elif i < row_count and (
                                    temp_piece[1] == 'B' or temp_piece[2] == 'B' or temp_piece[3] == 'B' or temp_piece[
                                1] == 'W' or temp_piece[2] == 'W' or temp_piece[3] == 'W'):
                                return False
                        self.update_footprint(curr, new, footprint_values, 'N', row_count)
                    elif footprint_values[2] != 'W':
                        return False
                    if self.check_for_rings('W') is False:
                        self._game_board = temp_board
                        return False
                    if self.check_for_rings('B') is False:
                        self._game_state = "WHITE_WON"
                        return True

                if (-3 <= row_count < 0) or ((-3 > row_count) and footprint_values[0] == 'W'):  # South
                    print("move is attempting to go down")
                    if footprint_values[6] == 'W':
                        for i in range(1, abs(row_count) + 1):  # Move south then check for overlaps
                            temp_ord = ord(curr[0])  # Get coordinates of next step in player's move [row][column]
                            temp_row = int(curr[1:]) - i
                            temp_center = chr(temp_ord) + str(temp_row)
                            temp_piece = curr_pieces[temp_center]  # Temp (next) piece's values
                            # Check for overlaps with another stone before completing a move, return False if there is overlap before reaching the end of a move
                            if i == abs(row_count) and (
                                    temp_piece[5] == 'W' or temp_piece[6] == 'W' or temp_piece[7] == 'W' or temp_piece[
                                5] == 'B' or temp_piece[6] == 'B' or temp_piece[7] == 'B'):
                                self.update_footprint(curr, new, footprint_values, 'S', abs(row_count))
                            elif i < abs(row_count) and (
                                    temp_piece[5] == 'W' or temp_piece[6] == 'W' or temp_piece[7] == 'W' or temp_piece[
                                5] == 'B' or temp_piece[6] == 'B' or temp_piece[7] == 'B'):
                                return False
                        self.update_footprint(curr, new, footprint_values, 'S', abs(row_count))
                    elif footprint_values[6] != 'W':
                        return False
                    if self.check_for_rings('W') is False:
                        self._game_board = temp_board
                        return False
                    if self.check_for_rings('B') is False:
                        self._game_state = "WHITE_WON"
                        return True

            # (Horizontal move) Attempted move is in same row, different column. 'a14', 'b14', 'c14'
            if curr[0] != new[0] and curr[1:] == new[1:]:
                if (0 < column_count <= 3) or ((column_count > 3) and footprint_values[0] == 'W'):  # East
                    print("move is attempting to go right")
                    if footprint_values[4] == 'W':
                        for i in range(1, column_count + 1):  # Move right and check for overlaps
                            temp_ord = ord(curr[0]) + i
                            temp_center = chr(temp_ord) + str(curr[1:])
                            temp_piece = curr_pieces[temp_center]  # Temp (next) piece's values
                            # Check for overlaps with another stone before completing a move, return False if there is overlap before reaching the end of a move
                            if i == column_count and (temp_piece[3] == 'B' or temp_piece[4] == 'B' or temp_piece[5] == 'B'
                                                      or temp_piece[3] == 'W' or temp_piece[4] == 'W' or temp_piece[5] == 'W'):
                                self.update_footprint(curr, new, footprint_values, 'E', column_count)
                            elif i < column_count and (temp_piece[3] == 'B' or temp_piece[4] == 'B' or temp_piece[5] == 'B'
                                                       or temp_piece[3] == 'W' or temp_piece[4] == 'W' or temp_piece[5] == 'W'):
                                return False
                        self.update_footprint(curr, new, footprint_values, 'E', column_count)
                    elif footprint_values[4] != 'W':
                        return False
                    if self.check_for_rings('W') is False:
                        self._game_board = temp_board
                        return False
                    if self.check_for_rings('B') is False:
                        self._game_state = "WHITE_WON"
                        return True

                if (-3 <= column_count < 0) or ((-3 > column_count) and footprint_values[0] == 'W'):  # West
                    print("move is attempting to go left")
                    if footprint_values[8] == 'W':
                        for i in range(1, abs(column_count) + 1):  # Move left and check for overlaps
                            temp_ord = ord(curr[0]) - i
                            temp_center = chr(temp_ord) + str(curr[1:])
                            temp_piece = curr_pieces[temp_center]  # Temp (next) piece's values
                            # Check for overlaps with another stone before completing a move, return False if there is overlap before reaching the end of a move
                            if i == abs(column_count) and (
                                    temp_piece[1] == 'B' or temp_piece[7] == 'B' or temp_piece[8] == 'B'
                                    or temp_piece[1] == 'W' or temp_piece[7] == 'W' or temp_piece[
                                        8] == 'W'):
                                self.update_footprint(curr, new, footprint_values, 'W', abs(column_count))
                            elif i < abs(column_count) and (
                                    temp_piece[1] == 'B' or temp_piece[7] == 'B' or temp_piece[8] == 'B' or
                                    temp_piece[1] == 'W' or temp_piece[7] == 'W' or temp_piece[8] == 'W'):
                                return False
                        self.update_footprint(curr, new, footprint_values, 'W', abs(column_count))
                    elif footprint_values[8] != 'W':
                        return False
                    if self.check_for_rings('W') is False:
                        self._game_board = temp_board
                        return False
                    if self.check_for_rings('B') is False:
                        self._game_state = "WHITE_WON"
                        return True

            # (Diagonal move) Attempted move is in different row, different column. 'a13', 'b14', 'c15'
            if curr[0] != new[0] and curr[1:] != new[1:]:
                if (0 < column_count <= 3 and 0 < row_count <= 3) or (footprint_values[0] == 'W' and (column_count > 3 and row_count > 3)):  # NE
                    print("move is attempting to go 'NE'")
                    if footprint_values[3] == 'W':
                        for i in range(1, abs(column_count) + 1):  # Move right and up then check for overlaps
                            temp_ord = ord(curr[0]) + i  # Get coordinates of next step in player's move [row][column]
                            temp_row = int(curr[1:]) + i
                            temp_center = chr(temp_ord) + str(temp_row)
                            temp_piece = curr_pieces[temp_center]  # Temp (next) piece's values
                            # Check for overlaps with another stone before completing a move, return False if there is overlap before reaching the end of a move
                            if i == column_count and (
                                    temp_piece[1] == 'B' or temp_piece[2] == 'B' or temp_piece[3] == 'B' or temp_piece[4] == 'B' or temp_piece[5] == 'B'
                                    or temp_piece[1] == 'W' or temp_piece[2] == 'W' or temp_piece[3] == 'W' or temp_piece[4] == 'W' or temp_piece[5] == 'W'):
                                self.update_footprint(curr, new, footprint_values, 'NE', row_count)
                            elif i < column_count and (
                                    temp_piece[1] == 'B' or temp_piece[2] == 'B' or temp_piece[3] == 'B' or temp_piece[4] == 'B' or temp_piece[5] == 'B'
                                    or temp_piece[1] == 'W' or temp_piece[2] == 'W' or temp_piece[3] == 'W' or temp_piece[
                                        4] == 'W' or temp_piece[5] == 'W'):
                                return False
                        self.update_footprint(curr, new, footprint_values, 'NE', row_count)
                    elif footprint_values[3] != 'W':
                        return False
                    if self.check_for_rings('W') is False:
                        self._game_board = temp_board
                        return False
                    if self.check_for_rings('B') is False:
                        self._game_state = "WHITE_WON"
                        return True

                if (0 < column_count <= 3 and 0 > row_count >= -3) or (footprint_values[0] == 'W' and (column_count > 3 and row_count < -3)):  # SE
                    print("move is attempting to go 'SE'")
                    if footprint_values[5] == 'W':
                        for i in range(1, abs(column_count) + 1):  # Move right and down then check for overlaps
                            temp_ord = ord(curr[0]) + i  # Get coordinates of next step in player's move [row][column]
                            temp_row = int(curr[1:]) - i
                            temp_center = chr(temp_ord) + str(temp_row)
                            temp_piece = curr_pieces[temp_center]  # Temp (next) piece's values
                            # Check for overlaps with another stone before completing a move, return False if there is overlap before reaching the end of a move
                            if i == abs(column_count) and (temp_piece[3] == 'B' or temp_piece[4] == 'B' or temp_piece[5] == 'B' or temp_piece[6] == 'B' or temp_piece[7] == 'B'
                                                       or temp_piece[3] == 'W' or temp_piece[4] == 'W' or temp_piece[5] == 'W' or temp_piece[6] == 'W' or temp_piece[7] == 'W'):
                                self.update_footprint(curr, new, footprint_values, 'SE', abs(row_count))
                            elif i < abs(column_count) and (temp_piece[1] == 'B' or temp_piece[2] == 'B' or temp_piece[3] == 'B'
                                                       or temp_piece[3] == 'W' or temp_piece[4] == 'W' or temp_piece[5] == 'W' or temp_piece[6] == 'W' or temp_piece[7] == 'W'):
                                return False
                        self.update_footprint(curr, new, footprint_values, 'SE', abs(row_count))
                    elif footprint_values[5] != 'W':
                        return False
                    if self.check_for_rings('W') is False:
                        self._game_board = temp_board
                        return False
                    if self.check_for_rings('B') is False:
                        self._game_state = "WHITE_WON"
                        return True

                if (0 > column_count >= -3 and 0 < row_count <= 3) or (footprint_values[0] == 'W' and (column_count < -3 and row_count > 3)):  # NW
                    print("move is attempting to go 'NW'")
                    if footprint_values[1] == 'W':
                        for i in range(1, abs(column_count) + 1):  # Move left and up then check for overlaps
                            temp_ord = ord(curr[0]) - i  # Get coordinates of next step in player's move [row][column]
                            temp_row = int(curr[1:]) + i
                            temp_center = chr(temp_ord) + str(temp_row)
                            temp_piece = curr_pieces[temp_center]  # Temp (next) piece's values
                            # Check for overlaps with another stone, if there is overlap before reaching the destination, return False
                            if i == abs(column_count) and (
                                    temp_piece[1] == 'B' or temp_piece[2] == 'B' or temp_piece[3] == 'B' or temp_piece[7] == 'B' or temp_piece[8] == 'B'
                                    or temp_piece[1] == 'W' or temp_piece[2] == 'W' or temp_piece[3] == 'W' or temp_piece[
                                        7] == 'W' or temp_piece[8] == 'W'):
                                self.update_footprint(curr, new, footprint_values, 'NW', abs(column_count))
                            elif i < abs(column_count) and (
                                    temp_piece[1] == 'B' or temp_piece[2] == 'B' or temp_piece[3] == 'B' or temp_piece[7] == 'B' or temp_piece[8] == 'B'
                                    or temp_piece[1] == 'W' or temp_piece[2] == 'W' or temp_piece[3] == 'W' or temp_piece[
                                        7] == 'W' or temp_piece[8] == 'W'):
                                return False
                        self.update_footprint(curr, new, footprint_values, 'NW', abs(column_count))
                    elif footprint_values[1] != 'W':
                        return False
                    if self.check_for_rings('W') is False:
                        self._game_board = temp_board
                        return False
                    if self.check_for_rings('B') is False:
                        self._game_state = "WHITE_WON"
                        return True

                if (0 > column_count >= -3 and 0 > row_count >= -3) or (footprint_values[0] == 'W' and (column_count < -3 and row_count < -3)):  # SW
                    print("move is attempting to go 'SW'")
                    if footprint_values[7] == 'W':
                        for i in range(1, abs(column_count) + 1):  # Move left and down then check for overlaps
                            temp_ord = ord(curr[0]) - i  # Get coordinates of next step in player's move [row][column]
                            temp_row = int(curr[1:]) - i
                            temp_center = chr(temp_ord) + str(temp_row)
                            temp_piece = curr_pieces[temp_center]  # Temp (next) piece's values
                            # Check for overlaps with another stone before completing a move, return False if there is overlap before reaching the end of a move
                            if i == abs(column_count) and (
                                    temp_piece[1] == 'B' or temp_piece[5] == 'B' or temp_piece[6] == 'B' or temp_piece[7] == 'B' or temp_piece[8] == 'B'
                                    or temp_piece[1] == 'W' or temp_piece[5] == 'W' or temp_piece[6] == 'W' or temp_piece[
                                        7] == 'W' or temp_piece[8] == 'W'):
                                self.update_footprint(curr, new, footprint_values, 'SW', abs(column_count))
                            elif i < abs(column_count) and (
                                    temp_piece[1] == 'B' or temp_piece[5] == 'B' or temp_piece[6] == 'B' or temp_piece[7] == 'B' or temp_piece[8] == 'B'
                                    or temp_piece[1] == 'W' or temp_piece[5] == 'W' or temp_piece[6] == 'W' or temp_piece[
                                        7] == 'W' or temp_piece[8] == 'W'):
                                return False
                        self.update_footprint(curr, new, footprint_values, 'SW', abs(column_count))
                    elif footprint_values[7] != 'W':
                        return False
                    if self.check_for_rings('W') is False:
                        self._game_board = temp_board
                        return False
                    if self.check_for_rings('B') is False:
                        self._game_state = "WHITE_WON"
                        return True

            self.change_player_turn()
            return True

    def get_piece_values_dict(self):
        """Helper method to calculate and return a dictionary of location: values.
           Used to update piece locations during make_move()."""
        piece_values = {}
        for i in range(1, 18):  # Loop through columns
            row = str(i + 1)
            for j in range(0, 18):  # Loop through the rows
                piece_value_array = []
                piece_value_array.clear()  # Clear the piece_value array before each iteration so the there is no mix ups
                column = chr(98 + j)
                location = str(column + row)
                piece = Piece(
                    location)  # Initialize a new piece starting at 'b2', and checking each piece's footprint for a ring
                footprint = piece.get_piece_footprint()
                for square in footprint.values():  # Loop through dictionary and make an array of piece values for each piece on the board
                    value = self.get_value_at_location(square)
                    piece_value_array.append(value)
                piece_values[location] = piece_value_array
        return piece_values

    def update_footprint(self, curr, new, values, direction, squares_moved):
        """
        Method that updates the values of each square in a footprint. Used in make_move().
        This method also handles the capturing of stones and when stones go out of the boards boundaries.
        """
        new_column = abs(ord(new[0]) - ord('a'))  # Used to retrieve coordinates of each square in new location
        new_row = abs(21 - int(new[1:]))

        old_column = ord(curr[0]) - ord('a')  # Used to retrieve coordinates of each square in old location
        old_row = 21 - int(curr[1:])

        if direction == 'C' or squares_moved == 0:
            return False

        # Update the new location with the correct piece values
        self._game_board[new_row][new_column] = values[0]  # C
        self._game_board[new_row - 1][new_column - 1] = values[1]  # NW
        self._game_board[new_row - 1][new_column] = values[2]  # N
        self._game_board[new_row - 1][new_column + 1] = values[3]  # NE
        self._game_board[new_row][new_column + 1] = values[4]  # E
        self._game_board[new_row + 1][new_column + 1] = values[5]  # SE
        self._game_board[new_row + 1][new_column] = values[6]  # S
        self._game_board[new_row + 1][new_column - 1] = values[7]  # SW
        self._game_board[new_row][new_column - 1] = values[8]  # W

        # Handle the case where piece movement causes stones to go outside the limits
        if new_column == 1:  # If there are squares that move outside the board into 'a' column, remove stones
            self._game_board[new_row][new_column - 1] = '-'
            self._game_board[new_row - 1][new_column - 1] = '-'
            self._game_board[new_row + 1][new_column - 1] = '-'
        if new_column == 18:
            self._game_board[new_row - 1][new_column + 1] = '-'
            self._game_board[new_row][new_column + 1] = '-'
            self._game_board[new_row + 1][new_column + 1] = '-'
        if new_row == 1:
            self._game_board[new_row - 1][new_column - 1] = '-'
            self._game_board[new_row - 1][new_column] = '-'
            self._game_board[new_row - 1][new_column + 1] = '-'
        if new_row == 18:
            self._game_board[new_row + 1][new_column - 1] = '-'
            self._game_board[new_row + 1][new_column] = '-'
            self._game_board[new_row + 1][new_column + 1] = '-'

        # Replace the old square values with an empty square depending on how many squares a piece moves and in which direction
        if direction == 'NW' and squares_moved == 1:  # Northwest
            self._game_board[old_row - 1][old_column + 1] = '-'  # NE
            self._game_board[old_row][old_column + 1] = '-'  # E
            self._game_board[old_row + 1][old_column + 1] = '-'  # SE
            self._game_board[old_row + 1][old_column] = '-'  # S
            self._game_board[old_row + 1][old_column - 1] = '-'  # SW
        elif direction == 'NW' and squares_moved == 2:
            self._game_board[old_row - 1][old_column + 1] = '-'  # NE
            self._game_board[old_row][old_column + 1] = '-'  # E
            self._game_board[old_row + 1][old_column + 1] = '-'  # SE
            self._game_board[old_row + 1][old_column] = '-'  # S
            self._game_board[old_row + 1][old_column - 1] = '-'  # SW
            self._game_board[old_row - 1][old_column] = '-'  # N
            self._game_board[old_row][old_column] = '-'  # C
            self._game_board[old_row][old_column - 1] = '-'  # W
        elif direction == 'NW' and squares_moved >= 3:
            self._game_board[old_row - 1][old_column + 1] = '-'  # NE
            self._game_board[old_row][old_column + 1] = '-'  # E
            self._game_board[old_row + 1][old_column + 1] = '-'  # SE
            self._game_board[old_row + 1][old_column] = '-'  # S
            self._game_board[old_row + 1][old_column - 1] = '-'  # SW
            self._game_board[old_row - 1][old_column] = '-'  # N
            self._game_board[old_row][old_column] = '-'  # C
            self._game_board[old_row][old_column - 1] = '-'  # W
            self._game_board[old_row - 1][old_column - 1] = '-'  # NW

        if direction == 'N' and squares_moved == 1:  # North
            self._game_board[old_row + 1][old_column + 1] = '-'  # SE
            self._game_board[old_row + 1][old_column] = '-'  # S
            self._game_board[old_row + 1][old_column - 1] = '-'  # SW
        elif direction == 'N' and squares_moved == 2:
            self._game_board[old_row + 1][old_column + 1] = '-'  # SE
            self._game_board[old_row + 1][old_column] = '-'  # S
            self._game_board[old_row + 1][old_column - 1] = '-'  # SW
            self._game_board[old_row][old_column] = '-'  # C
            self._game_board[old_row][old_column + 1] = '-'  # E
            self._game_board[old_row][old_column - 1] = '-'  # W
        elif direction == 'N' and squares_moved >= 3:
            self._game_board[old_row - 1][old_column] = '-'  # N
            self._game_board[old_row - 1][old_column + 1] = '-'  # NE
            self._game_board[old_row - 1][old_column - 1] = '-'  # NW
            self._game_board[old_row + 1][old_column + 1] = '-'  # SE
            self._game_board[old_row + 1][old_column] = '-'  # S
            self._game_board[old_row + 1][old_column - 1] = '-'  # SW
            self._game_board[old_row][old_column] = '-'  # C
            self._game_board[old_row][old_column + 1] = '-'  # E
            self._game_board[old_row][old_column - 1] = '-'  # W

        if direction == 'NE' and squares_moved == 1:  # Northeast
            self._game_board[old_row - 1][old_column - 1] = '-'  # NW
            self._game_board[old_row][old_column - 1] = '-'  # W
            self._game_board[old_row + 1][old_column - 1] = '-'  # SW
            self._game_board[old_row + 1][old_column] = '-'  # S
            self._game_board[old_row + 1][old_column + 1] = '-'  # SE
        elif direction == 'NE' and squares_moved == 2:
            self._game_board[old_row - 1][old_column - 1] = '-'  # NW
            self._game_board[old_row][old_column - 1] = '-'  # W
            self._game_board[old_row + 1][old_column - 1] = '-'  # SW
            self._game_board[old_row + 1][old_column] = '-'  # S
            self._game_board[old_row + 1][old_column + 1] = '-'  # SE
            self._game_board[old_row][old_column] = '-'  # C
            self._game_board[old_row - 1][old_column] = '-'  # N
            self._game_board[old_row][old_column + 1] = '-'  # E
        elif direction == 'NE' and squares_moved >= 3:
            self._game_board[old_row - 1][old_column - 1] = '-'  # NW
            self._game_board[old_row][old_column - 1] = '-'  # W
            self._game_board[old_row + 1][old_column - 1] = '-'  # SW
            self._game_board[old_row + 1][old_column] = '-'  # S
            self._game_board[old_row + 1][old_column + 1] = '-'  # SE
            self._game_board[old_row][old_column] = '-'  # C
            self._game_board[old_row - 1][old_column] = '-'  # N
            self._game_board[old_row][old_column + 1] = '-'  # E
            self._game_board[old_row - 1][old_column + 1] = '-'  # NE

        if direction == 'E' and squares_moved == 1:  # East
            self._game_board[old_row - 1][old_column - 1] = '-'  # NW
            self._game_board[old_row][old_column - 1] = '-'  # W
            self._game_board[old_row + 1][old_column - 1] = '-'  # SW
        elif direction == 'E' and squares_moved == 2:
            self._game_board[old_row - 1][old_column - 1] = '-'  # NW
            self._game_board[old_row][old_column - 1] = '-'  # W
            self._game_board[old_row + 1][old_column - 1] = '-'  # SW
            self._game_board[old_row][old_column] = '-'  # C
            self._game_board[old_row - 1][old_column] = '-'  # N
            self._game_board[old_row + 1][old_column] = '-'  # S
        elif direction == 'E' and squares_moved >= 3:
            self._game_board[old_row - 1][old_column - 1] = '-'  # NW
            self._game_board[old_row][old_column - 1] = '-'  # W
            self._game_board[old_row + 1][old_column - 1] = '-'  # SW
            self._game_board[old_row][old_column] = '-'  # C
            self._game_board[old_row - 1][old_column] = '-'  # N
            self._game_board[old_row + 1][old_column] = '-'  # S
            self._game_board[old_row][old_column + 1] = '-'  # E
            self._game_board[old_row - 1][old_column + 1] = '-'  # NE
            self._game_board[old_row + 1][old_column + 1] = '-'  # SE

        if direction == 'SE' and squares_moved == 1:  # Southeast
            self._game_board[old_row - 1][old_column - 1] = '-'  # NW
            self._game_board[old_row][old_column - 1] = '-'  # W
            self._game_board[old_row + 1][old_column - 1] = '-'  # SW
            self._game_board[old_row - 1][old_column] = '-'  # N
            self._game_board[old_row - 1][old_column + 1] = '-'  # NE
        elif direction == 'SE' and squares_moved == 2:
            self._game_board[old_row - 1][old_column - 1] = '-'  # NW
            self._game_board[old_row][old_column - 1] = '-'  # W
            self._game_board[old_row + 1][old_column - 1] = '-'  # SW
            self._game_board[old_row - 1][old_column] = '-'  # N
            self._game_board[old_row - 1][old_column + 1] = '-'  # NE
            self._game_board[old_row][old_column] = '-'  # C
            self._game_board[old_row][old_column + 1] = '-'  # E
            self._game_board[old_row + 1][old_column] = '-'  # S
        elif direction == 'SE' and squares_moved >= 3:
            self._game_board[old_row - 1][old_column - 1] = '-'  # NW
            self._game_board[old_row][old_column - 1] = '-'  # W
            self._game_board[old_row + 1][old_column - 1] = '-'  # SW
            self._game_board[old_row - 1][old_column] = '-'  # N
            self._game_board[old_row - 1][old_column + 1] = '-'  # NE
            self._game_board[old_row][old_column] = '-'  # C
            self._game_board[old_row][old_column + 1] = '-'  # E
            self._game_board[old_row + 1][old_column] = '-'  # S
            self._game_board[old_row + 1][old_column + 1] = '-'  # SE

        if direction == 'S' and squares_moved == 1:  # South
            self._game_board[old_row - 1][old_column - 1] = '-'  # NW
            self._game_board[old_row - 1][old_column] = '-'  # N
            self._game_board[old_row - 1][old_column + 1] = '-'  # NE
        elif direction == 'S' and squares_moved == 2:
            self._game_board[old_row - 1][old_column - 1] = '-'  # NW
            self._game_board[old_row - 1][old_column] = '-'  # N
            self._game_board[old_row - 1][old_column + 1] = '-'  # NE
            self._game_board[old_row][old_column - 1] = '-'  # W
            self._game_board[old_row][old_column] = '-'  # C
            self._game_board[old_row][old_column + 1] = '-'  # E
        elif direction == 'S' and squares_moved >= 3:
            self._game_board[old_row - 1][old_column - 1] = '-'  # NW
            self._game_board[old_row - 1][old_column] = '-'  # N
            self._game_board[old_row - 1][old_column + 1] = '-'  # NE
            self._game_board[old_row][old_column - 1] = '-'  # W
            self._game_board[old_row][old_column] = '-'  # C
            self._game_board[old_row][old_column + 1] = '-'  # E
            self._game_board[old_row + 1][old_column - 1] = '-'  # SW
            self._game_board[old_row + 1][old_column] = '-'  # S
            self._game_board[old_row + 1][old_column + 1] = '-'  # SE

        if direction == 'SW' and squares_moved == 1:  # Southwest
            self._game_board[old_row - 1][old_column - 1] = '-'  # NW
            self._game_board[old_row - 1][old_column] = '-'  # N
            self._game_board[old_row - 1][old_column + 1] = '-'  # NE
            self._game_board[old_row][old_column + 1] = '-'  # E
            self._game_board[old_row + 1][old_column + 1] = '-'  # SE
        elif direction == 'SW' and squares_moved == 2:
            self._game_board[old_row - 1][old_column - 1] = '-'  # NW
            self._game_board[old_row - 1][old_column] = '-'  # N
            self._game_board[old_row - 1][old_column + 1] = '-'  # NE
            self._game_board[old_row][old_column + 1] = '-'  # E
            self._game_board[old_row + 1][old_column + 1] = '-'  # SE
            self._game_board[old_row][old_column - 1] = '-'  # W
            self._game_board[old_row][old_column] = '-'  # C
            self._game_board[old_row + 1][old_column] = '-'  # S
        elif direction == 'SW' and squares_moved >= 3:
            self._game_board[old_row - 1][old_column - 1] = '-'  # NW
            self._game_board[old_row - 1][old_column] = '-'  # N
            self._game_board[old_row - 1][old_column + 1] = '-'  # NE
            self._game_board[old_row][old_column + 1] = '-'  # E
            self._game_board[old_row + 1][old_column + 1] = '-'  # SE
            self._game_board[old_row][old_column - 1] = '-'  # W
            self._game_board[old_row][old_column] = '-'  # C
            self._game_board[old_row + 1][old_column] = '-'  # S
            self._game_board[old_row + 1][old_column - 1] = '-'  # SW

        if direction == 'W' and squares_moved == 1:  # West
            self._game_board[old_row - 1][old_column + 1] = '-'  # NE
            self._game_board[old_row][old_column + 1] = '-'  # E
            self._game_board[old_row + 1][old_column + 1] = '-'  # SE
        elif direction == 'W' and squares_moved == 2:
            self._game_board[old_row - 1][old_column + 1] = '-'  # NE
            self._game_board[old_row][old_column + 1] = '-'  # E
            self._game_board[old_row + 1][old_column + 1] = '-'  # SE
            self._game_board[old_row - 1][old_column] = '-'  # N
            self._game_board[old_row][old_column] = '-'  # C
            self._game_board[old_row + 1][old_column] = '-'  # S
        elif direction == 'W' and squares_moved >= 3:
            self._game_board[old_row - 1][old_column + 1] = '-'  # NE
            self._game_board[old_row][old_column + 1] = '-'  # E
            self._game_board[old_row + 1][old_column + 1] = '-'  # SE
            self._game_board[old_row - 1][old_column] = '-'  # N
            self._game_board[old_row][old_column] = '-'  # C
            self._game_board[old_row + 1][old_column] = '-'  # S
            self._game_board[old_row - 1][old_column - 1] = '-'  # NW
            self._game_board[old_row][old_column - 1] = '-'  # W
            self._game_board[old_row + 1][old_column - 1] = '-'  # SW

    def check_for_rings(self, player):
        """Method that scans the board, and checks to see if each player has at least 1 ring each.
           If either of the players have 0 rings, it will update game state and return False.
           If there are no rings, return True"""

        black_ring = ['-', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B']
        white_ring = ['-', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']
        piece_value_array = []
        black_ring_count = 0
        white_ring_count = 0

        # Iterate through each viable ring piece on the board, and return True if both players have at least one ring
        # Update the game_state if a player has 0 rings
        for i in range(2, 18):  # Loop through columns
            row = str(i + 1)
            for j in range(1, 18):  # Loop through the rows
                piece_value_array.clear()  # Clear the piece_value array before each iteration so the there is no mix ups
                column = chr(98 + j)
                location = str(column + row)
                piece = Piece(
                    location)  # Initialize a new piece starting at 'c3', and checking the each piece's footprint for a ring
                footprint = piece.get_piece_footprint()
                for square in footprint.values():  # Loop through dictionary and make an array of piece values for each piece on the board
                    value = self.get_value_at_location(square)
                    piece_value_array.append(value)
                if piece_value_array == black_ring:  # If the piece value array matches either black/white_ring, this means it is a ring
                    black_ring_count += 1
                if piece_value_array == white_ring:
                    white_ring_count += 1
        if player == 'B':
            if black_ring_count == 0:
                return False
            else:
                return True
        if player == 'W':
            if white_ring_count == 0:
                return False
            else:
                return True

    def get_value_at_location(self, location):
        """Helper method that returns the x, y indices value on the game board,
        for example, when given a string location such as 'a17', it will return the value on the board."""

        # Used to retrieve coordinates into the 2d array game board
        column = (ord(location[0]) - ord('a'))
        row = 21 - (int(location[1:]))
        return self._game_board[row][column]

    def resign_game(self):
        """The current player who calls this method will concede the game."""
        current_player = self.get_player_turn()
        if current_player == "Black's move":
            self._game_state = "WHITE_WON"
        elif current_player == "White's move":
            self._game_state = "BLACK_WON"

