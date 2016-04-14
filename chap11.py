# Chap 11 - Sorting and Searching
from collections import defaultdict
import random
import copy
import sys
import math


# 11.0.1
# Implement Bubble Sort, Selection Sort, Merge Sort and Quick Sort
def bubble_sort(l):
    swap = True
    while swap:
        swap = False
        for i, (a, b) in enumerate(zip(l, l[1:])):
            if b < a:
                l[i], l[i+1] = l[i+1], l[i]
                swap = True
    return l

l1 = [1, 2, 3, 4, 5, 5, 6, 7, 7, 8, 9, 10]
l2 = copy.copy(l1)
random.shuffle(l2)
assert bubble_sort(l2) == l1


def selection_sort(l):
    def find_smallest(l, start):
        best_a, index = sys.maxint, -1
        for i, a in enumerate(l[start:]):
            if a < best_a:
                best_a, index = a, i
        return start + index

    for i in range(len(l)):
        index = find_smallest(l, i)
        if index == -1:
            break
        l[i], l[index] = l[index], l[i]
    return l

random.shuffle(l2)
assert selection_sort(l2) == l1


def merge_sort(l):
    def merge(left, right):
        result, i, j = [], 0, 0
        while i < len(left) and j < len(right):
            a, b = left[i], right[j]
            if a <= b:
                result.append(a)
                i += 1
            else:
                result.append(b)
                j += 1
        if i < len(left):
            result += left[i:]
        if j < len(right):
            result += right[j:]
        return result

    mid = len(l) / 2
    if mid == 0:
        return l
    array_left = merge_sort(l[0:mid])
    array_right = merge_sort(l[mid:])
    return merge(array_left, array_right)

random.shuffle(l2)
assert merge_sort(l2) == l1


def quick_sort(l):
    def partition(l, start, end, pivot):
        i, j = start, end
        while i <= j:
            while l[i] < pivot:
                i += 1
            while l[j] > pivot:
                j -= 1
            if i <= j:
                l[i], l[j] = l[j], l[i]
                i += 1
                j -= 1
        return i

    def _quick_sort(l, start, end):
        pivot = l[(start + end) / 2]
        index = partition(l, start, end, pivot)
        if start < index - 1:
            _quick_sort(l, start, index-1)
        if index < end:
            _quick_sort(l, index, end)

    _quick_sort(l, 0, len(l)-1)
    return l

random.shuffle(l2)
assert quick_sort(l2) == l1


# 11.0.2
# Implement Radix Sort
# Assume l is a list of positive integers
def radix_sort(l):
    # gives the digit of a number at given position
    def get_digit(number, i):
        if i >= int(math.log10(number or 1)) + 1:
            return -1
        return (number % 10**(i+1)) / 10**i

    # pre-fill the array for the first digit
    levels = [[[] for i in range(10)]]
    for number in l:
        levels[0][get_digit(number, 0)].append(number)

    # fill-up the next level according to previous level
    for i, level in enumerate(levels):
        for digit, numbers in enumerate(level):
            # we have to copy the elements in order to change the iteration
            for number in copy.copy(numbers):
                # get the next digit if it exists
                next_digit = get_digit(number, i + 1)
                if next_digit == -1:
                    continue
                # create the next level if it does not exist
                if i + 1 >= len(levels):
                    levels.append([[] for j in range(10)])
                # add this number for the next digit
                levels[i+1][next_digit].append(number)
                # remove that number from the previous level
                # not the best of way of doing this
                # instead we should be popping the elements
                level[digit].remove(number)

    # loop from smaller to larger levels and return the results
    result = []
    for level in levels:
        for numbers in level:
            result += numbers
    return result

l = [0, 34, 2, 7, 143, 34, 5, 1000, 32, 44, 11]
assert radix_sort(l) == sorted(l)


# 11.0.3
# Sort people by increasing order of age (bucket sort)
def bucket_sort(l):
    counts = [0] * 100
    for a in l:
        counts[a] += 1
    result = []
    for i, count in enumerate(counts):
        if count:
            result += [i] * count
    return result

