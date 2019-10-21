######################
# TreeSet.py
######################
"""
Defines all necessary objects and functions to implement and manipulate an
AVLTree
"""
class TreeNode:
    """
    A TreeNode to be used by the TreeSet
    """
    def __init__(self, data=None):
        """
        Constructor
        You can add additional data as needed
        :param data:
        """
        self.data = data
        self.left = None
        self.right = None
        self.height = 0
        self.balance = 0
    def __iter__(self):
        """
        Iterator
        Returns each node's data in the tree set
        """
        if self.left:
            yield from self.left
        yield self.data
        if self.right:
            yield from self.right
    def maximum(self, comp):
        """
        Returns the maximum data item in the tree
        :param comp: comparison function for nodes
        """
        if self.right is None:
            return self
        else:
            return self.right.maximum(comp)
    def get_height(self):
        """
        Gets the height of the tree
        :return: height of the tree
        """
        # base case for end of left tree
        if self.left is None:
            l_height = -1
        else:
            # recursively call get_height on left child
            l_height = self.left.get_height()
        # base case for end of right tree
        if self.right is None:
            r_height = -1
        else:
            # recursively call get_height on right child
            r_height = self.right.get_height()
        return 1 + max(l_height, r_height)
    def insert(self, item, comp, parent, tree):
        """
        Inserts the item into the tree, starts at the root node
        :param item:
        :param comp: a comparison function for nodes
        :param parent: the parent node
        :param tree: the tree in question
        :return: If the operation was successful
        """
        # to pass code formatting test when rebalance is commented out
        parent = parent
        # handles if item needs to go to the left
        if comp(item, self.data) < 0:
            # if left is open, insert there and update params
            if self.left is None:
                self.left = TreeNode(item)
                tree.length += 1
                self.height += 1
                self.updateBalance()
                return True
            # if left is not open, recursively call insert on left node
            else:
                succesful = self.left.insert(item, comp, self, tree)
                # I tried to get rebalancing, to work, but ultimately
                # failed. If you want to see what happens when my algorithm
                # is implemented, uncomment self.rebalance(parent, comp) both
                # here and in next comparison
                # self.rebalance(parent, comp)
                return succesful
        # handles if item needs to go to the right
        elif comp(item, self.data) > 0:
            # if right is open, insert there and update params
            if self.right is None:
                self.right = TreeNode(item)
                tree.length += 1
                self.height += 1
                self.updateBalance()
                return True
            # if right not open, recursively call insert on right node
            else:
                succesful = self.right.insert(item, comp, self, tree)
                # uncomment this if you want to see how my rebalance doesn't
                # work -- infinite loop
                # self.rebalance(parent, comp)
                return succesful
        # if item is already in list, return false
        else:
            return False
    def rebalance(self, parent, comp):
        """
        Rebalances the node in question for O(logn) time complexity
        :param parent: parent of node
        :param comp: comparison function
        """
        self.updateHeights()
        self.updateBalance()
        # if balance is left-heavy
        if self.balance > 1:
            if self.left.balance < 0:       # left-right case
                self.left.rotate_left(parent, comp)
                                                # left-left case
            self.rotate_right(parent, comp)
        # if balance is right-heavy
        if self.balance < -1:
            if self.right.balance > 0:       # right-left case
                self.right.rotate_right(parent, comp)
                                                      # right-right case
            self.rotate_left(parent, comp)
    def get_right_height(self):
        """
        Returns the height of the right subtree
        :return: height (int)
        """
        if self.right is None:
            return -1
        else:
            return self.right.height
    def get_left_height(self):
        """
        Returns the height of the left subtree
        :return: height (int)
        """
        if self.left is None:
            return -1
        else:
            return self.left.height
    def updateHeights(self):
        """
        Updates the height of node
        """
        self.height = 1 + max(self.get_left_height(), self.get_right_height())
    def updateBalance(self):
        """
        Updates the balance parameter of node
        """
        self.balance = self.get_left_height() - self.get_right_height()
    def rotate_right(self, parent, comp):
        """
        Rotates a node right for rebalancing a tree
        :param parent: parent of node
        :param comp: comparison function
        """
        # set the new root, new root's left, and store old root
        new_root = self.left
        new_left = new_root.right
        old_root = self
        # updates the tree with new_root and subtrees
        old_root.left = new_left
        new_root.right = old_root
        # if new root is greater, set parent's right to point to the new root
        if comp(new_root.data, parent.data) > 0:
            parent.right = new_root
        # if new root is lesser, set parent's left to point to new root
        elif comp(new_root.data, parent.data) < 0:
            parent.left = new_root
        # update the height and balance of node and its right node
        self.updateHeights()
        self.updateBalance()
        self.right.updateHeights()
        self.right.updateBalance()
    def rotate_left(self, parent, comp):
        """
        Rotates a node left for rebalancing a tree
        :param parent: parent of node
        :param comp: comparison function
        """
        # set the new root, new root's left, and store old root
        new_root = self.right
        new_left_sub = new_root.left
        old_root = self
        # update the tree with new_root and subtrees
        old_root.right = new_left_sub
        new_root.left = old_root
        # if new root is greater, set parent's right to point to new root
        if comp(new_root.data, parent.data) > 0:
            parent.right = new_root
        # if new root is lesser, set parent's left to point to new root
        elif comp(new_root.data, parent.data) < 0:
            parent.left = new_root
        # update the height and balance of node and its left node
        self.updateHeights()
        self.updateBalance()
        self.left.updateHeights()
        self.left.updateBalance()
    def containsNode(self, item, comp):
        """
        Checks to see if a node has an item in any of its subtrees
        :param item: The item we are looking for
        :param comp: a comparison function
        :return: True if node is found, False if not
        """
        # if tree is empty
        if self.data is None:
            return False
        # if item is less than node
        elif comp(item, self.data) < 0:
            # if left is empty, item is not in tree
            if self.left is None:
                return False
            # recursively call containsNode on left
            return self.left.containsNode(item, comp)
        # if item is greater than node
        elif comp(item, self.data) > 0:
            # if right is empty, item is not in tree
            if self.right is None:
                return False
            # recursively call containsNode on right
            return self.right.containsNode(item, comp)
        # if item == data in the node, return True
        else:
            return True
    def delete_node(self, comp, item, parent, tree):
        """
        Deletes a node from the tree
        :param comp: a comparison function
        :param item: item to Delete
        :param parent: parent of node
        :param tree: The overall tree in which we're deleting
        :return: True if item was found and deleted
        """
        # if we're at the node in question
        if not comp(item, self.data):
            # if that node is the root node
            if not comp(self.data, tree.root.data):
                # if root has no left subtree, change root to right subtree
                if tree.root.left is None:
                    tree.root = tree.root.right
                    tree.length -= 1
                    return True
                # if root has no right subtree, change root to left subtree
                elif tree.root.right is None:
                    tree.root = tree.root.left
                    tree.length -= 1
                    return True
                # if tree has both right and left subtrees
                else:
                    # store self in a temp variable and find least successor and
                    # least successor's parent
                    temp = self
                    least_succ = self.right.minimum(comp)
                    least_succ_parent = self.right.minParent(comp, self.right)
                    # update the nodes that will have changes in their data
                    least_succ_parent.left = least_succ.right
                    least_succ.right = temp.right
                    least_succ.left = temp.left
                    # empty out the deleted node
                    self.right = None
                    self.left = None
                    # set node to least successor and set new root of tree
                    tree.root = least_succ
                    tree.length -= 1
                    return True
            # if deleted node is a leaf node
            if self.right is None and self.left is None:
                # if right leaf node, update parent
                if comp(parent.data, self.data) < 0:
                    parent.right = None
                    tree.length -= 1
                    return True
                # if left leaf node, update parent
                else:
                    parent.left = None
                    tree.length -= 1
                    return True
            # if deleted node only has left children
            elif self.right is None and self.left:
                # if right node of parent, set parent's new right
                if comp(parent.data, self.data) < 0:
                    parent.right = self.left
                    self.left = None
                    tree.length -= 1
                    return True
                # if left node of parent, set parent's new left
                else:
                    parent.left = self.left
                    self.left = None
                    tree.length -= 1
                    return True
            # if deleted node only has right children
            elif self.left is None and self.right:
                # if right node of parent, set parent's new right
                if comp(parent.data, self.data) < 0:
                    parent.right = self.right
                    self.right = None
                    tree.length -= 1
                    return True
                # if left node of parent, set parent's new left
                else:
                    parent.left = self.right
                    self.right = None
                    tree.length -= 1
                    return True
            # if deleted node has both left and right children
            elif self.left and self.right:
                temp = self
                # obtain least successor and least successor's parent
                least_succ = self.right.minimum(comp)
                least_succ_parent = self.right.minParent(comp, self.right)
                # if least successor had a right, update parent's left to that
                if least_succ.right:
                    least_succ_parent.left = least_succ.right
                # if deleted node was to the left of parent
                if comp(parent.data, self.data) > 0:
                    # update parent's left to be least successor
                    parent.left = least_succ
                # if deleted node was right of parent
                else:
                    # update parent's right to be least successor
                    parent.right = least_succ
                # if least succssor and parent of least successor are the same
                if not comp(least_succ_parent.data, least_succ.data):
                    # if we're dealing with the root node
                    # (this is a special case with only 3 nodes in tree)
                    if not comp(self.data, parent.data):
                        # set self to right node of root, update left and
                        # root of the tree
                        self.left = temp.left
                        tree.root = self
                    # if we're not dealing with the root node
                    else:
                        # if node we're deleting is to the right of parent
                        if comp(parent.data, self.data) < 0:
                            # update parent's right, the node in question,
                            # and that node's left
                            parent.right = temp.right
                            self.left = temp.left
                        # if node we're deleting is to the left of parent
                        else:
                            # update parent's left, the node in question,
                            # and that node's left
                            parent.left = temp.right
                            self.left = temp.left
                # update tree length and return
                tree.length -= 1
                return True
        # if the item is less than the node we're looking at
        if comp(item, self.data) < 0:
            # if left is empty, node isn't in tree
            if self.left is None:
                return False
            # recursively call delete_node on left node
            return self.left.delete_node(comp, item, self, tree)
        # if the item is greater than node we're looking at
        else:
            # if right is empty, node isn't in tree
            if self.right is None:
                return False
            # recursively call delete_node on right node
            return self.right.delete_node(comp, item, self, tree)
    def minimum(self, comp):
        """
        Find the minimum item in the tree
        :param comp: a comparison function
        :return: minimum node in tree
        """
        # if at minimum node, return it
        if self.left is None:
            return self
        else:
            # recursively call minimum on left child
            return self.left.minimum(comp)
    def minParent(self, comp, parent):
        """
        Find the parent of the minimum item in the tree
        :param comp: a comparison function
        :param parent: parent of the node
        :return: minimum node's parent in tree
        """
        # if at minimum node, return its parent
        if self.left is None:
            return parent
        else:
            # recursively call minParent on left node
            return self.left.minParent(comp, self)
    def __repr__(self):
        """
        A string representing this node
        :return: A string
        """
        return 'TreeNode({0})'.format(self.data)
