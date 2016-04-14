# Chap 7 - Mathematics and Probability
import math


# 7.0.1
# Checking for primality
def is_prime(number):
    for i in range(2, int(math.sqrt(number))):  # we can go till sqrt(number) only
        if number % i == 0:
            return False
    return True

assert is_prime(13)
assert not is_prime(55)


# 7.0.2
# Generate a list of prime numbers
def sieve(max):
    def get_next_prime(numbers):
        return (i for i in numbers if i)

    numbers, primes = [0, 0] + range(2, max), []
    for prime in get_next_prime(numbers):
        primes.append(prime)
        for i in range(prime * prime, max, prime):  # we can start at prime^2
            numbers[i] = 0
    return primes

assert sieve(50) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]


# 7.3
# Given two lines, determine whether the two lines intersect
class Line(object):
    epsilon = 0.00001

    def __init__(self, m=None, b=None, x=None):
        self.m = m
        self.b = b
        self.x = x

    # if there are equal then they intersect otherwise
    # just check that the slope is different
    def intersect(self, other):
        return self == other or not Line._floats_equal(self.m, other.m)

    def __eq__(self, other):
        return Line._floats_equal(self.m, other.m) and \
               Line._floats_equal(self.b, other.b) and \
               Line._floats_equal(self.x, other.x)

    def __hash__(self):
        return hash(self.m) + hash(self.b) + hash(self.x)

    @classmethod
    def new_line(cls, pt1, pt2):
        if pt1 == pt2:
            raise "Can't dertermine a line, the points must be different!"
        x1, y1, x2, y2 = pt1, pt2
        if x1 == x2:
            return Line(x=x1)
        m = 1.0 * (y2 - y1) / (x2 - x1)
        return Line(m, y1 - m * x1)

    @classmethod
    def _floats_equal(cls, a, b):
        if a is None or b is None:
            return a == b
        return abs(a - b) <= Line.epsilon

assert Line(0.33, 5.5).intersect(Line(0.66, 5.5))  # different slopes
assert not Line(0.33, 5.5).intersect(Line(0.33, 8.5))
assert Line(0, 5.5).intersect(Line(0, 5.5))  # no slope but same line
assert not Line(0, 5.5).intersect(Line(0, 8.5))
assert Line(x=4.2).intersect(Line(x=4.2))  # infinite slope but same line
assert not Line(x=4.2).intersect(Line(x=5))


# 7.4
# Implement multiply, subtract, and divide of integers using only
# the add operator
def negate(a):
    sign, b = -1 if a > 0 else 1, 0
    while a != 0:
        a += sign
        b += sign
    return b

assert negate(3) == -3
assert negate(-3) == 3


def subtract(a, b):
    return b + negate(a)

assert subtract(5, 10) == 5
assert subtract(7, 3) == -4


def absolute(a):
    return a if a > 0 else negate(a)


# check that for clarity!
def multiply(a, b):
    if absolute(b) > absolute(a):
        return multiply(b, a)
    sign = 1 if (a > 0 and b > 0) or (a < 0 and b < 0) else -1
    if a > 0 and sign < 0 or a < 0 and sign > 0:
        a = negate(a)
    r, b = 0, absolute(b)
    while b > 0:
        r += a
        b = subtract(1, b)
    return r

assert multiply(5, 5) == 25
assert multiply(-3, 10) == -30
assert multiply(-3, -3) == 9


def divide(a, b):
    if b == 0:
        raise "Divide by zero!"
    sign = 1 if (a > 0 and b > 0) or (a < 0 and b < 0) else -1
    a, b = absolute(a), absolute(b)
    if b > a:
        return sign
    r = 1
    while b < a:
        r += 1
        b += b
    return r if sign > 0 else negate(r)

assert divide(10, 3) == 3
assert divide(5, -5) == -1


# 7.5
# Given two squares find a line that cut them in two.
# Assume the squares run parallel to the x axis.
class Square(object):
    def __init__(self, top_left, top_right, bot_left, bot_right):
        self.top_left = top_left
        self.top_right = top_right
        self.bot_left = bot_left
        self.bot_right = bot_right

    def get_middle_point(self):
        return (self.top_left + self.bot_left)/2, (self.top_right + self.bot_right)/2


def cut_squares(s1, s2):
    return Line.new_line(s1.get_middle_point(), s2.get_middle_point())


# 7.6
# Find a line which passes the most number of points.
def best_line(points):
    cnt_lines, best_line = {}, None
    for i, pt1 in enumerate(points):
        if i + 1 > len(points):
            break
        for pt2 in points[i+1:]:
            line = Line.new_line(pt1, pt2)
            if line in cnt_lines:
                cnt_lines[line] += 1
            else:
                cnt_lines[line] = 1
            if cnt_lines[line] > cnt_lines.get(best_line, 0):
                best_line = line
    return best_line
