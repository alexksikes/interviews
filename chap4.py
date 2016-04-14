# Chap 4 - Trees and Graphs
from chap3 import Queue


# 4.0.1
# Implement pre-order, in-order and post-order traversal
class TreeNode(object):
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def pre_order(self):
        result = str(self.data)
        if self.left:
            result += " " + self.left.pre_order()
        if self.right:
            result += " " + self.right.pre_order()
        return result

    def in_order(self):
        result = ""
        if self.left:
            result += self.left.in_order() + " "
        result += str(self.data)
        if self.right:
            result += " " + self.right.in_order()
        return result

    def post_order(self):
        result = ""
        if self.left:
            result += self.left.post_order() + " "
        if self.right:
            result += self.right.post_order() + " "
        result += str(self.data)
        return result

    def __str__(self):
        return "(%s %s %s)" % (self.data, self.left or ".", self.right or ".")

    def __eq__(self, other):
        return self.data == other.data and \
               self.left == other.left and \
               self.right == other.right

tree = TreeNode(0, TreeNode(1, TreeNode(2), TreeNode(3)), TreeNode(4, TreeNode(5), TreeNode(6)))
assert tree.pre_order() == "0 1 2 3 4 5 6"
assert tree.in_order() == "2 1 3 0 5 4 6"
assert tree.post_order() == "2 3 1 5 6 4 0"


# 4.0.1
# Implement breath first search and depth first search
class GraphNode(object):
    def __init__(self, data, *adjacent):
        self.data = data
        self.visited = False
        self.adjacent = adjacent if adjacent else []

    def dfs(self):
        self.visited = True
        result = str(self.data)
        for n in self.adjacent:
            if not n.visited:
                result += " " + n.dfs()
        return result

    def bfs(self):
        queue = Queue().enqueue(self)
        result = ""
        while not queue.is_empty():
            root = queue.dequeue()
            root.visited = True
            result += str(root.data) + " "
            for n in root.adjacent:
                if not n.visited:
                    queue.enqueue(n)
        return result

    def __eq__(self, other):
        return self.dfs() == other.dfs()

graph = GraphNode(0, GraphNode(1), GraphNode(2), GraphNode(3), GraphNode(4, GraphNode(5)), GraphNode(6, GraphNode(7)))
graph.adjacent[-1].adjacent[-1].adjacent.append(graph)  # have a loop in there
assert graph.dfs() == "0 1 2 3 4 5 6 7"

graph = GraphNode(0, GraphNode(1), GraphNode(2), GraphNode(3), GraphNode(4, GraphNode(5)), GraphNode(6, GraphNode(7)))
graph.adjacent[-1].adjacent[-1].adjacent.append(graph)
assert graph.bfs() == "0 1 2 3 4 6 5 7 "


# 4.1
# Write a function to check whether a binary tree is balanced
# A binary tree is balanced if at any node the heights of its
# left and right subtree do not differ by more than one.
def is_balanced(tree):
    if tree is None:
        return True
    diff = abs(get_height(tree.left) - get_height(tree.right))
    if diff > 1:
        return False
    else:
        return is_balanced(tree.left) and is_balanced(tree.right)


def get_height(tree):
    if tree is None:
        return 0
    return 1 + max(get_height(tree.left), get_height(tree.right))


tree = TreeNode(0, TreeNode(1, TreeNode(2), TreeNode(3)), TreeNode(4, TreeNode(5), TreeNode(6)))
assert is_balanced(tree)
tree = TreeNode(0, TreeNode(3, TreeNode(4)), TreeNode(5, TreeNode(6, TreeNode(7))))
assert not is_balanced(tree)


# However we are re-computing the height at each node, instead
# we can either save this value or simply check the height
def check_height(tree):
    if tree is None:
        return 0
    leftHeight = check_height(tree.left)
    if leftHeight -1:
        return -1
    rightHeight = check_height(tree.right)
    if rightHeight == -1:
        return -1
    diff = abs(leftHeight - rightHeight)
    if diff > 1:
        return -1
    else:
        return 1 + max(leftHeight, rightHeight)


def is_balanced2(tree):
    return check_height(tree) != -1


tree = TreeNode(0, TreeNode(1, TreeNode(2), TreeNode(3)), TreeNode(4, TreeNode(5), TreeNode(6)))
assert is_balanced(tree)
tree = TreeNode(0, TreeNode(3, TreeNode(4)), TreeNode(5, TreeNode(6, TreeNode(7))))
assert not is_balanced(tree)


