import random
from chap4 import TreeNode


# You are given the pre-order traversal of a tree as well
# as its in-order traversal. Using these two lists generate
# the tree.
def make_tree(pre_order, in_order):
    if not pre_order:
        return

    tree = TreeNode(pre_order[0])
    index = in_order.index(tree.data)

    in_order_left = in_order[:index]
    in_order_right = in_order[index+1:]

    pre_order_left = [x for x in pre_order if x in in_order_left]
    pre_order_right = [x for x in pre_order if x in in_order_right]

    tree.left = make_tree(pre_order_left, in_order_left)
    tree.right = make_tree(pre_order_right, in_order_right)

    return tree


def make_random_tree(data):
    if not data:
        return

    tree = TreeNode(data.pop())
    leaf = random.choice((1, 2, 3))
    if leaf == 1 or leaf == 3:  # left or both leaves
        tree.left = make_random_tree(data)
    if leaf == 2 or leaf == 3:  # right or both leaves
        tree.right = make_random_tree(data)
    return tree


def test(size=10):
    # make a random tree with 10 nodes
    tree = make_random_tree(range(size))
    # get the array obtained by pre-order traversal
    pre_order = map(int, tree.pre_order().split())
    # get the array obtained by in-order traversal
    in_order = map(int, tree.in_order().split())
    # make a tree from these arrays
    assert make_tree(pre_order, in_order) == tree

# test on trees of size from 0 to 99
for i in range(1, 100):
    test(i)
