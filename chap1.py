# Chapter 1 - Arrays and Strings
import copy


# 1.1
# Determine if a string has all unique characters.
# What if you cannot use additional data structrures?
def is_unique(string):
    seen = set()    # instead of using a set we could also use bitset for every character
    for c in string:
        if c in seen:
            return False
        else:
            seen.add(c)
    return True


def is_unique2(string):
    for i, c in enumerate(string):
        if c in string[i+1:]:
            return False
    return True

s = "abcdefg"

assert is_unique(s)
assert is_unique2(s)

s = "abccdeefg"

assert not is_unique(s)
assert not is_unique2(s)


# 1.2
# Implement the reverse list function for primitive types. Do it in place without using slicing operations.
def reverse(lst):
    i, j = 0, len(lst)-1
    while i < j:
        lst[i], lst[j] = lst[j], lst[i]
        i += 1
        j -= 1
    return lst

lst = [1, 2, 3, 4, 5, 6, 7]
lst2 = copy.copy(lst)
lst2.reverse()

assert reverse(lst) == lst2
assert reverse(lst) == lst


# 1.3
# Given two strings determine if one is a permutation of the other
# We could compare sorted version of strings but this would be O(nlog(n))
# We could save space by using a bitset where each 26 letter is 0 or 1
def is_permutation(string1, string2):
    def get_counts(string):
        counts = {}
        for c in string:
            if c in counts:
                counts[c] += 1
            else:
                counts[c] = 1
        return counts
    return get_counts(string1) == get_counts(string2)

assert is_permutation("abcdefg", "gfeabcd")
assert not is_permutation("abcdefg", "abc")


# 1.4
# Implement a replace character function. Do not use python replace function.
def replace(string, old, new):
    # In C and if given enough space we would do it from the back of the array in place
    # but this seems convoluted in python
    new_str = ""
    for c in string:
        if c == old:
            new_str += new
        else:
            new_str += c
    return new_str

assert replace("Mr John Smith", " ", "%20") == "Mr%20John%20Smith"


# 1.5
# Implement simple string compression that transforms aabccccaa into a2b1c4a2 for example
def compress(string):
    cstr, i = "", 0
    while i < len(string):
        j = 1
        while i + j < len(string) and string[i] == string[i+j]:
            j += 1
        cstr += string[i] + str(j)
        i += j
    return cstr

assert compress("aabccccaa") == "a2b1c4a2"


# 1.6
# Rotate an image by 90 degrees, you can assume the image is
# an NxN matrix implemented as a list of list.
def rotate(m):
    # note this is similar to a transpose operation
    rot_m = []
    for i in range(len(m)):
        rot_m.append([])
    for i, row in enumerate(m[::-1]):
        for j, val in enumerate(row):
            rot_m[j].append(val)
    return rot_m

m_start = [
    [ 1,  2,  3,  4],
    [ 5,  6,  7,  8],
    [ 9, 10, 11, 12],
    [13, 14, 15, 16]]
m_expected = [
    [13,  9,  5,  1],
    [14, 10,  6,  2],
    [15, 11,  7,  3],
    [16, 12,  8,  4]]

assert rotate(m_start) == m_expected


# 1.7
# Implement a function such that if an element in a MxN matrix is 0
# then its entire row and column are set to 0
def zero_matrix(matrix):
    # record the row and column index
    row_index, col_index = [], []
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if val == 0:
                row_index.append(i)
                col_index.append(j)

    for i in row_index:
        for j in xrange(len(matrix[i])):
            matrix[i][j] = 0
    for j in col_index:
        for i, row in enumerate(matrix):
            for col in xrange(len(matrix)):
                row[j] = 0

    return matrix

m = [[0, 1, 2],
     [3, 4, 5],
     [5, 6, 0]]
assert zero_matrix(m) == [
    [0, 0, 0],
    [0, 4, 0],
    [0, 0, 0]]


# 1.8
# Given two strings s1 and s2, write a function such checks
# whether s2 is a rotation of s1
def is_rotation(s1, s2):
    return s2 in (s1 * 2)

assert is_rotation("alex is cool", "coolalex is")
assert not is_rotation("alex is cool", "coolalex is not")
