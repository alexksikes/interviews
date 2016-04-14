# Chap 17 - Moderate
import copy
from collections import defaultdict


# 17.2
# Design an algorithm to figure if someone has won at the
# game of tic-tac-toe.
#
# Follow up: Generalize to a NxN board
class TicTacToe(object):
    def __init__(self, board):
        self._size = len(board)
        self._board = board

    def is_occupied(self, i, j):
        return self._board[i][j] != 0

    def is_in_board(self, i, j):
        return 0 <= i < self._size and 0 <= j < self._size

    def has_won(self):
        def three_in_row(i, j, inc_i, inc_j):
            return (self.is_occupied(i, j) and self._board[i][j]
                    == self._board[i+inc_i][j+inc_j]
                    == self._board[i+2*inc_i][j+2*inc_j])

        def check_row(i):
            j = 0
            while self.is_in_board(i, j+2):
                if three_in_row(i, j, 0, 1):
                    return self._board[i][j]
                j += 1

        def check_col(j):
            i = 0
            while self.is_in_board(i+2, j):
                if three_in_row(i, j, 1, 0):
                    return self._board[i][j]
                i += 1

        def check_diag(i, j, inc_i=1, inc_j=1):
            while self.is_in_board(i+2*inc_i, j+2*inc_j):
                if three_in_row(i, j, inc_i, inc_j):
                    return self._board[i][j]
                i += inc_i
                j += inc_j

        won, i = None, 0
        while not won and i < self._size:
            won = (check_row(i) or check_col(i)
                or check_diag(0, i)
                or check_diag(0, i, inc_j=-1)  # crossed diagonal
                or check_diag(i, 0)
                or check_diag(self._size-1, i, inc_i=-1))  # crossed diagonal
            i += 1
        return won

assert TicTacToe([
    [1, 1, 1],
    [2, 1, 2],
    [1, 2, 2]
]).has_won() == 1

assert TicTacToe([
    [1, 1, 1],
    [2, 1, 2],
    [1, 2, 2]
]).has_won() == 1

assert TicTacToe([
    [1, 1, 2],
    [2, 1, 2],
    [0, 1, 0]
]).has_won() == 1

assert TicTacToe([
    [1, 2, 1],
    [2, 1, 2],
    [1, 2, 1]
]).has_won() == 1

assert not TicTacToe([
    [1, 2, 1],
    [1, 1, 2],
    [2, 1, 2]
]).has_won()

assert TicTacToe([
    [1, 0, 2],
    [1, 1, 2],
    [2, 1, 2]
]).has_won() == 2

assert TicTacToe([
    [2, 1, 0],
    [1, 2, 0],
    [0, 1, 2]
]).has_won() == 2

assert TicTacToe([
    [0,0,2,0,0,2,0,0,0],
    [0,1,0,0,2,0,0,0,0],
    [0,0,1,0,0,0,2,0,0],
    [0,1,0,1,0,0,0,0,0],
    [0,0,0,0,1,0,0,0,0],
    [0,2,0,1,0,0,0,2,0],
    [0,2,0,0,2,0,0,1,0],
    [0,0,0,1,2,0,1,2,0],
    [2,0,1,0,1,0,1,0,0]
]).has_won() == 1


# 17.3
# Write an algorithm to count the number of trailing zeroes
# in n factorial.
def num_trailing_zeroes(n):
    def count_tens(n):
        count = 0
        while n % 5 == 0:
            count += 1
            n /= 5
        return count

    sum = 0
    for i in range(1, n+1):
        sum += count_tens(i)
    return sum


def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)

assert num_trailing_zeroes(5) == 1
assert num_trailing_zeroes(25) == 6
assert num_trailing_zeroes(30) == 7


# 17.6
# Given an array of integers, write a method to find m and n such
# that if you sorted the elements m through n, the entire array
# would be sorted. Minimize n - m, find the smallest such sequence.

# Example:
# 1, 2, 4, 7, 10, 11, 7, 12, 6, 7, 16, 18, 19
# output: (3, 9)
def find_unsorted_array(l):
    l = 1
    while l < len(a) and a[l-1] < a[l]:
        l += 1
    r = len(a)-2
    while r > 0 and a[r] < a[r+1]:
        r -= 1
    if r < l:
        return (0, 0)

    _min, _max = min(a[l:r+1]), max(a[l:r+1])
    m = l
    while m-1 >= 0 and a[m-1] > _min:
        m -= 1
    n = r
    while n+1 < len(a) and a[n+1] < _max:
        n += 1
    return m, n

a = [1, 2, 4, 7, 10, 11, 7, 12, 6, 7, 16, 18, 19]
assert find_unsorted_array(a) == (4, 9)
a = [5, 10, 5, 2, 1, 0]
assert find_unsorted_array(a) == (0, 5)
a = [1, 2, 3, 4, 5]
assert find_unsorted_array(a) == (0, 0)


# 17.8
# Find the contiguous sequence of integers in array with
# the largest sum.
def largest_sum_seq(a):
    sum, best_sum = 0, 0
    seq, best_seq = [], []
    for e in a:
        sum += e
        seq.append(e)
        if sum > best_sum:
            best_sum, best_seq = sum, copy.copy(seq)
        if sum < 0:
            sum, seq = 0, []
    return best_seq

a = [-2, 3, 4, -10, 9, -4, 7, -8, -1, -1, -3, 4, 5, -10, 7, 0, -9]
assert largest_sum_seq(a) == [9, -4, 7]


# 17.12
# Design an algorithm to find all pairs of integers within
# an array which sum to a specified value
def find_pairs(a, sum):
    d, pairs = {}, []
    for x in a:
        if x in d:
            pairs.append((x, d[x]))
        else:
            d[sum - x] = x
    return pairs


def find_pairs2(a, sum):
    pairs, a = [], sorted(a)
    i, j = 0, len(a)-1
    while i < j:
        x, y = a[i], a[j]
        if x + y == sum:
            pairs.append((x, y))
            i += 1
            j -= 1
        elif x + y < sum:
            i += 1
        else:
            j -= 1
    return pairs


a = [9, 4, 7, 8, 1, 1, 3, 4, 5, 10, 7, 0, 9]
assert find_pairs(a, 10) == [(1, 9), (1, 9), (3, 7), (0, 10)]
assert find_pairs(a, 2) == [(1, 1)]
assert find_pairs(a, 5) == [(1, 4), (1, 4), (0, 5)]
assert not find_pairs(a, 22)

assert  find_pairs2(a, 10) == [(0, 10), (1, 9), (1, 9), (3, 7)]
assert find_pairs2(a, 2) == [(1, 1)]
assert find_pairs2(a, 5) == [(0, 5), (1, 4), (1, 4)]
assert not find_pairs2(a, 22)