a = [23, 45, 12, 7, 67, 32, 88, 23, 11, 7]
assert bucket_sort(a) == sorted(a)


# 11.0.4
# Implement Binary Search
def binary_search(l, a):
    def _binary_search(start, end):
        if start > end:
            return -1
        mid = (start + end) / 2
        if a < l[mid]:
            return _binary_search(start, mid-1)
        elif a > l[mid]:
            return _binary_search(mid+1, end)
        else:
            return mid
    return _binary_search(0, len(l)-1)


l1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
assert binary_search(l1, 3) == 2
assert binary_search(l1, 11) == -1


# 11.1
# Merge array B into array A, assuming A has
# enough space at the end to accommodate for B
def merge_in_place(A, B):
    i, j = len(A) - 1, len(B) - 1
    A = A + len(B) * [None]  # simulate buffer at the end of the array
    k = len(A) - 1
    while i >= 0 and j >= 0:
        if A[i] > B[j]:
            A[k] = A[i]
            i -= 1
        else:
            A[k] = B[j]
            j -= 1
        k -= 1
    if j >= 0:
        A = B[:j+1] + A[j:]
    return A

A = [1, 2, 3, 4, 5, 6, 10, 11, 12]
B = [0, 1, 1, 2, 5, 7, 9]
assert merge_in_place(A, B) == [0, 1, 1, 1, 1, 2, 2, 3, 4, 5, 5, 6, 7, 9, 10, 11, 12]


# 11.2
# Write a method to sort an array of strings so that the
# anagrams are next to each other
def sort_anagrams(l):
    return sorted(l, key=lambda x: sorted(x, reverse=True))

l = ["alex", "is", "cool", "xela", "si", "zebra"]
assert sort_anagrams(l) == ['cool', 'is', 'si', 'alex', 'xela', 'zebra']


# 11.3
# Given a sorted of integers that has been rotated,
# write code to find an element in the array
def binary_search_rotated(l, x):
    def _binary_search_rotated(l, start, end):
        if start > end:
            return -1
        mid = (start + end) / 2
        if x == l[mid]:
            return mid
        # normally sorted left side
        if l[start] <= l[mid]:
            if l[start] < x < l[mid]:
                return _binary_search_rotated(l, start, mid - 1)
            else:
                return _binary_search_rotated(l, mid + 1, end)
        # normally sorted right
        else:
            if l[mid] < x < l[end]:
                return _binary_search_rotated(l, mid + 1, end)
            else:
                return _binary_search_rotated(l, start, mid - 1)
    return _binary_search_rotated(l, 0, len(l)-1)

l = [9, 10, 11, 1, 2, 3, 4, 5, 6, 7, 8]
assert binary_search_rotated(l, 5) == 7
l = [6, 7, 8, 9, 1, 2, 3, 4, 5]
assert binary_search_rotated(l, 7) == 1
l = [8, 8, 8, 8, 2, 3, 4, 5, 6, 7, 8, 8]
assert binary_search_rotated(l, 2) == 4


# 11.4
# How would you sort the strings (one per line) in large file (external sort)
def external_sort(fi, max_buffer_size):
    def handle_buffer(buffer, i):
        buffer.sort()
        with open("data/ext_%s.txt" % i, mode="w") as f:
            for s in buffer:
                f.write("%s" % s)

    def find_smallest(strings):
        best_i, best_s = -1, None
        for i, s in enumerate(strings):
            if s != '' and s is not None:
                if s < best_s or best_s is None:
                    best_i, best_s = i, s
        return best_i

    def merge_files(num_files):
        results = open("data/ext_results.txt", mode="w")
        files = [open("data/ext_%s.txt" % i) for i in range(num_files)]
        i, strings = 0, [fi.readline() for fi in files]
        while True:
            i = find_smallest(strings)
            if i == -1:
                break
            results.write(strings.pop(i))
            strings.insert(i, files[i].readline())
        for fi in files:
            fi.close()
        results.close()

    buffer, num_files = [], 0
    with open(fi) as f:
        for line in f:
            buffer.append(line)
            if len(buffer) == max_buffer_size:
                handle_buffer(buffer, num_files)
                num_files += 1
                buffer = []
    if buffer:
        handle_buffer(buffer, num_files)
        num_files += 1
    merge_files(num_files)


