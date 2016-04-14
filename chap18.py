# Chap 18 - Hard
import random
import heapq
from collections import defaultdict
from chap3 import Queue
random.seed(0)


# 18.2
# Write a method to shuffle a deck of cards.
def shuffle(cards):
    def _shuffle(pos):
        if pos == 0:
            return
        i = random.randint(0, pos)
        cards[pos], cards[i] = cards[i], cards[pos]
        _shuffle(pos-1)
    _shuffle(len(cards)-1)
    return cards

assert shuffle(range(1, 14)) == [1, 7, 8, 9, 12, 2, 6, 4, 13, 3, 5, 10, 11]
assert shuffle(range(1, 14)) == [1, 5, 13, 12, 2, 11, 6, 8, 9, 3, 7, 10, 4]


# 18.3
# Write a method to randomly generate a set of m integers from
# an array of size n where m <= n.
def choice(a, m):
    # we do it iteratively for a change
    n, pos, r = len(a), len(a)-1, []
    while pos >= 0 and pos >= n - m:
        i = random.randint(0, pos)
        r.append(a[i])
        a[pos], a[i] = a[i], a[pos]
        pos -= 1
    return r

assert choice(range(100), 10) == [47, 9, 42, 59, 87, 91, 44, 80, 23, 73]
assert choice(range(100), 10) == [54, 1, 70, 38, 79, 63, 0, 45, 95, 22]
assert not choice(range(100), 0)
assert not choice(range(100), -5)
assert len(choice(range(100), 10000)) == 100


# 18.5
# Given any two words in a large text file, find the shortest distance
# (in terms of number of words) between these two words.
# Assume the two words are different and the order does not matter.
def shortest_distance(file, w1, w2):
    def update_min_dist(p1, p2, prev_min):
        if p1 >= 0 and p2 >= 0:
            dist = abs(p1 - p2)
            return dist if dist < prev_min or prev_min == -1 else prev_min
        else:
            return prev_min

    pos, p1, p2, min_dist = -1, -1, -1, -1
    with open(file) as f:
        for l in f:
            for w in l.split():
                pos += 1
                if w == w1:
                    p1 = pos
                elif w == w2:
                    p2 = pos
                else:
                    continue
                min_dist = update_min_dist(p1, p2, min_dist)
    return min_dist

assert shortest_distance("data/sample_text.txt", "the", "and") == 1
assert shortest_distance("data/sample_text.txt", "utilities", "master") == 4
assert shortest_distance("data/sample_text.txt", "alex", "master") == -1


# If we need to repeat the operation, then we build an inverted index (word, pos)
# and find the pair with minimum distance.
def build_dict(file):
    d, pos = defaultdict(list), 0
    with open(file) as f:
        for l in f:
            for w in l.split():
                d[w].append(pos)
                pos += 1
    return d


def shortest_distance2(dict, w1, w2):
    def merge(a1, a2):
        r, i, j = [], 0, 0
        while i < len(a1) and j < len(a2):
            p1, p2 = a1[i], a2[j]
            if p1 <= p2:
                r.append((p1, 'w1'))
                i += 1
            else:
                r.append((p2, 'w2'))
                j += 1
        if i >= len(a1):
            r += [(p2, 'w2') for p2 in a2[j:]]
        else:
            r += [(p1, 'w1') for p1 in a2[i:]]
        return r

    l, min_dist = merge(dict[w1], dict[w2]), -1
    for (p1, w1), (p2, w2) in zip(l, l[1:]):
        if w1 != w2:
            dist = abs(p1 - p2)
            if dist < min_dist or min_dist == -1:
                min_dist = dist
    return min_dist

dict_ = build_dict("data/sample_text.txt")
assert shortest_distance2(dict_, "the", "and") == 1
assert shortest_distance2(dict_, "utilities", "master") == 4
assert shortest_distance2(dict_, "alex", "master") == -1


# 18.6
# Find the nth smallest number in a very large array.
def nsmallest(n, a):
    h = []
    for e in a[:n]:
        heapq.heappush(h, -e)  # we use a max heap but push -1 * e
    for e in a[n:]:
        heapq.heappushpop(h, -e)
    return -heapq.heappop(h)