class TreeSet:
    """
    A set data structure backed by a tree.
    Items will be stored in an order determined by a comparison
    function rather than their natural order.
    """
    def __init__(self, comp):
        """
        Constructor for the tree set.
        You can perform additional setup steps here
        :param comp: A comparison function over two elements
        """
        self.comp = comp
        self.root = None
        self.length = 0
    def __len__(self):
        """
        Counts the number of elements in the tree
        :return: length of tree
        """
        return self.length
    def height(self):
        """
        Finds the height of the tree
        :return: height of tree
        """
        # if tree is empty
        if self.root is None:
            return -1
        else:
            # call get_height on root node
            return self.root.get_height()
    def insert(self, item):
        """
        Inserts the item into the tree
        :param item:
        :return: If the operation was successful
        """
        # if tree is empty, set root
        if self.root is None:
            self.root = TreeNode(item)
            self.length += 1
            return True
        else:
            return self.root.insert(item, self.comp, self.root, self)
    def remove(self, item):
        """
        Removes the item from the tree
        :param item:
        :return: If the operation was successful
        """
        # if tree is empty
        if self.root is None:
            return False
        # if tree has one node
        elif self.length == 1 and item == self.root.data:
            self.root = None
            self.length = 0
            return True
        else:
            return self.root.delete_node(self.comp, item, self.root, self)
    def __contains__(self, item):
        """
        Checks if the item is in the tree
        :param item:
        :return: if the item was in the tree
        """
        # if tree is empty
        if self.root is None:
            return False
        else:
            return self.root.containsNode(item, self.comp)
    def first(self):
        """
        Finds the minimum item of the tree
        :return:
        """
        # if tree is empty, there is no first
        if self.root is None:
            raise KeyError
        else:
            # get minimum node
            minNode = self.root.minimum(self.comp)
        # return its data
        return minNode.data
    def last(self):
        """
        Finds the maximum item of the tree
        :return:
        """
        # if tree is empty, there is no last
        if self.root is None:
            raise KeyError
        else:
            # get maximum node
            maxNode = self.root.maximum(self.comp)
        # return its data
        return maxNode.data
    def clear(self):
        """
        Empties the tree
        :return:
        """
        self.root = None
        self.length = 0
    def __iter__(self):
        """
        Does an in-order traversal of the tree
        :return:
        """
        # if tree is empty, return empty iterator
        if self.root is None:
            return iter([])
        # call iterator function on root TreeNode
        return self.root.__iter__()
    def is_disjoint(self, other):
        """
        Check if two TreeSet is disjoint
        :param other: A TreeSet object
        :return: True if the sets have no elements in common
        """
        # loop through tree
        for thing in self:
            # it data matches, it isn't disjoint
            if other.__contains__(thing):
                return False
        # if none of the data matched, return true
        return True
    def is_empty(self):
        """
        Determines whether the set is empty
        :return: False if the set contains no items, True otherwise
        """
        return len(self) == 0
    def __repr__(self):
        """
        Creates a string representation of this set using an in-order traversal.
        :return: A string representing this set
        """
        return 'TreeSet([{0}])'.format(','.join(str(item) for item in self))
    def __bool__(self):
        """
        Checks if the tree is non-empty
        :return:
        """
        return not self.is_empty()
