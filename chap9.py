# Chap 9 - Recursion and Dynamic Programming
import copy


# 9.0.1
# Return the nth Fibonacci number in O(n)
def fibonacci(n):
    def _fibonacci(n):
        if n == 0 or n == 1:
            return n
        if n not in fib:
            fib[n] = _fibonacci(n-1) + _fibonacci(n-2)
        return fib[n]
    fib = {}
    return _fibonacci(n)

assert fibonacci(50) == 12586269025


# 9.1
# A child can go up the stairs by one, two, or three steps.
# In how many ways can he go up the stairs.
def stairs(n):
    def _stairs(n):
        if n == 0 or n == 1 or n == 2:
            return n
        if n == 3:
            return 4
        if n not in d:
            d[n] = _stairs(n-1) + _stairs(n-2) + _stairs(n-3)
        return d[n]
    d = {}
    return _stairs(n)

assert stairs(50) == 10562230626642


# 9.2
# A robot is sitting on the upper left corner of an X and Y grid.
# The robot can move right and down only. How many possible paths
# are there to go from the upper left corner to the bottom right
# corner?
#

# The robot needs to make a path that looks like this: DDDRRDRRD with
# X downs (D) and Y rights (R). Numbering each of the Ds and Ys, we
# need to pick exactly X Ds from a set of size X+Y. That is given
# X+Y choose X or C(X+Y,X).

# Follow up: if there are spots on which the robot can't go, design
# an algorithm to find a path from the upper left corner to the
# bottom right corner.
def find_path_robot(grid):
    def _find_path(x, y, path):
        path.append((x, y))
        # we found the end
        if x == X and y == Y:
            return path
        # mark as visited
        grid[x][y] = 1
        # move robot right or down
        success = False
        if y+1 <= Y and grid[x][y+1] == 0:
            success = _find_path(x, y+1, path)
            if not success:
                path.remove((x, y+1))
        if not success and x+1 <= X and grid[x+1][y] == 0:
            success = _find_path(x+1, y, path)
            if not success:
                path.remove((x+1, y))
        return success
    X, Y = len(grid)-1, len(grid[0])-1
    return _find_path(0, 0, [])

grid = [
    [0,2,0,0,0,0,0,0,0],
    [0,0,0,0,0,2,0,0,0],
    [0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0],
    [0,0,0,0,2,2,2,0,2],
    [0,0,0,0,2,0,0,2,0],
    [0,0,0,0,0,2,2,0,0],
    [0,0,0,2,0,0,0,0,0],
    [0,0,2,0,0,0,0,0,0]]
assert find_path_robot(grid) == [
    (0, 0), (1, 0), (1, 1), (1, 2), (1, 3), (2, 3),
    (3, 3), (4, 3), (5, 3), (6, 3), (6, 4), (7, 4),
    (7, 5), (7, 6), (7, 7), (7, 8), (8, 8)]
grid = [
    [0,2,0,0,0,0,0,0,0],
    [0,0,0,0,0,2,0,0,0],
    [0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0],
    [0,0,0,0,2,2,2,0,2],
    [0,0,0,0,2,0,0,2,0],
    [0,0,0,0,2,2,2,0,0],
    [0,0,0,2,0,0,0,0,0],
    [0,0,2,0,0,0,0,0,0]]
assert not find_path_robot(grid)


# 9.3
# The magic index i of an array A is defined as A[i] == i
# Given a sorted array of distinct integers, find a magic
# index if it exists.
def find_magic_index(A):
    def _find_magic_index(start, end):
        if start > end:
            return -1
        mid = (start + end) / 2
        if mid == A[mid]:
            return mid
        if mid < A[mid]:
            return _find_magic_index(start, mid - 1)
        else:
            return _find_magic_index(mid + 1, end)
    return _find_magic_index(0, len(A)-1)

assert find_magic_index([0, 1, 3, 5, 6, 7, 8, 9]) == 1
assert find_magic_index([1, 2, 3, 5, 6, 7, 8, 9]) == -1


# Follow up: what if the elements are not distinct ?
def find_magic_index_not_distinct(A):
    def _find_magic_index(start, end):
        if start > end:
            return -1
        mid = (start + end) / 2
        if mid == A[mid]:
            return mid
        left = _find_magic_index(start, min(mid - 1, A[mid]))
        if left >= 0:
            return left
        right = _find_magic_index(max(mid + 1, A[mid]), end)
        if right >= 0:
            return right
        return -1
    return _find_magic_index(0, len(A)-1)

assert find_magic_index_not_distinct([1, 1, 2, 3, 4, 4, 5, 6, 6, 9, 9, 10]) == 2
assert find_magic_index_not_distinct([1, 2, 3, 5, 6, 7, 8, 9]) == -1


