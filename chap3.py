# Chap 3 - Stacks and Queues
import sys
from chap2 import Node


# 3.0.1
# Implement a stack
class Stack(object):
    def __init__(self):
        self._top = None

    def push(self, data):
        self._top = Node(data, self._top)
        return self

    def pop(self):
        if self._top:
            data = self._top.data
            self._top = self._top.next
            return data

    def peek(self):
        if self._top:
            return self._top.data

    def is_empty(self):
        return self._top is None

    def __str__(self):
        return str(self._top)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self._top == other
        return self._top == other._top


stack = Stack().push(0).push(1).push(2).push(3)
assert stack == Node(3, Node(2, Node(1, Node(0))))
assert stack.pop() == 3
assert stack.peek() == 2


# 3.0.1
# Implement a queue
class Queue(object):
    def __init__(self):
        self._first = self._last = None

    def enqueue(self, data):
        node = Node(data)
        if not self._first:
            self._first = self._last = node
        else:
            self._last.next = node
            self._last = node
        return self

    def dequeue(self):
        if self._first:
            data = self._first.data
            self._first = self._first.next
            return data

    def peek(self):
        if self._first:
            return self._first.data

    def is_empty(self):
        return self._first is None

    def __str__(self):
        return str(self._first)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self._first == other
        return self._first == other._first


queue = Queue().enqueue(0).enqueue(1).enqueue(2).enqueue(3)
assert queue == Node(0, Node(1, Node(2, Node(3))))
assert queue.dequeue() == 0


# 3.1
# Describe how to use a single array to implement three stacks
# We assume the three arrays have a fixed size
class StackArray(object):
    def __init__(self, array_size, num_stacks):
        self._array = [None] * array_size
        self._size = array_size / num_stacks
        self._stack_pt = [-1] * num_stacks

    def _abs_stack_pt(self, stack_no):
        return stack_no * self._size + self._stack_pt[stack_no]

    def _set(self, data, stack_no):
        self._array[self._abs_stack_pt(stack_no)] = data

    def _get(self, stack_no):
        return self._array[self._abs_stack_pt(stack_no)]

    # assume stack number is within range, also we don't cover the case
    # where last stack has one more element
    def push(self, data, stack_no):
        if self._stack_pt[stack_no] + 1 < self._size:
            self._stack_pt[stack_no] += 1
            self._set(data, stack_no)
        return self

    def pop(self, stack_no):
        index = self._stack_pt[stack_no]
        if index >= 0:
            data = self._array[self._abs_stack_pt(stack_no)]
            self._set(None, stack_no)
            self._stack_pt[stack_no] -= 1
            return data

    def peek(self, stack_no):
        if self._stack_pt[stack_no] >= 0:
            return self._get(stack_no)

    def __str__(self):
        return str(self._array)

    def __eq__(self, other):
        if isinstance(other, list):
            return self._array == other
        return self._array == other._array


def test_stack_array():
    stack = StackArray(10, 3).push(0, 0).push(1, 0).push(2, 1).push(3, 1).push(4, 2)
    assert stack == [0, 1, None, 2, 3, None, 4, None, None, None]
    assert stack.pop(0) == 1
    assert stack == [0, None, None, 2, 3, None, 4, None, None, None]
    assert stack.pop(2) == 4
    assert stack == [0, None, None, 2, 3, None, None, None, None, None]
    assert not stack.pop(2)
    stack.push(4, 2)
    assert stack == [0, None, None, 2, 3, None, 4, None, None, None]
    assert stack.peek(1) == 3
    stack.push(5, 2).push(6, 2).push(7, 2).push(100, 2)
    assert stack == [0, None, None, 2, 3, None, 4, 5, 6, None]

test_stack_array()


# 3.2
# Implement a stack which can return the min element in cst time
class StackMin(Stack):
    def __init__(self):
        super(StackMin, self).__init__()
        self._min_stack = Stack()

    def push(self, data):
        if data <= self.min() or self.min() is None:
            self._min_stack.push(data)
        return super(StackMin, self).push(data)

    def pop(self):
        data = super(StackMin, self).pop()
        if data <= self.min():
            self._min_stack.pop()
        return data

    def peek(self):
        return super(StackMin, self).peek()

    def min(self):
        return self._min_stack.peek()

stack = StackMin().push(1).push(3).push(0).push(3)
assert stack.min() == 0
assert stack.pop() == 3
assert stack.min() == 0
assert stack.pop() == 0
assert stack.min() == 1


# 3.3.0
# Implement a SetOfStacks which behave like a normal single stack
# Follow up: implement a pop_at(index) which performs pop operation
# on a given stack
class SetOfStacks(object):
    def __init__(self, capacity):
        self._capacity = capacity
        self._last = -1
        self._stacks = [Stack()]

    def _push_at(self, data, stack_no):
        if stack_no >= len(self._stacks):
            self._stacks.append(Stack())
            stack_no += 1
        return self._stacks[stack_no].push(data)

    def pop_at(self, stack_no):
        data = self._stacks[stack_no].pop()
        if data is None and stack_no > 0:
            del self._stacks[stack_no]
            return self._stacks[stack_no-1].pop()
        return data

    def push(self, data):
        self._last += 1
        return self._push_at(data, self._last / self._capacity)

    def pop(self):
        data = self.pop_at(self._last / self._capacity)
        self._last -= 1
        return data

    def peek(self):
        return self._stack[self._last].peek()

    def __repr__(self):
        return [stack.to_python_list() for stack in self._stacks]

    def __eq__(self, other):
        if isinstance(other, list):
            return self._stacks == other
        return self._stacks == other._stacks


