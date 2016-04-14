# Chap 5 - Bit Manipulation

# 5.0.1
# Do the following bit wise operation by hand
assert 0b0110 + 0b0011 == 6 + 3 == 0b1001

assert 0b0011 + 0b0011 == 0b0011 << 1 == 0b0110

assert 0b0110 - 0b0011 == 6 - 3 == 0b0011 == 3

assert 0b1000 - 0b0110 == 8 - 6 == 2

assert 0b0011 * 0b0101 == 3 * 5 == 15

assert 0b0011 * 0b0011 == 0b0011 * (2 + 1) == (0b0011 << 1) + 0b0011 == 0b1001

assert 0b1101 >> 2 == 0b0011

assert 0b1101 ^ 0b0101 == 0b1000

assert 0b0110 + 0b0110 == 2 * 0b0110 == 0b0110 << 1 == 0b1100

assert 0b0100 * 0b0011 == 0b0011 * 2 * 2 == 0b0011 << 2 == 0b1100

assert 0b1101 ^ (~0b1101 & 0xF) == 0b1111  # we need to add mask to get true bitwise inversion

assert 0b1011 & (~0 & 0xF << 2) == 0b1011 & 0b1100 == 0b1000  # we need to add mask to get true bitwise inversion


# 5.0.2
# Implement get, set, clear and update bit
def get_bit(n, i):
    return 0 if (n & 1 << i) == 0 else 1

assert get_bit(0b011010001, 7) == 1
assert get_bit(0b011010001, 1) == 0


def set_bit(n, i):
    return n | (1 << i)

assert set_bit(0b011010001, 3) == 0b011011001
assert set_bit(0b011010001, 1) == 0b011010011


def clear_bit(n, i):
    return n & ~(1 << i)

assert clear_bit(0b011010001, 7) == 0b001010001
assert clear_bit(0b011010001, 1) == 0b011010001


def clear_most_sig_bits(n, i):
    return n & ((1 << i) - 1)

assert clear_most_sig_bits(0b011010001, 4) == 0b000000001
assert clear_most_sig_bits(0b011010001, 6) == 0b000010001


def clear_least_sig_bits(n, i):
    return n & ~((1 << (i + 1)) - 1)

assert clear_least_sig_bits(0b011010001, 4) == 0b011000000
assert clear_least_sig_bits(0b011010001, 3) == 0b011010000


def update_bit(n, i, v):
    return (n & ~(1 << i)) | (v << i)

assert update_bit(0b011010001, 7, 0) == 0b001010001
assert update_bit(0b011010001, 1, 1) == 0b011010011


# 5.1
# Given two 32-bit numbers A, B, insert B into A at a given
# position i to j. Assume there is enough room in A to insert
# B.
def insert_bits(A, B, i, j):
    mask = ((1 << i) -1) | ~((1 << j) - 1)
    return (A & mask) | (B << i)

assert insert_bits(0b1101000111, 0b10101, 2, 7) == 0b1101010111
assert insert_bits(0b1101000111, 0b101, 4, 7) == 0b1101010111


# 5.2
# Similarly to the binary representation of integers, floating point
# numbers can be can be written as n = (1/2)^1 * a1 + (1/2)^2 * a2 + ... + (1/2)^n * an.
# Write a method to return this representation if possible, otherwise
# return an error.
# Example: .0101 == (1/2)^1 * 0 + (1/2)^2 * 1 + (1/2)^3 * 0 + (1/2)^4 * 1
def bin_real(n):
    r, d = '.', 0
    while n != 0 and d <= 32:
        n *= 2
        if n >= 1:
            r += '1'
            n -= 1
        else:
            r += '0'
        d += 1
    return r if d < 32 else None

assert bin_real(1.0/(2**2) + 1.0/(2**4)) == '.0101'
assert bin_real(1.0/(2**1) + 1.0/(2**2) + 1.0/(2**4) + 1.0/(2**8)) == '.11010001'
assert not bin_real(0.33)


# 5.4
# Explain what the following code does: (n & (n-1)) == 0

# If n!=0 then let's write n as abcfef100 with 1 being the least
# significant 1s.
# Then (n & (n-1)) == 0 iff abcfef100 & abcfef011 == 0
# iff a,b,c,d,e,f == 0 iff n is a power of 2
def is_power_of_2(n):
    return True if n != 0 and (n & (n-1)) == 0 else False

assert is_power_of_2(32)
assert not is_power_of_2(33)


# 5.5
# Write a method to determine the number of bits required to
# convert integer A into integer B.
def number_bits_convert(A, B):
    A, c = A ^ B, 0
    while A > 0:
        c += A & 1
        A >>= 1
    return c

assert number_bits_convert(0b011010001, 0b000010001) == 2
assert number_bits_convert(0b001010101, 0b010010101) == 2
assert number_bits_convert(0b111111111, 0b010010101) == 5


# 5.6
# Write a program to swap odd and even bits in an integers with
# as few instructions as possible.
def swap_odd_even_bits(n):
    even, odd = 0x55, 0xAA
    return (n & even) << 1 | (n & odd) >> 1

assert swap_odd_even_bits(0b11010001) == 0b11100010
assert swap_odd_even_bits(0b01010101) == 0b10101010