# 9.4
# Write a method to return all subsets of a set
def power_set(s):
    def P(n):
        if n == 0:
            return [[]]
        _P = P(n-1)
        for subset in copy.copy(_P):
            _P.append(subset + [s[n-1]])
        return _P
    return P(len(s))

assert power_set((1, 2, 3)) == [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]


# we can also observe that there are as many subsets as there
# integers from 0 to 2**n. Therefore, to a subset of the power
# set corresponds a given number in binary.
def power_set2(s):
    def to_set(number):
        subset = []
        for i, e in enumerate(s):
            if number & (1 << i) != 0:
                subset.append(s[i])
        return subset

    def P(n):
        _P = []
        for number in range(2**n):
            _P.append(to_set(number))
        return _P
    return P(len(s))

assert power_set2((1, 2, 3)) == [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]


# 9.5
# Write a method to compute all permutations of a string
def permutations(s):
    if s == "":
        return [""]

    r = []
    for str in permutations(s[:-1]):
        r.append(str + s[-1])
        i = len(str) - 1
        while i >= 0:
            r.append(str[:i] + s[-1] + str[i:])
            i -= 1
    return r

assert permutations("123") == ['123', '132', '312', '213', '231', '321']


# 9.6
# Design a method to print all valid combinations of n-pairs of
# parenthesis.
def parenthesis(n):
    def _insert(paren):
        return (paren[0:i] + "()" + paren[i:] for i in range(len(paren)))

    r = []
    if n <= 1:
        return ["()"]
    for paren in parenthesis(n-1):
        for p in _insert(paren):
            if p not in r:
                r.append(p)
    return r

assert parenthesis(2) == ['()()', '(())']
assert parenthesis(3) == ['()()()', '(())()', '()(())', '(()())', '((()))']


# 9.7
# Implement a paint fill function which given a screen, a point,
# and a new color, fill the surround area until the color changes
# from the original.
def paint_fill(image, point, new_color):
    def _paint_fill(x, y):
        if 0 <= x <= X and 0 <= y <= Y and image[x][y] == old_color:
            image[x][y] = new_color
            _paint_fill(x+1, y)
            _paint_fill(x, y+1)
            _paint_fill(x-1, y)
            _paint_fill(x, y-1)
    x, y = point[0], point[1]
    old_color = image[x][y]
    X, Y = len(image)-1, len(image[0])-1
    _paint_fill(x, y)
    return image


def test_image():
    return [
        [0,2,0,0,0,0,0,0,0],
        [0,0,0,0,0,2,0,0,0],
        [0,0,1,0,0,0,1,0,2],
        [2,0,0,0,0,0,0,0,0],
        [0,0,0,0,2,2,2,0,2],
        [0,0,1,0,2,2,2,2,0],
        [0,0,0,0,2,2,2,0,0],
        [0,0,0,2,0,0,0,0,0],
        [0,0,2,0,0,0,1,0,0]]

assert paint_fill(test_image(), (5, 4), 3) == [
[0,2,0,0,0,0,0,0,0],
[0,0,0,0,0,2,0,0,0],
[0,0,1,0,0,0,1,0,2],
[2,0,0,0,0,0,0,0,0],
[0,0,0,0,3,3,3,0,2],
[0,0,1,0,3,3,3,3,0],
[0,0,0,0,3,3,3,0,0],
[0,0,0,2,0,0,0,0,0],
[0,0,2,0,0,0,1,0,0]]

assert paint_fill(test_image(), (0, 0), 3) == [
[3,2,3,3,3,3,3,3,3],
[3,3,3,3,3,2,3,3,3],
[3,3,1,3,3,3,1,3,2],
[2,3,3,3,3,3,3,3,3],
[3,3,3,3,2,2,2,3,2],
[3,3,1,3,2,2,2,2,0],
[3,3,3,3,2,2,2,0,0],
[3,3,3,2,0,0,0,0,0],
[3,3,2,0,0,0,1,0,0]]


# 9.9
# Arrange 8 queens on a 8x8 chess board so that none of them share
# the same row, column or diagonal. Return all possible solutions.
def eight_queens():
    def valid(row, col, board):
        # we should only check for the top row-1 and top diagonals
        for i in range(row):
            if board.get(i) == col:
                return False
            if (board.get(row-i-1) == col-i-1 or
                board.get(row-i-1) == col+i+1):
                return False
        return True

    def place_queens(row, board, results):
        if row == 8:
            results.append(copy.copy(board))
        for col in range(8):
            if valid(row, col, board):
                board[row] = col
                place_queens(row+1, board, results)
        return results

    return place_queens(0, {}, [])


def dict_to_matrix(d, size):
    m = []
    for row in sorted(d.keys()):
        m.append([0] * size)
        m[-1][d[row]] = 1
    return m


def unique(l):
    new = []
    for e in l:
        if e not in new:
            new.append(e)
    return new

assert len(eight_queens()) == len(unique(eight_queens())) == 92
