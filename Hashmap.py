######################
# HashMap.py
######################
"""
Defines all necessary classes and functions for the implementation of
a Hash Map data structure. Uses double hashing to resolve collisions insertions
"""
class HashMap:
    """
    A open-addressed hashmap for effectively storing key-value pairs. Resolves
    collision conflicts with double hashing.
    """
    def __init__(self, load_factor=.5):
        """
        Constructor
        :param load_factor: The maximum load factor that a hashmap can
        have before rehashing occurs
        """
        # You may change the default maximum load factor
        self.max_load_factor = load_factor
        # Other initialization code can go here
        self.size = 10
        self.items = 0
        self.hmbuckets = [None] * self.size
        self.keysset = set()
    def hash1(self, val):
        """
        Calculates the first index to look in the hashmap to insert/find a pair.
        :param val: The hash value for the key object
        :return: an index in the hashmap
        """
        return val % self.size
    def hashIndex(self, val, i):
        """
        Calculates a semi-random index in the hashmap to be checked for open
        addressing.
        :param val: The hash value for the key object
        :param i: A secondary value passed in to choose the number to be
        multiplied by the second hash function to ensure variety in the hash
        index calculated
        """
        return (self.hash1(val) + (i*(hash2(val, i)))) % self.size
    def __len__(self):
        """
        Returns how many items are in the hashmap
        :return: number of items in the hashmap
        """
        return self.items
    def buckets(self):
        """
        Gives the capacity of the hashmap
        :return: capacity of the hashmap
        """
        return self.size
    def load(self):
        """
        Calculates the load factor of the hashmap
        :return: (items in hashmap)/(capacity of hashmap)
        """
        return float(self.items)/self.size
    def __contains__(self, key):
        """
        Checks to see if the key is in the hashmap
        :param key: Key we're checking for in hashmap
        :return: boolean, whether key was found or not
        """
        return key in self.keysset
    def __getitem__(self, key):
        """
        Gets a the value associated with a key in the hashmap. If key is not in
        hashmap, a KeyError is raised
        :param key: The key we're looking for in the hashmap
        :return: The value of the key in the hashmap.
        """
        # if key isn't in map, raise error
        if key not in self:
            raise KeyError(key)
        else:
            # set i value for double hashing to 0
            i = 0
            # keep looping until item is found
            while True:
                # find index to check for key in hashmap
                index = self.hashIndex(hash(key), i)
                # if that index doesn't have the key, add 1 to 1 and loop
                if self.hmbuckets[index] is None or self.hmbuckets[index][0] != key:
                    i += 1
                # if the keys match, return value associated with key
                else:
                    return self.hmbuckets[index][1]

    def __setitem__(self, key, value):
        """
        Sets a (key, value) pair in the hashmap. If key already exists in the
        map, update the value associated with the key
        :param key: key for the pair
        :param value: value associated with key
        """
        # find initial index for insertion
        index = self.hashIndex(hash(key), 0)
        inserted = False
        # intialize i for subsequent calls to hashIndex
        i = 1
        # Until something is inserted
        while not inserted:
            # if hashmap and index is empty
            if self.hmbuckets[index] is None:
                # set the key, value pair to be at that index
                self.hmbuckets[index] = [key, value]
                self.keysset.add(key)
                # stop looping, and add 1 to # of items
                inserted = True
                self.items += 1
            # if key is already in hashmap
            elif self.hmbuckets[index][0] == key:
                # update value, stop looping
                self.hmbuckets[index][1] = value
                inserted = True
            # if there's a key at that index but not the right key
            else:
                # find the next hash index, update i
                index = self.hashIndex(hash(key), i)
                i += 1
        # rehash
        self.resizeMap()
    def resizeMap(self, shrinking=False):
        """
        Rehashes map to stay under maximum load factor and over minimum load
        factor
        :param shrinking: boolean, whether or not we're shrinking the capacity
        of the hashmap
        """
        # create new hash map
        new_map = HashMap()
        # if we need to grow or shrink
        if self.load() >= self.max_load_factor or shrinking:
            # if it's shrinking we're doing
            if shrinking:
                # new map will be half the size
                new_map.size = self.size // 2
            else:
                # if growing, new map will be double size
                new_map.size = self.size * 2
            new_map.hmbuckets = [None] * new_map.size
            # add all pairs from old map into new map
            for pair in self:
                new_map[pair[0]] = pair[1]
                new_map.keysset.add(pair[0])
            # update size and buckets to new map's size and buckets
            self.size = new_map.size
            self.hmbuckets = new_map.hmbuckets

    def __delitem__(self, key):
        """
        Deletes an item from the hashmap if that item is in there
        :param key: the key of the item we want to delete
        """
        # find initial index of key in hashmap
        index = self.hashIndex(hash(key), 0)
        # initialize i for subsequent calls to hashIndex
        i = 1
        deleted = False
        # if key exists in hashmap
        if key in self:
            # loop until we find the key
            while not deleted:
                # if there is nothing at the current index
                if self.hmbuckets[index] is None:
                    # update index and loop again
                    index = self.hashIndex(hash(key), i)
                    i += 1
                # if we find the key
                elif self.hmbuckets[index][0] == key:
                    # set that index to None, items--, stop looping
                    self.hmbuckets[index] = None
                    self.keysset.remove(key)
                    self.items -= 1
                    deleted = True
                # if the key at current index isn't the key we're looking for
                else:
                    # update index and loop again
                    index = self.hashIndex(hash(key), i)
                    i += 1
            # after done deleting, if load factor is too low,
            if self.size > 10 and self.load() <= .05:
                # rehash
                self.resizeMap(shrinking=True)
        # if key doesn't exist in hashmap
        else:
            raise KeyError(key)
    def __iter__(self):
        """
        Iterates through the hashmap, yielding (key, value) pairs
        """
        # loop through numbers 0 to capacity of hashmap
        for i in range(0, self.size):
            # yield the pair at that index if pair exists
            if self.hmbuckets[i]:
                yield self.hmbuckets[i]
    def clear(self):
        """
        Clears the hashmap of all pairs
        """
        # set all pairs in hashmap to None
        for item in self:
            item.clear()
        # reinitialize all member variables
        self.size = 10
        self.items = 0
        self.keysset = set()
    def keys(self):
        """
        Gets the set of keys within the hashmap
        :return: set of keys in hashmap
        """
        return self.keysset
    # supplied methods
    def __repr__(self):
        """
        A string representation of this map
        :return: A string representing this map
        """
        return '{{{0}}}'.format(','.join('{0}:{1}'.format(k, v) for k, v in self))
    def __bool__(self):
        """
        Checks if there are items in the map
        :return True if the map is non-empty
        """
        return not self.is_empty()

    def is_empty(self):
        """
        Checks that there are no items in the map
        :return: True if there are no bindings
        """
        return len(self) == 0

    # Helper functions can go here
def hash2(val, i):
    """
    Second hash function for double hashing. Calculates a second index based
    on i passed into function
    :param val: The hash value for the key object
    :param i: The secondary value passed in to choose the prime number for
    the modulo function. Ensures that a spot will always be found
    :return: A second value for the final HashIndex function
    """
    primes = [17, 13, 19, 11]
    return (1 + (val % primes[i % 4]))
# Required Function
def year_count(input_hashmap):
    """
    Function to count the number of students born in the given year
    :input: A HashMap of student name and its birth year
    :return: A HashMap of the year and the number of students born in that year
    """
    # initialize new hashmap
    new_map = HashMap()
    # loop through input hashmap
    for pair in input_hashmap:
        # if the year isn't already a key in the hashmap
        if pair[1] not in new_map:
            # make it a key, and have 1 be it's associated value because there
            # is now one person with that birth year
            new_map[pair[1]] = 1
        # if the year is already in the map
        else:
            # add one to that year's value
            new_map[pair[1]] += 1
    return new_map
