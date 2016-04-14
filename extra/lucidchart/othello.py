# Implement the board game Othello/Reversi on the following board.
# Alternate black and white turns, and don't allow illegal moves.
#
# Extra credit: Have one human play against a computer that always
# makes a legal move.
#
# Extra extra credit: Have the computer make at least somewhat
# strategic moves rather than just some legal move.

# TODO:
# - improve on the corner / sides strategy
# - clean up generate_valid_moves func
# - random selection of who starts first
# - pygame interface
# - evolve a computer player by making it play against itself

import random
import string
from collections import defaultdict


class Player(object):
    NONE = 0
    BLACK = 1
    WHITE = 2


class Othello(object):
    ALPHA = string.ascii_letters

    def __init__(self, dim=8):
        self._dim = dim
        self._board = [[0] * dim for x in range(dim)]
        # place first four pieces
        self._place_first_pieces()
        # we start with the player with black pieces
        self._player = Player.BLACK

        self._valid_moves = {}
        self._prev_can_play = True
        self._computer_mode = False
        self._computer_strategy = 'random'
        self._self_playing = False

    def _place_first_pieces(self):
        mid = self._dim / 2
        self._board[mid-1][mid] = self._board[mid][mid-1] = Player.WHITE
        self._board[mid-1][mid-1] = self._board[mid][mid] = Player.BLACK

    def _generate_valid_moves(self):
        self._valid_moves = {}
        for x in range(self._dim):
            for y in range(self._dim):
                moves = self._generate_valid_moves_at(x, y)
                if moves:
                    self._valid_moves[(x, y)] = moves

    def _generate_valid_moves_at(self, x, y):
        def in_bound(x, y):
            return 0 <= x < self._dim and 0 <= y < self._dim

        def is_occupied(x, y):
            return self._board[x][y] != Player.NONE

        def opposite_color():
            return Player.BLACK if self._player != Player.BLACK else Player.WHITE

        def valid_in_direction(x, y, dirc, path):
            path.append((x, y))
            next_x, next_y = x + dirc[0], y + dirc[1]
            if not in_bound(next_x, next_y):
                return []
            if self._board[next_x][next_y] == self._player:
                return path
            if self._board[next_x][next_y] == opposite_color():
                return valid_in_direction(next_x, next_y, dirc, path)
            return []

        if not in_bound(x, y) or is_occupied(x, y):
            return []

        paths = []
        for direction in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]:
            next_x, next_y = x + direction[0], y + direction[1]
            if in_bound(next_x, next_y) and self._board[next_x][next_y] == opposite_color():
                path = valid_in_direction(next_x, next_y, direction, [])
                if path:
                    paths.append(path)
        return paths

    def _end_game(self):
        return not self._prev_can_play and not self._can_play()

    def _render(self):
        spacer = len(str(self._dim-1))
        print " " * spacer + " " + " ".join(a for a in Othello.ALPHA[:self._dim])
        for x in range(self._dim):
            row = "%*d" % (spacer, x)
            for y in range(self._dim):
                row += " " + self._render_space(x, y)
            print row

    def _render_space(self, x, y):
        if self._board[x][y] == Player.BLACK:
            return "B"
        elif self._board[x][y] == Player.WHITE:
            return "W"
        return " "

    def _can_play(self):
        return self._valid_moves != {}

    def _get_player_input(self):
        print "Player %s plays ..." % self._player
        x = y = -1
        try:
            row, col = raw_input('')
            x = ord(row) - ord('0')
            y = ord(col) - ord('a')
        except ValueError:
            print "Please enter a row and a column, for example: 'b3'"
        if not self._is_valid_move(x, y):
            return self._get_player_input()
        return x, y

    def _is_computer_turn(self):
        if self._self_playing:
            return True
        return self._player != Player.BLACK and self._computer_mode

    def _get_computer_input(self):
        def distance((x1, y1), (x2, y2)):
            return abs(x1 - x2) + abs(y1 - y2)

        def close_to_corner(moves):
            corners = [(0, 0), (0, self._dim-1), (self._dim-1, 0), (self._dim-1, self._dim-1)]
            # compute the dist to each corner of every valid move
            dist = [((x1, y1), distance((x1, y1), (x2, y2))) for x1, y1 in moves for x2, y2 in corners]
            # and return the coordinate with min distance
            return min(dist, key=lambda x: x[1])[0]

        # greedily attempts to capture corners
        # only attempt to do so randomly to make it a bit harder
        # to guess the computer strategy
        if random.choice((True, False)) and self._computer_strategy == 'corners':
            move = close_to_corner(self._valid_moves.keys())
        # or just select a random valid move
        else:
            move = random.choice(self._valid_moves.keys())
        print "Computer plays ..."
        print str(move[0]) + Othello.ALPHA[move[1]]
        return move

    def _is_valid_move(self, x, y):
        return (x, y) in self._valid_moves

    def _place_piece(self, x, y):
        self._board[x][y] = self._player

    def _update_board(self, x, y):
        for path in self._valid_moves[(x, y)]:
            for i, j in path:
                self._board[i][j] = self._player

    def _next_player(self):
        self._prev_can_play = self._can_play()
        self._player = Player.BLACK if self._player == Player.WHITE else Player.WHITE

    def _who_won(self):
        counts = defaultdict(int)
        for row in self._board:
            for val in row:
                counts[val] += 1

        if counts[Player.BLACK] > counts[Player.WHITE]:
            print "Color black won!"
        elif counts[Player.BLACK] < counts[Player.WHITE]:
            print "Color white won!"
        else:
            print "Draw!"

    def set_computer_mode(self):
        self._computer_mode = True

    def set_computer_strategy(self, strategy):
        self._computer_strategy = strategy

    def set_self_playing(self):
        self._self_playing = True

    def play(self):
        # generate all valid moves for first player
        self._generate_valid_moves()
        
        # the game ends when no player can play
        while not self._end_game():
            # render the board
            self._render()
            
            # if the current player can play
            if self._can_play():
                # get the user or computer input
                if self._is_computer_turn():
                    x, y = self._get_computer_input()
                else:
                    x, y = self._get_player_input()
                
                # place the piece on the board
                self._place_piece(x, y)
                
                # update the board
                self._update_board(x, y)

            # next player round
            self._next_player()

            # update all valid moves for that player
            self._generate_valid_moves()

        # determine who has won
        self._who_won()


def main():
    othello = Othello(8)
    othello.set_computer_mode()
    othello.set_computer_strategy('corners')
    othello.play()


def test():
    othello = Othello(50)
    othello.set_self_playing()
    othello.set_computer_strategy(random.choice(('corners', 'random')))
    othello.play()

if __name__ == "__main__":
    test()
    # main()