# stack = SetOfStacks(2).push(0).push(1).push(2).push(3).push(4)
# print stack
# assert stack == [[0, 1], [2, 3], [4]]


# 3.4
# Implement a solution to the classic tower of Hanoi problem
class Tower(Stack):
    def __init__(self, num_disks):
        super(Tower, self).__init__()
        for i in range(num_disks)[::-1]:
            self.push(i)
        self._num_disks = num_disks

    def move(self, n, t3, t2):
        if n <= 0:
            return
        else:
            # take n-1 disks from t1 to t3 using t2
            self.move(n-1, t2, t3)
            # move disk n to t3
            self.move_top(t3)
            # take n-1 disks from t2 to t3 using t1
            t2.move(n-1, t3, self)

    def move_top(self, to):
        if self.peek() is not None:
            to.push(self.pop())
            self._num_disks -= 1

    def solve(self, t2, t3):
        t1.move(self._num_disks, t3, t2)

t1, t2, t3 = Tower(5), Tower(0), Tower(0)
t1.solve(t2, t3)
assert t3 == Node(0, Node(1, Node(2, Node(3, Node(4)))))


# 3.5
# Implement a queue using two stacks
class MyQueue(object):
    def __init__(self):
        self._stack_enqueue = Stack()
        self._stack_dequeue = Stack()

    def _rollover(self):
        while self._stack_enqueue.peek() is not None:
            self._stack_dequeue.push(self._stack_enqueue.pop())

    def enqueue(self, data):
        self._stack_enqueue.push(data)
        return self

    def dequeue(self):
        if self._stack_dequeue.peek() is None:
            self._rollover()
        return self._stack_dequeue.pop()

queue = MyQueue().enqueue(0).enqueue(1).enqueue(2).enqueue(3)
assert queue.dequeue() == 0
assert queue.dequeue() == 1
assert queue.dequeue() == 2
assert queue.enqueue(0)
assert queue.dequeue() == 3
assert queue.dequeue() == 0


# 3.6
# Sort a stack in ascending order only using possibly additional stacks
def sort_stack(stack):
    result, buffer = Stack(), Stack()
    while not stack.is_empty():
        # find the smallest element
        smallest = sys.maxsize
        while not stack.is_empty():
            data = stack.pop()
            if data < smallest:
                smallest = data
            buffer.push(data)
        # store the elements back in the stack
        while not buffer.is_empty():
            data = buffer.pop()
            if data == smallest:
                result.push(data)
            else:
                stack.push(data)
    return result

stack = Stack().push(2).push(3).push(1).push(0)
stack = sort_stack(stack)
assert stack == Node(3, Node(2, Node(1, Node(0))))


# Another slightly more efficient and elegant solution consists
# of inserting the smallest element instead of finding it
# (insertion sort vs. selection sort)
def sort_stack(stack):
    result = Stack()
    while not stack.is_empty():
        data = stack.pop()
        while result.peek() is not None and data > result.peek():
            stack.push(result.pop())
        result.push(data)
    return result


stack = sort_stack(stack)
assert stack == Node(0, Node(1, Node(2, Node(3))))


# 3.7
# People bring in either a cat or a dog to an animal shelter,
# and can get the oldest of the animal brought in with a
# preference for a cat or a dog if they'd like.
class AnimalShelterQueue(object):
    def __init__(self):
        self._time = 0
        self._queue_cat = Queue()
        self._queue_dog = Queue()

    # assume we have an actual animal no duck typing
    def enqueue(self, animal):
        animal.set_priority(self._time)
        if isinstance(animal, Cat):
            self._queue_cat.enqueue(animal)
        else:
            self._queue_dog.enqueue(animal)
        self._time += 1
        return self

    def dequeue(self):
        cat, dog = self._queue_cat.peek(), self._queue_dog.peek()
        if cat is None:
            return self.dequeue_dog()
        if dog is None:
            return self.dequeue_cat()
        if cat <= dog:
            return self.dequeue_cat()
        else:
            return self.dequeue_dog()

    def dequeue_cat(self):
        return self._queue_cat.dequeue()

    def dequeue_dog(self):
        return self._queue_dog.dequeue()


class Animal(object):
    def __init__(self, name):
        self._name = name
        self._priority = 0

    def set_priority(self, priority):
        self._priority = priority

    def __le__(self, other):
        return self._priority <= other._priority

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return self.__class__.__name__ + ": " + self._name


class Cat(Animal):
    pass


class Dog(Animal):
    pass


shelter = AnimalShelterQueue()
shelter.enqueue(Dog("Barnie")).enqueue(Dog("Toby")).enqueue(Cat("Noe")).enqueue(Dog("Roger")).enqueue(Cat("Elise"))
assert shelter.dequeue_dog() == Dog("Barnie")
assert shelter.dequeue_cat() == Cat("Noe")
assert shelter.dequeue() == Dog("Toby")
assert shelter.dequeue() == Dog("Roger")
assert shelter.dequeue() == Cat("Elise")
