"""Defines the Person object, and all necessary functions for alphabetizing lists of Person objects
"""
class Person:
    """Object Person"""
    def __init__(self, first, last, email):
        self.first = first
        self.last = last
        self.email = email
    def __str__(self):
        return '{0} {1} <{2}>'.format(self.first, self.last, self.email)
    def __repr__(self):
        return '({0}, {1}, {2})'.format(self.first, self.last, self.email)
    def __eq__(self, other):
        return self.first == other.first and self.last == other.last and self.email == other.email
def order_first_name(a, b):
    """
    Orders two people by their first names
    :param a: a Person
    :param b: a Person
    :return: True if a comes before b alphabetically and False otherwise
    """
    # if first names are equal
    if a.first == b.first:
        # compare last names alphanumerically
        return a.last < b.last
    # returns true if first name of first person is alphanumerically less than
    # first name of second person
    return a.first < b.first
def order_last_name(a, b):
    """
    Orders two people by their last names
    :param a: a Person
    :param b: a Person
    :return: True if a comes before b alphabetically and False otherwise
    """
    # if the last names are equal
    if a.last == b.last:
        # compare first names
        return a.first < b.first
    # returns true if last name of first person is alphanumerically less than
    # last name of second person
    return a.last < b.last
def is_alphabetized(roster, ordering):
    """
    Checks whether the roster of names is alphabetized in the given order
    :param roster: a list of people
    :param ordering: a function comparing two elements
    :return: True if the roster is alphabetized and False otherwise
    """
    # loop through roster
    for i in range(len(roster) - 1):
        # if two sequential elements in the array are the same
        if roster[i] == roster[i + 1]:
            # continue looping
            continue
        # if two sequential elements are not in order,
        if not ordering(roster[i], roster[i + 1]):
            # the list is not alphabetized, so return False
            return False
    # if the code gets here, the list is alphabetized: return True
    return True
def merge(l, r, ordering):
    """
    Merges two arrays with the correct ordering passed to the function
    :param l: the left side of the previous larger list
    :param r: the right side of the previous larger list
    :param ordering: a function comparing two elements
    :return: a sorted version of roster (temp)
    :return: the number of comparisons made
    """
    # initialize
    i, j, comparisons = 0, 0, 0
    # initialize upper bounds for left and right lists
    n, m = len(l), len(r)
    # set empty temp array to return
    temp = []
    # loop through left and right lists
    while i < n and j < m:
        # if the person from left is less than that of the right based
        # on ordering function called
        if  ordering(l[i], r[j]):
            # append that person to temp and move to next element in left
            temp.append(l[i])
            i += 1
        # if the person in the right list is less than or equal to the left,
        else:
        # append that person to temp and move to next element in right
            temp.append(r[j])
            j += 1
        # add one to comparisons before next loop
        comparisons += 1
    # if all elements in left list were added to temp before right
    while j < len(r):
        # add the rest of right list to temp
        temp.append(r[j])
        j += 1  # increment j
    # if all elements of right list were added to temp before left
    while i < len(l):
        # add the rest of the left list
        temp.append(l[i])
        i += 1  # increment i
    # return sorted temp list and total comparisons
    return (temp, comparisons)
def alphabetize(roster, ordering):
    """
    Alphabetizes the roster according to the given ordering
    :param roster: a list of people
    :param ordering: a function comparing two elements
    :return: a sorted version of roster
    :return: the number of comparisons made
    """
    # if the roster is empty or has only one person
    if len(roster) < 2:
        # return the roster and 0 comparisons
        return (list(roster), 0)
    comparisons = 0
    # partition right half of the roster
    r = roster[(len(roster) // 2):]
    # partition left half of the roster
    l = roster[:(len(roster) // 2)]
    # recursively alphabetize on right list
    r, comparisons1 = alphabetize(r, ordering)
    # recursively alphabetize on left list
    l, comparisons2 = alphabetize(l, ordering)
    # merge the two sorted sublists
    roster, comparisons3 = merge(r, l, ordering)
    # add up the comparisons from right and left lists
    comparisons = comparisons1 + comparisons2 + comparisons3
    # return sorted list and number of comparisons
    return (list(roster), comparisons)
    