def test_external_sort():
    dict = open("/usr/share/dict/words").readlines()
    random.shuffle(dict)
    open("data/words.txt", mode="w").writelines(dict)
    external_sort("data/words.txt", 50000)
    assert open("data/ext_results.txt").readlines() == sorted(open("/usr/share/dict/words").readlines())

test_external_sort()


# 11.5
# Given a sorted array with empty strings,
# find the location of a given string.
def binary_search_null(l, x):
    def find_closest_string(mid, start, end):
        i, j = mid, mid
        while i >= start or j <= end:
             if l[i]:
                 return i
             if l[j]:
                 return j
             i -= 1
             j += 1
        return -1

    def _binary_search(start, end):
        if start > end:
            return -1
        mid = (start + end) / 2
        if not l[mid]:
            mid = find_closest_string(mid, start, end)
        if mid == -1:
            return -1
        if x < l[mid]:
            return _binary_search(start, mid - 1)
        elif x > l[mid]:
            return _binary_search(mid + 1, end)
        else:
            return mid
    return _binary_search(0, len(l)-1)

l = ["alex", "", "", "", "", "", "bob", "", "roger", "zoe", ""]
assert binary_search_null(l, "alex") == 0
assert binary_search_null(l, "bob") == 6
assert binary_search_null(l, "roger") == 8
assert binary_search_null(l, "zoe") == 9
assert binary_search_null(l, "nathalie") == -1


# 11.6
# Given an M x N matrix in which each row and column are sorted in
# ascending order, write a method to find an element.
def find_in_sorted_matrix(M, x):
    m, n = len(M), len(M[0])
    i, j = 0, n-1
    while i < m and j >=0:
        if M[i][j] == x:
            return i, j
        elif x < M[i][j]:
            j -= 1
        else:
            i += 1

M = [[10, 20, 30, 40, 50],
     [20, 25, 35, 45, 55],
     [45, 55, 65, 70, 75],
     [65, 70, 75, 80, 85],
     [75, 80, 85, 90, 95]]

assert find_in_sorted_matrix(M, 10) == (0, 0)
assert find_in_sorted_matrix(M, 55) == (1, 4)
assert find_in_sorted_matrix(M, 65) == (2, 2)
assert find_in_sorted_matrix(M, 95) == (4, 4)
assert not find_in_sorted_matrix(M, 100)


# 11.8
# In a stream of numbers, implement a way of obtaining the
# rank of a number x which is the number of values less than
# or equal to x (not including itself)
class RankTree(object):
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.left_size = 0

    def insert(self, data):
        if data <= self.data:
            if not self.left:
                self.left = RankTree(data)
            else:
                self.left.insert(data)
            self.left_size += 1
        else:
            if not self.right:
                self.right = RankTree(data)
            else:
                self.right.insert(data)

    def get_rank(self, data):
        if data == self.data:
            return self.left_size
        if data < self.data:
            if not self.left:
                return -1
            return self.left.get_rank(data)
        else:
            right_rank = self.right.get_rank(data) if self.right else -1
            if right_rank == -1:
                return -1
            return self.left_size + 1 + right_rank

tree = RankTree(1)
for i in (5, 2, 7, 1, 5, 5, 2, 7, 11, 1, 3):
    tree.insert(i)

assert tree.get_rank(7) == 10
assert tree.get_rank(1) == 2
assert tree.get_rank(33) == -1

for i in (2, 33, 5, 1):
    tree.insert(i)

assert tree.get_rank(33) == 15
assert tree.get_rank(3) == 7
assert tree.get_rank(22) == -1