a = range(100)
random.shuffle(a)
assert nsmallest(30, a) == 29
assert nsmallest(67, a) == 66

b = [random.randint(0, 100) for i in range(100)]
assert nsmallest(30, b) == 30
assert nsmallest(67, b) == 64


# Implementation of selection rank (may not be O(space) feasible if
# the array is very large)
def nsmallest2(n, a):
    def split_left_right(pivot, a):
        left, right = [], []
        for e in a:
            if e <= pivot:
                left.append(e)
            else:
                right.append(e)
        return left, right

    def selection_rank(rank, a):
        left, right = split_left_right((a[0] + a[-1]) / 2, a)
        if len(left) == rank:
            return max(left)
        elif len(left) > rank:
            return selection_rank(rank, left)
        else:
            return selection_rank(rank - len(left), right)

    return selection_rank(n, a)

assert nsmallest2(30, a) == 29
assert nsmallest2(67, a) == 66
assert nsmallest2(30, b) == 30
assert nsmallest2(67, b) == 64


# Implementation of selection rank but in place (this modifies the
# actual array)
def nsmallest3(n, a):
    def partition(start, end, pivot):
        i, j = start, end
        while i <= j:
            while a[i] < pivot:
                i += 1
            while a[j] > pivot:
                j -= 1
            if i <= j:
                a[i], a[j] = a[j], a[i]
                i += 1
                j -= 1
        return i

    def selection_rank(rank, start, end):
        pivot = a[(start + end) / 2]
        index = partition(start, end, pivot)
        left_size = index - start
        if left_size == rank:
            return max(a[start:index])
        elif left_size > rank:
            return selection_rank(rank, start, index-1)
        else:
            return selection_rank(rank - left_size, index, end)

    return selection_rank(n, 0, len(a)-1)

a = range(100)
random.shuffle(a)
assert nsmallest3(30, a) == 29

a = range(100)
random.shuffle(a)
assert nsmallest3(67, a) == 66

assert nsmallest3(30, b) == 30


# 18.7
# Given a list of word, find the longest word made of other words.
def longest_word(words):
    def is_made_up(w, allow_itself=False, cache = {}):
        if w in cache or (allow_itself and w in dict_words):
            return True

        success, i = False, 1
        while i < len(w):
            if w[0:i] in dict_words:
                success = True and is_made_up(w[i:], True, cache)
            i += 1
        cache[w] = success  # we cache the results
        return success

    dict_words = set(words)
    for w in sorted(words, key=lambda x: -len(x)):  # from largest to smallest words
        if is_made_up(w):
            return w

assert longest_word(['a', 'b', 'c', 'ab', 'abc', 'xxabbcabc', 'bc', 'xx', 'aaavvabvvvvvv']) == 'xxabbcabc'
assert longest_word(open("/usr/share/dict/words").read().splitlines()) == 'formaldehydesulphoxylate'


# 18.9
# In a stream of numbers, have a method to maintain the median value.
class MedianTree(object):
    def __init__(self):
        self.left, self.right = [], []

    def add(self, num):
        median = self.get_median()
        if median is None or num <= median:
            heapq.heappush(self.left, -num)
        else:
            heapq.heappush(self.right, num)
        self.rebalance()

    def get_median(self):
        if not self.left and not self.right:
            return None
        if len(self.left) > len(self.right):
            return -self.left[0]
        if len(self.left) == len(self.right):
            return (-self.left[0] + self.right[0]) / 2.0

    def rebalance(self):
        diff = len(self.left) - len(self.right)
        if diff > 1:
            heapq.heappush(self.right, -heapq.heappop(self.left))
        if diff <= -1:
            heapq.heappush(self.left, -heapq.heappop(self.right))

m = MedianTree()
for i in range(10):
    m.add(i)
assert m.get_median() == 4.5

for i in [random.randint(0, 10) for i in range(10)]:
    m.add(i)