# 4.2
# Given a directed graph, determine whether there is a route between two nodes
def route_between(node1, node2, found=False):
    if found or node1 is node2:
        return True
    node1.visited = True
    for n in node1.adjacent:
        if not n.visited:
            found = route_between(n, node2, found)
    return found

A, B, C = GraphNode(0), GraphNode(1), GraphNode(2)
A.adjacent = [GraphNode(3, GraphNode(4, A), GraphNode(5, B), GraphNode(6, C))]
assert route_between(A, B)
A.visited = B.visited = C.visited = False
A.adjacent = [GraphNode(3, GraphNode(4, A), GraphNode(5, B), GraphNode(6, C))]
assert route_between(A, C)
A.visited = B.visited = C.visited = False
A.adjacent = [GraphNode(3, GraphNode(4, A), GraphNode(5, B), GraphNode(6, C))]
assert not route_between(B, C)


# 4.3
# Given a sorted array, create a binary search tree of minimum height
def make_bst(array):
    mid = len(array)/2
    if mid == 0:
        return TreeNode(array[0])
    elif mid == 1:
        return TreeNode(array[1], TreeNode(array[0]))
    else:
        return TreeNode(array[mid], make_bst(array[:mid]), make_bst(array[mid+1:]))

a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
assert make_bst(a).in_order() == "0 1 2 3 4 5 6 7 8 9"


# 4.4
# Given a binary search tree, return a list of the nodes at every level
def create_level_list(tree):
    levels = []
    def _get_level_list(tree, level):
        if tree is None:
            return
        if level >= len(levels):
            levels.append([tree.data])
        else:
            levels[level].append(tree.data)
        _get_level_list(tree.left, level+1)
        _get_level_list(tree.right, level+1)
    _get_level_list(tree, 0)
    return levels

tree = TreeNode(0, TreeNode(1, TreeNode(2), TreeNode(3)), TreeNode(4, TreeNode(5), TreeNode(6)))
assert create_level_list(tree) == [[0], [1, 4], [2, 3, 5, 6]]


# 4.5
# Check whether a binary tree is a binary search tree
def check_bst(tree, is_bst=True):
    if not is_bst:
        return False
    if tree.left and not tree.left.data <= tree.data:
        return False
    if tree.right and not tree.data < tree.right.data:
        return False
    if tree.left:
        is_bst = check_bst(tree.left, is_bst)
    if tree.right:
        is_bst = check_bst(tree.right, is_bst)
    return is_bst

tree = make_bst([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
assert check_bst(tree)
tree = TreeNode(0, TreeNode(1, TreeNode(2), TreeNode(3)), TreeNode(4, TreeNode(5), TreeNode(6)))
assert not check_bst(tree)


# checking in-order traversal is sorted
def check_bst2(tree):
    def copy_in_order(tree, array):
        if not tree:
            return
        copy_in_order(tree.left, array)
        array.append(tree.data)
        copy_in_order(tree.right, array)

    def is_sorted(array):
        for a, b in zip(array, array[1:]):
            if a > b:
                return False
        return True
    array = []
    copy_in_order(tree, array)
    return is_sorted(array)

tree = make_bst([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
assert check_bst2(tree)
tree = TreeNode(0, TreeNode(1, TreeNode(2), TreeNode(3)), TreeNode(4, TreeNode(5), TreeNode(6)))
assert not check_bst2(tree)


# 4.9
# Design an algorithm that prints all paths which sum to a given value
def find_paths(tree, value):
    def find_paths_to(tree, paths, level):
        if tree is None:
            return
        # the current path we are in is paths[0:level]
        if level >= len(paths):
            paths.append(tree.data)
        else:
            paths[level] = tree.data
        # find path from the current node till the potentially root
        sum = 0
        for i, data in enumerate(paths[level::-1]):
            sum += data
            if sum == value:
                found_paths.append(paths[level::-1][:i+1][::-1])
        # recurse to each subtree
        find_paths_to(tree.left, paths, level + 1)
        find_paths_to(tree.right, paths, level + 1)

    found_paths = []
    find_paths_to(tree, [], 0)
    return found_paths

tree = make_bst([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
assert find_paths(tree, 8) == [[5, 2, 1], [5, 2, 1, 0], [8]]
assert find_paths(tree, 17) == [[8, 9]]
assert find_paths(tree, 4) == [[4]]
assert find_paths(tree, 7) == [[5, 2], [4, 3], [7]]
assert find_paths(tree, 5) == [[5]]
