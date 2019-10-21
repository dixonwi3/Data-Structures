######################
# Deque.py
######################
"""Defines all necessary objects and methods to use a deque"""
class Node:
    """
    A Node Object that holds data and points to the object
    in front of it and behind it in a Deque
    """
    def __init__(self, data=None):
        """Initializes a Node with data"""
        self.data = data
        # initializing an empty node that has no next nor prior node
        self.next = self.prior = None
class Deque:
    """
    A double-ended queue
    """
    def __init__(self):
        """
        Initializes an empty Deque
        """
        # initialize an empty node
        emptyNode = Node()
        # empty deque has size 0
        self.size = 0
        # front and back of deque are empty Nodes
        self.front = self.back = emptyNode
    def __len__(self):
        """
        Computes the number of elements in the Deque
        :return: The size of the Deque
        """
        return self.size
    def peek_front(self):
        """
        Looks at, but does not remove, the first element
        :return: The first element
        """
        # if the deque is empty
        if self.is_empty():
            # call an IndexError
            raise IndexError()
        # if deque is not empty, return front's data
        return self.front.data
    def peek_back(self):
        """
        Looks at, but does not remove, the last element
        :return: The last element
        """
        # if the deque is empty
        if self.is_empty():
            # raise an IndexError
            raise IndexError()
        # if deque is not empty, return back's data
        return self.back.data
    def push_front(self, e):
        """
        Inserts an element at the front of the Deque
        :param e: An element to insert
        """
        # initialize new Node with data e
        newNode = Node(e)
        # if the deque is empty
        if self.size == 0:
            # set the front and back to the new node
            self.front = self.back = newNode
        # if deque is not empty
        else:
            # previous front node is the prior to the new front Node
            newNode.prior = self.front
            # previous front node's next node is new node
            self.front.next = newNode
            # front node is the new node
            self.front = newNode
        # increment deque size
        self.size += 1
    def push_back(self, e):
        """
        Inserts an element at the back of the Deque
        :param e: An element to insert
        """
        # initialize new node with data e
        newNode = Node(e)
        # if deque is empty
        if self.size == 0:
            # set both front and back to new node
            self.front = self.back = newNode
        # if deque is not empty
        else:
            # set new node's next as the previous back, set previous back's
            # prior to the new node, and set the back of the deque to new node
            newNode.next = self.back
            self.back.prior = newNode
            self.back = newNode
        # increment deque size
        self.size += 1
    def pop_front(self):
        """
        Removes and returns the first element
        :return: The (former) first element
        """
        # set temp to deque's front for return
        temp = self.front
        # if deque is empty
        if self.size == 0:
            # raise IndexError
            raise IndexError()
        # if deque has one element
        elif self.size == 1:
            # empty the deque completely
            self.back = None
            self.front = None
            self.size -= 1
        # if the deque has more than one element
        else:
            # set front to front's prior node, set that node's next to
            # none, and decrement deque's size by 1
            self.front = self.front.prior
            self.front.next = None
            self.size -= 1
        # return previous front node's data
        return temp.data
    def pop_back(self):
        """
        Removes and returns the last element
        :return: The (former) last element
        """
        # set temp to back node of deque
        temp = self.back
        # if the deque is empty
        if self.size == 0:
            # raise IndexError
            raise IndexError()
        # if deque has one element
        elif self.size == 1:
            # empty the deque completely
            self.back = None
            self.front = None
            self.size -= 1
        # if deque has more than one element
        else:
            # set deque's back to previous back's next, set the new
            # back's prior to None, and decrement deque size
            self.back = self.back.next
            self.back.prior = None
            self.size -= 1
        # return previous back node's data
        return temp.data
    def clear(self):
        """
        Removes all elements from the Deque
        """
        # set front and back of deque to none, and size of deque to 0
        self.front = None
        self.back = None
        self.size = 0
    def __iter__(self):
        """
        Iterates over this Deque from front to back
        :return: An iterator
        """
        # set current node to front node
        current = self.front
        # while current != None
        while current:
            # send out current node's data
            yield current.data
            # move to next node
            current = current.prior
    def extend(self, other):
        """
        Takes a Deque object and adds each of its elements to the back of self
        :param other: A Deque object
        """
        # iterate through other deque
        for item in other:
            # if the current item's data is None
            if item is None:
                # that deque is empty, so we're done
                break
            # if other deque has items, push back current item and loop
            self.push_back(item)
    def drop_between(self, start, end):
        """
        Deletes elements from the Deque that within the range [start, end)
        :param start: indicates the first position of the range
        :param end: indicates the last position of the range(does not drop this element)
        """
        # catch all invalid args and throw an Index error if true
        if start < 0 or end > self.size or start > end:
            raise IndexError()
        # initialize node counter to 0
        counter = 0
        # current node for looping is front node
        current = self.front
        # while current node isn't None
        while current is not None:
            # if it's position is within start and end args
            if start <= counter < end:
                # skip the current node in the deque, effectively
                # deleting it
                current.prior.next = current.next
                # if current node's next is empty
                if current.next is None:
                    # you have one node left, and you have to get
                    # rid of it, so clear the deque and break
                    self.size = 0
                    self.front = None
                    self.back = None
                    break
                # set next node's prior to current's prior, effectively
                # skipping the current node in deque
                current.next.prior = current.prior
                # decrement size of deque
                self.size -= 1
            # add one to the counter
            counter += 1
            # move on to the next node who flows. He nose dove and sold
            # nada :)
            current = current.prior
    def count_if(self, criteria):
        """
        counts how many elements of the Deque satisfy the criteria
        :param criteria: a bool function that takes an element of the Deque
        and returns true if that element matches the criteria and false otherwise
        """
        # set count to 0
        count = 0
        # iterate through nodes in deque
        for item in self:
            # if the node's data meets the criteria passed,
            if criteria(item):
                # increment count
                count += 1
        # return the count
        return count
    # provided functions
    def is_empty(self):
        """
        Checks if the Deque is empty
        :return: True if the Deque contains no elements, False otherwise
        """
        return len(self) == 0
    def __repr__(self):
        """
        A string representation of this Deque
        :return: A string
        """
        return 'Deque([{0}])'.format(','.join(str(item) for item in self))
        
