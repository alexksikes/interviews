# Extra Interview Questions
import re
from collections import defaultdict


# Implement a function to determine whether a list of points
# (given as tuples) form a square
def is_square(list_of_points):
    def dist(pt1, pt2):
        return (pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2

    distances = {}
    for pt1 in list_of_points:
        for pt2 in list_of_points:
            if pt1 == pt2:
                continue
            dst = dist(pt1, pt2)
            if dst in distances:
                distances[dst] += 1
            else:
                distances[dst] = 1
    
    found_edges, found_diag = False, False
    for counts in distances.values():
        if counts == 2 * 2:    # double counted diagonals
            found_diag = True
        if counts == 4 * 2:    # double counted edges
            found_edges = True
    return found_edges and found_diag

pt1, pt2, pt3, pt4 = (0,0), (0,1), (1,1), (1,0)
assert is_square([pt1, pt2, pt3, pt4])


# Find the most frequent `num_words` words in the reviews.
#
# We want to summarize a business's reviews. First let's find words that
# occur in many reviews.
#
# We only want to show users the a few words, so let's only return the
# first `num_words` words.
#
#
# For example, we might find that:
# * "pizza" occurs in 200 reviews
# * "olives" occurs in 50 reviews
# ...
# * "tofu" occurs in 1 review
#
# If we want only the first (num_words=1) review then we would return "pizza".
def find_n_most_frequent_words(reviews, num_words):
    d = {}
    for review in reviews:
        seen = set()
        for word in review.split():
            if word not in d:
                d[word] = 1
                seen.add(word)
            elif word in d and word not in seen:
                d[word] += 1

    return (x[0] for x in sorted(d.items(), key = lambda(x): -1*x[1])[:num_words])

reviews = [
    "horrible horrible horrible horrible horrible",
    "I liked the food.",
    "The food was amazing food.",
]

num_words = 3
for word in find_n_most_frequent_words(reviews, num_words):
    assert word in ["food.", "liked", "I"]


# Implement a function to check whether you have a valid sudoku board
# Assume the board is given as a list of list with numbers from 1 - 9
def valid_sudoku(board):
    # check all numbers in every row are unique
    for row in board:
        seen = set()
        for value in row:
            if value in seen:
                return False
            seen.add(value)
    # check all numbers in every column are unique
    for col in range(len(board)):
        seen = set()
        for row in board:
            if row[col] in seen:
                return False
            seen.add(row[col])
    return True

board = [
[5,1,3,6,8,7,2,4,9],
[8,4,9,5,2,1,6,3,7],
[2,6,7,3,4,9,5,8,1],
[1,5,8,4,6,3,9,7,2],
[9,7,4,2,1,8,3,6,5],
[3,2,6,7,9,5,4,1,8],
[7,8,2,9,3,4,1,5,6],
[6,3,5,1,7,2,8,9,4],
[4,9,1,8,5,6,7,2,3]]
assert valid_sudoku(board)

board = [
[5,1,3,6,8,7,2,4,5],
[8,4,9,5,2,1,6,3,7],
[2,6,7,3,4,9,5,8,1],
[1,5,8,4,7,3,9,7,2],
[9,7,4,2,1,8,3,6,5],
[3,2,6,7,9,5,4,1,8],
[7,8,2,9,3,4,1,5,6],
[6,3,5,1,7,2,8,9,4],
[4,9,1,8,5,6,7,2,1]]
assert not valid_sudoku(board)


# Implement a paint fill function.
# Assume the image is a matrix of 0s and 2s where 0s are white squares
# to be painted and 2s are black squares to be omitted.
def paint(image, start):
    row, col = start
    # check the edges
    if not (0 <= row < len(image)):
        return
    if not (0 <= col < len(image[row])):
        return
    # already visited or black square
    if image[row][col] == 1 or image[row][col] == 2:
        return
    # paint the square
    if image[row][col] == 0:
        image[row][col] = 1
    # paint left
    paint(image, (row, col-1))
    # paint bottom
    paint(image, (row+1, col))
    # paint right
    paint(image, (row, col+1))
    # paint top
    paint(image, (row-1, col))

    return image


def test_image():
    return [
        [0,2,0,0,0,0,0,0,0],
        [0,0,0,0,0,2,0,0,0],
        [0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0],
        [0,0,0,0,2,2,2,0,2],
        [0,0,0,0,2,0,0,2,0],
        [0,0,0,0,2,2,2,0,0],
        [0,0,0,2,0,0,0,0,0],
        [0,0,2,0,0,0,0,0,0]]

assert paint(test_image(), [0,0]) == [
[1,2,1,1,1,1,1,1,1],
[1,1,1,1,1,2,1,1,1],
[1,1,1,1,1,1,1,1,2],
[2,1,1,1,1,1,1,1,1],
[1,1,1,1,2,2,2,1,2],
[1,1,1,1,2,0,0,2,0],
[1,1,1,1,2,2,2,0,0],
[1,1,1,2,0,0,0,0,0],
[1,1,2,0,0,0,0,0,0]]

assert paint(test_image(), [5,5]) == [
[0,2,0,0,0,0,0,0,0],
[0,0,0,0,0,2,0,0,0],
[0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0],
[0,0,0,0,2,2,2,0,2],
[0,0,0,0,2,1,1,2,0],
[0,0,0,0,2,2,2,0,0],
[0,0,0,2,0,0,0,0,0],
[0,0,2,0,0,0,0,0,0]]

assert paint(test_image(), [8,8]) == [
[0,2,0,0,0,0,0,0,0],
[0,0,0,0,0,2,0,0,0],
[0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0],
[0,0,0,0,2,2,2,0,2],
[0,0,0,0,2,0,0,2,1],
[0,0,0,0,2,2,2,1,1],
[0,0,0,2,1,1,1,1,1],
[0,0,2,1,1,1,1,1,1]]


# Given an array that contains from 0 to n integers expect one, write a
# method to return this missing integer.
def find_missing_integer(a):
    sum = 0
    for e in a:
        sum += e
    n = len(a)  # it is len(a) because one is missing of the actual array
    return n * (n + 1) / 2 - sum  # sum(k, 1, n) = n * (n + 1) / 2

a = range(15)
a.remove(10)
assert find_missing_integer(a) == 10


# Implement a simple eval function.
#
# Assume:
#   * operators are +, *
#   * operands are integers
#   * expression is well-parenthesized
#
# Example: ((3 + 7) * (6 + 4)) = 100
def eval(s):
    def is_operand(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def find_operator(s):
        cnt = 0
        for i, c in enumerate(s):
            if c == '(':
                cnt += 1
            if c == ')':
                cnt -= 1
            if is_operator(c) and cnt == 0:
                return i

    def is_operator(c):
        return c == '+' or c == '*'

    def compute(operator, a, b):
        if operator == '+':
            return a + b
        if operator == '*':
            return a * b

    def _eval(s):
        s = re.sub("^\(|\)$", "", s)
        if is_operand(s):
            return int(s)
        else:
            i = find_operator(s)
            return compute(s[i], _eval(s[:i]), _eval(s[i+1:]))

    return _eval(s.replace(" ", ""))

assert eval("(2 + 3)") == 5
assert eval("((2 + 3) * 2)") == 10
assert eval("((3 + 7) * (6 + 4))") == 100


# Implement a method to count how many events fall into
# each specific range.
#
# Input:
#
# events : [e0, e1, e2, ...]
# ranges : [(s0, r0), (s1, r1), (s2, r2), ...]
#
# Ouput:
#
# {e0: 2, e1: 0, e3: 1}
def count_events(events, ranges):
    starts = sorted(r[0] for r in ranges)
    events = sorted(((e, i) for i, e in enumerate(events)), key=lambda x: x[0])
    ends = sorted(r[0] + r[1] for r in ranges)

    # counting as we are indirectly merging
    counts, sum = defaultdict(int), 0
    while events:
        event_time, event_index = events[0]
        start = starts[0] if starts else None
        end = ends[0] if ends else None

        # counting #starts before the event
        if start <= event_time and start is not None:
            sum += 1
            starts.pop(0)
        # counting #events before end
        elif event_time <= end or end is None:
            counts[event_index] = sum
            events.pop(0)
        # passed the end time?
        else:
            sum -= 1
            ends.pop(0)
    return counts

events = (0, 2, 5, 7)
ranges = ((2, 5), (0, 6), (5, 8))
assert sorted(count_events(events, ranges).items()) == [(0, 1), (1, 2), (2, 3), (3, 2)]