assert m.get_median() == 3.5


# 18.10
# One letter game: design an algorithm to go from one word to another
# word of the same length by changing one letter at a time.
class OneLetterGame(object):

    LETTERS = "abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    def __init__(self):
        self.dict = set(open("/usr/share/dict/words").read().splitlines())

    def solve(self, w1, w2):
        def make_path(word, paths):
            path = []
            while word is not None:
                path.append(word)
                word = paths.get(word)
            path.reverse()
            return path

        paths = {w1: None}
        q = Queue().enqueue(w1)
        while not q.is_empty():
            word = q.dequeue()
            if word == w2:
                return make_path(w2, paths)
            else:
                for w in self.get_neighbors(word):
                    if w in paths:
                        continue
                    q.enqueue(w)
                    paths[w] = word

    def get_neighbors(self, w):
        for c in OneLetterGame.LETTERS:
            for i in range(len(w)):
                word = w[0:i] + c + w[i+1:]
                if word in self.dict:
                    yield word

game = OneLetterGame()
assert game.solve("cat", "dog") == ['cat', 'cag', 'dag', 'dog']
assert game.solve("sky", "dog") == ['sky', 'soy', 'sog', 'dog']
assert not game.solve("nope", "nnnn")
assert game.solve("lime", "like") == ['lime', 'like']
assert game.solve("damp", "like") == ['damp', 'dame', 'dime', 'dike', 'like']


# 18.11
# Given a square matrix with zeroes and ones, find the largest square
# with all borders set to one.
def largest_square(A):
    def check_row(i, j, size):
        for e in A[i][j:j+size]:
            if not e:
                return False
        return True

    def check_col(i, j, size):
        for row in range(i, size):
            if not A[row][j]:
                return False
        return True

    def is_square(size):
        for i in range(N-size+1):
            for j in range(N-size+1):
                if (check_row(i, j, size) and
                        check_col(i, j, size) and
                        check_row(size-1+i, j, size) and
                        check_col(i, size-1+j, size)):
                    return size, [(i, j), (i, size-1+j), (size-1+i, size-1+j), (size-1+i, j)]

    N, square, n = len(A), None, len(A)
    while square is None and n >= 1:
        square = is_square(n)
        n -= 1
    return square

assert largest_square([
    [0,1,0,0,0,0,0,0,0],
    [0,0,0,0,1,1,1,1,0],
    [0,0,0,0,1,0,0,1,0],
    [1,1,1,1,1,0,0,1,0],
    [1,0,0,0,1,1,1,1,0],
    [1,0,0,0,1,0,0,1,0],
    [1,0,0,0,1,1,1,1,0],
    [1,1,1,1,1,0,0,0,0],
    [0,0,1,0,0,0,0,0,0]]
) == (5, [(3, 0), (3, 4), (7, 4), (7, 0)])

assert largest_square([
    [0,1,0,0,0,0,0,0,0],
    [0,0,0,0,1,1,1,1,0],
    [0,0,1,1,1,1,1,1,1],
    [1,1,1,1,1,0,0,1,1],
    [1,0,1,0,1,1,1,1,1],
    [1,0,1,0,1,0,0,1,1],
    [1,0,1,0,1,1,1,1,1],
    [1,1,1,1,1,0,0,0,1],
    [0,0,1,1,1,1,1,1,1]]
) == (7, [(2, 2), (2, 8), (8, 8), (8, 2)])

assert largest_square([
    [0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,0,0,0,0],
    [0,1,0,0,1,0,0,0,0],
    [0,1,0,0,1,0,0,0,0],
    [0,1,1,1,1,0,0,0,0],
    [0,0,0,0,0,0,1,1,1],
    [0,0,0,0,0,0,1,0,1],
    [0,0,0,0,0,0,1,1,1],
    [0,0,0,0,0,0,0,0,0]]
) == (4, [(1, 1), (1, 4), (4, 4), (4, 1)])

assert not largest_square([
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]]
)

assert largest_square([
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]]
) == (1, [(3, 3), (3, 3), (3, 3), (3, 3)])
