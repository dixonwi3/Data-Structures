######################
# Heap.py
######################
"""
Defines all necessary classes and functions for the implementation of
a Heap data structure
"""
import math # This allows for the use of the floor function
class Heap:
    """
    A heap-based priority queue
    Items in the queue are ordered according to a comparison function
    """
    def __init__(self, comp):
        """
        Constructor
        :param comp: A comparison function determining the priority of the
        included elements
        """
        self.heap = []
        self.length = 0
        self.comp = comp
    def __len__(self):
        """
        Finds the number of items in the heap
        :return: The size
        """
        return self.length
    def peek(self):
        """
        Finds the item of highest priority
        :return: The item item of highest priority
        """
        return self.heap[0]
    def insert(self, item):
        """
        Adds the item to the heap
        :param item: An item to insert
        """
        i = self.length
        # append the new item to the end of the list and increase length
        # of heap
        self.heap.append(item)
        self.length += 1
        # while we're not dealing with the root of the heap, and
        # the item has higher priority than its parent
        while i > 0 and self.comp(item, self.heap[parent(i)]):
            # swap the parent and the item and set i to track the item
            self.heap[i] = self.heap[parent(i)]
            i = parent(i)
        self.heap[i] = item
    def extract(self):
        """
        Removes the item of highest priority
        :return: the item of highest priority
        """
        # cannot extract from an empty heap
        if self.is_empty():
            raise IndexError
        minimum = self.heap[0]
        # Move last item in heap to root
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self.length -= 1
        # refactor the heap
        self.heapify(0)
        return minimum
    def heapify(self, p):
        """
        Recursively refactors a heap to follow the rules of a heap
        :param p: the index of the parent of the item in the heap
        """
        # find the left and right children of the parent
        l = left(p)
        r = right(p)
        # if left child has higher priority than its parent
        if l < self.length and self.comp(self.heap[l], self.heap[p]):
            # it will become the new parent
            extreme = l
        # if not, the parent stays
        else:
            extreme = p
        # if the right child has higher priority than its parent
        if r < self.length and self.comp(self.heap[r], self.heap[extreme]):
            # it will become the new parent
            extreme = r
        # if parent doesn't stay, perform swap on child and parent
        if extreme != p:
            # Swap
            (self.heap[p], self.heap[extreme]) = \
                (self.heap[extreme], self.heap[p])
            self.heapify(extreme)
    def extend(self, seq):
        """
        Adds all elements from the given sequence to the heap
        :param seq: An iterable sequence
        """
        # insert all items from the sequence into the heap
        for item in seq:
            self.insert(item)
    def replace(self, item):
        """
        Adds the item to the heap and returns the new highest-priority item
        Faster than insert followed by extract.
        :param item: An item to insert
        :return: The item of highest priority
        """
        # if the heap is empty or the item would become the new root
        if self.is_empty() or self.comp(item, self.heap[0]):
            # just return the item
            return item
        # if not, get the root for return
        root = self.heap[0]
        # make the new root the item
        self.heap[0] = item
        self.heapify(0)
        return root
    def clear(self):
        """
        Removes all items from the heap
        """
        # loop and delete each item in the heap array
        del self.heap[:]
        self.length = 0
    def __iter__(self):
        """
        An iterator for this heap
        :return: An iterator
        """
        for item in self.heap:
            yield item
    def __bool__(self):
        """
        Checks if this heap contains items
        :return: True if the heap is non-empty
        """
        return not self.is_empty()
    def is_empty(self):
        """
        Checks if this heap is empty
        :return: True if the heap is empty
        """
        return len(self) == 0
    def __repr__(self):
        """
        A string representation of this heap
        :return:
        """
        return 'Heap([{0}])'.format(','.join(str(item) for item in self))
# Required Non-heap member function
def find_median(seq):
    """
    Finds the median (middle) item of the given sequence.
    Ties are broken arbitrarily.
    :param seq: an iterable sequence
    :return: the median element
    """
    if not seq:
        raise IndexError
    # initialize the two necessary heaps and the median
    min_heap = Heap(lambda a, b: a < b)
    max_heap = Heap(lambda a, b: a > b)
    # loop through each item in the sequence
    for item in seq:
        minSize = len(min_heap)
        maxSize = len(max_heap)
        # find the correct median based on the sizes of the two heaps
        if minSize == 0 and maxSize == 0:
            median = 0
        elif minSize > maxSize:
            median = min_heap.peek()
        elif minSize < maxSize:
            median = max_heap.peek()
        else:
            median = (min_heap.peek() + max_heap.peek()) // 2
        # item goes in minheap if it's greater than the median, goes to
        # maxheap otherwise
        if item > median:
            min_heap.insert(item)
        else:
            max_heap.insert(item)
        # get the new sizes of the heaps
        minSize = len(min_heap)
        maxSize = len(max_heap)
        # rebalance the heaps if one has two elements more than the other
        if minSize > maxSize + 1:
            max_heap.insert(min_heap.extract())
        if maxSize > minSize + 1:
            min_heap.insert(max_heap.extract())
    # if one heap has more elements than the other, its top holds the median
    if len(min_heap) > len(max_heap):
        return min_heap.peek()
    if len(max_heap) > len(min_heap):
        return max_heap.peek()
    # if they have the same number of elements, choose the maxheap's median
    else:
        return max_heap.peek()
def left(index):
    """
    Gets the index of the left child of a node in the heap list
    :param index: the index of the parent in the heap list
    :return: the index of the the left child
    """
    return 2 * index + 1
def right(index):
    """
    Gets the index of the right child of an item in the heap
    :param index: the index of the parent in the heap list
    :return: the index of the right child
    """
    return 2 * index + 2
def parent(index):
    """
    Finds the index of an item's parent
    :param index: the index of the item in the array to find the parent of
    :return: the index of the parent of the item in the heap
    """
    return int(math.floor((index - 1) // 2))
