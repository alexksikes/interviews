# Some unfinished exercises


# 17.5
# The Game of Master Mind is played as follows:
#
# The computer has four slots containing balls that are red (R), yellow (Y),
# green (G) or blue (B). For example, the computer might have RGGB (e.g., Slot
# #1 is red, Slots #2 and #3 are green, Slot #4 is blue). You, the user, are
# trying to guess the solution. You might, for example, guess YRGB. When you
# guess the correct color for the correct slot, you get a "hit". If you guess a
# color that exists but is in the wrong slot, you get a 'pseudo-hit'. For
# example, the guess YRGB has 2 hits and one pseudo hit. For each guess, you are
# told the number of hits and pseudo-hits.
#
# Write a method that, given a guess and a solution, returns the number of hits
# and pseudo hits.
class MasterMind(object):
    def __init__(self, solution):
        self._solution = solution

    def guess(self, guess_):
        hits, cnt = 0, 0
        for a, b in zip(guess_, self._solution):
            if a in self._solution:
                cnt += 1
            if a == b:
                hits += 1
        return dict(hits=hits, pseudo_hits=cnt - hits)

# assert MasterMind("RGGB").guess("YRGB") == dict(hits=2, pseudo_hits=1)
# assert MasterMind("RGGB").guess("YRRR") == dict(hits=0, pseudo_hits=1)
# assert MasterMind("RGGB").guess("YYYY") == dict(hits=0, pseudo_hits=0)
# assert MasterMind("RGBG").guess("RGGB") == dict(hits=2, pseudo_hits=2)
# assert MasterMind("RGGB").guess("RGGB") == dict(hits=4, pseudo_hits=0)


# # 18.12
# # Given an NxN matrix of positive and negative integers, find the sub-matrix
# # with the largest possible sum.
# from chap17 import largest_sum_seq
# def largest_sum_matrix(A):
#     def sum_col(from_, to):
#         pass
#
#     N = len(A)
#     for size in range(N, 1):
#         a = []
#         for i in range(N):
#             a.append(sum_col())
#
#
#     size = len(A)
#     for i in range(len(A)):
#
#
#
#     sum, best_sum = 0, 0
#     seq, best_seq = [], []
#     for e in a:
#         sum += e
#         seq.append(e)
#         if sum > best_sum:
#             best_sum, best_seq = sum, copy.copy(seq)
#         if sum < 0:
#             sum, seq = 0, []
#     return best_seq
#
# print largest_sum_matrix([
# [1,2,3,-4,5,6]
# [1,2,3,4,5,-6]
# [1,2,3,-4,5,6]
# [1,-2,3,4,5,6]
# [1,-2,3,4,5,6]
# [1,2,-3,4,5,6]])
#
# assert largest_sum_matrix(a) == [9, -4, 7]