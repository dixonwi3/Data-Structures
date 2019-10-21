######################
# Lis.py
######################
"""
Defines functions necessary to find and verify a largest increasing subsequence
given a sequence of elements. To compute the LIS, I used a method that is based
on finding the index of the last number in the sequence, then keeping track of
all of the elements that come before that in another array to then build the
resultant subsequence array for return.
"""
def verify_subseq(seq, subseq):
    """
    Iteratively verifies that the subsequence array is indeed a subsequence of
    the sequence array
    :param seq: The sequence
    :param subseq: The subsequence to verify
    :return: if subseq is a subsequence of seq
    """
    j = 0    # Indexer for subseq
    i = 0    # Indexer for seq
    # starting at the first index in subseq and seq and going until we reach the
    # last element of either,
    while j < len(subseq) and i < len(seq):
        # if the characters match at any point,
        if subseq[j] == seq[i]:
            # move to the next subsequence element
            j = j + 1
        # go to next sequence element
        i = i + 1
    # if all elements in substring matched (j = len(subseq), then return True
    return j == len(subseq)
def verify_increasing(seq):
    """
    Verifies that a sequence is indeed increasing
    :param seq: The sequence
    :return: whether the sequence is increasing
    """
    for i in range(1, len(seq)):
        if seq[i] <= seq[i-1]:
            return False
    return True
def find_lis(seq):
    """
    Finds the largest increasing subsequence in the provided sequence.
    :param seq: The sequence
    :return: A list with the largest increasing subsequence
    """
    # if seq is empty, return it
    if not seq:
        return seq
    # M[j-1] holds the index in seq of the last number in the increasing subsequence of length j
    m = [None] * len(seq)
    # Where i is an index in seq, P[i] will point to M[j], effectively being used to find the previous element in the seq to construct the resultant increasing subsequence array at the end
    p = [None] * len(seq)
    # seq has at least one element, so length of lis is >= 1
    lis_length = 1
    # 0th element's array will only contain itself
    m[0] = 0
    # Loop through seq from second element
    for i in range(1, len(seq)):
        # binary search to maximize j <= lis_length s.t.
        # seq[M[j]] < seq[i] with lower bound starting at j = 0
        low = 0
        high = lis_length
        # binary search won't check the upper bound, so do that manually
        if seq[m[high-1]] < seq[i]:
            j = high
        else:
            # actual binary search loop
            while high - low > 1:
                # find middle index in M
                mid = (high + low) // 2
                # if that element is lower than index in question, set low
                if seq[m[mid-1]] < seq[i]:
                    low = mid
                # else set high to mid
                else:
                    high = mid
            # on first run, j = 0
            j = low
        # update P list from M
        p[i] = m[j-1]
        if j == lis_length or seq[i] < seq[m[j]]:
            m[j] = i
            # if j+1 is greater than existing LIS length, replace LIS length
            # (use j+1 to compensate for list indexing)
            lis_length = max(lis_length, j+1)
    # Building the result: [seq[M[L-1]], seq[P[M[L-1]]], seq[P[P[M[L-1]]]], ...]
    result = []
    index = m[lis_length-1]
    for _ in range(lis_length):
        result.append(seq[index])
        index = p[index]
    # return result reversed for LIS
    return result[::-1]
