# Chapter 2 - Linked Lists


# 2.0.1 Implement a basic link list
# We are give this simple Node class
class Node(object):
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next

    def append_to_tail(self, node):
        if self.is_empty():
            self.data = node.data
            self.next = node.next
        else:
            n = self
            while n.next is not None:
                n = n.next
            n.next = node

    def to_python_list(self):
        if self.is_empty():
            return []

        n, lst = self, []
        while n is not None:
            lst.append(n.data)
            n = n.next
        return lst

    def is_empty(self):
        return self.data is None and self.next is None

    def __str__(self):
        return str(self.to_python_list())

    def __eq__(self, other):
        return self.to_python_list() == other.to_python_list()

lst = Node(0, Node(1, Node(2, Node(3))))
lst.append_to_tail(Node(4))

assert lst == Node(0, Node(1, Node(2, Node(3, Node(4)))))


# 2.0.2 Delete a node from a singly linked list
# Assume two nodes are equal is they have the same data
def delete_node(head, data):
    if head.data == data:
        return head.next

    n = head
    while n.next is not None:
        if n.next.data == data:
            n.next = n.next.next
            return head
        n = n.next

    return head

lst = delete_node(lst, 2)

assert lst == Node(0, Node(1, Node(3, Node(4))))


# 2.1
# Remove duplicates from an unsorted linked list
def remove_duplicates(head):
    seen, n = {head.data}, head
    while n.next is not None:
        if n.next.data in seen:
            n.next = n.next.next
        else:
            seen.add(n.next.data)
            n = n.next
    return head

lst = Node(0, Node(1, Node(2, Node(3))))
lst.append_to_tail(Node(0, Node(1, Node(2, Node(3)))))

assert lst == Node(0, Node(1, Node(2, Node(3, Node(0, Node(1, Node(2, Node(3))))))))
assert remove_duplicates(lst) == lst


# 2.2
# Find the kth to last element in a singly linked list
def kth_to_last(head, k):
    # move pointer ahead k steps
    p1 = head
    for steps in range(k):
        if p1.next is None:
            return None # too short didn't find
        p1 = p1.next
    # move p2 till p1 hits the end
    p2 = head
    while p1.next is not None:
        p1 = p1.next
        p2 = p2.next
    return p2

lst = Node(0, Node(1, Node(2, Node(3, Node(4)))))

assert kth_to_last(lst, 1) == Node(3, Node(4))
assert not kth_to_last(lst, 5)


# 2.3 Delete a node in the middle of a singly linked list
# given only access to that node
def delete_node(node):
    node.data = node.next.data
    node.next = node.next.next
    return node

assert delete_node(Node(2, Node(3, Node(4)))) == Node(3, Node(4))


# 2.4 Partition a singly linked list around a value x so that
# all nodes less than x comes before all nodes greater or equal to x.
def partition(head, x):
    n, left, right = head, Node(), Node()
    while n is not None:
        if n.data < x:
            left.append_to_tail(Node(n.data))
        else:
            right.append_to_tail(Node(n.data))
        n = n.next
    left.append_to_tail(right)
    return left

lst = Node(3, Node(2, Node(2, Node(1, Node(0)))))
assert partition(lst, 2) == Node(1, Node(0, Node(3, Node(2, Node(2)))))


# 2.5.0
# Implement digit wise addition with two singly linked lists
# Assume each node has a digit and the digits are in backward order
def add(lst1, lst2):
    def _add(n1, n2, node, carry):
        sum = carry
        if n1:
            sum += n1.data
            n1 = n1.next
        if n2:
            sum += n2.data
            n2 = n2.next
        if sum > 0:
            node.data = sum % 10

        # is there more to add?
        carry = sum / 10
        if n1 or n2 or carry:
            node.next = Node()
            return _add(n1, n2, node.next, carry)
        else:
            return result
    result = Node()
    node = result
    return _add(lst1, lst2, node, 0)

a = Node(3, Node(2, Node(1)))
b = Node(9, Node(5))
assert add(a, b) == Node(2, Node(8, Node(1)))


# 2.5.1
# Follow up, assume the digits are stored in forward order
def add2(lst1, lst2):
    def _pad(lst1, lst2):
        # we assume length in cst time otherwise there is no point
        diff = length(lst1) - length(lst2)
        if diff < 0:
            lst1 = pad(lst1, -1 * diff)
        if diff > 0:
            lst2 = pad(lst2, diff)
        return lst1, lst2

    def _add(n1, n2, result):
        if not n1 and not n2:
            return None, None
        sum, result = _add(n1.next, n2.next, result)
        if sum is None:
            sum = n1.data + n2.data
        else:
            sum = n1.data + n2.data + sum / 10
        if result is None:
            result = Node(sum % 10)
        else:
            result = insert_before(sum % 10, result)
        return sum, result

    lst1, lst2 = _pad(lst1, lst2)
    sum, result = _add(lst1, lst2, None)
    return result


def length(head):
    size, pt = 0, head
    while pt:
        size +=1
        pt = pt.next
    return size


def pad(head, by):
    for i in range(by):
        head = insert_before(0, head)
    return head


def insert_before(data, head):
    prev = head
    head = Node(data)
    head.next = prev
    return head


a = Node(1, Node(2, Node(3)))
b = Node(5, Node(9))
assert add2(a, b) == Node(1, Node(8, Node(2)))


# 2.6 Return the node at the beginning of the loop of a circular linked list
# Assume the list is actually circular
def find_loop(head):
    pt, runner = head.next, next_node(head, 2)
    while pt is not runner:
        pt = pt.next
        runner = next_node(runner, 2)
    pt = head
    while pt is not runner:
        pt = pt.next
        runner = runner.next
    return pt


def next_node(head, by):
    for i in range(by):
        if head:
            head = head.next
    return head

start = Node(4)
lst = Node(0, Node(1, Node(2, Node(3, start))))
start.next = Node(5, Node(6, start))
assert find_loop(lst) is start


# 2.7
# Check whether a linked list is palindrome
def is_palindrome(head):
    pt, runner, data = head, head, []
    while runner:
        data.append(pt.data)
        runner = next_node(runner, 2)
        if runner:
            pt = pt.next
    while pt:
        if pt.data != data.pop(-1):
            return False
        pt = pt.next
    return True

assert is_palindrome(Node(0, Node(1, Node(2, Node(1, Node(0))))))
assert not is_palindrome(Node(0, Node(1, Node(2, Node(1, Node(1))))))
