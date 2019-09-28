#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: sort a linked list in O(1) space.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-09-09 (#169) and was classified as Medium.

  This problem was asked by Google.

  Given a linked list, sort it in O(n log n) time and constant space.

  For example, the linked list 4 -> 1 -> -3 -> 99 should become
  -3 -> 1 -> 4 -> 99.

* Solution

We use the classic Lisp representation of lists: singly linked "cons"
cells.

Since the lists don't support efficient random access, we choose to
sort them using a mergesort. (Mergesorts need only sequential scans
and were often used for disk-based sorting in the days before
solid-state drives.)

Our implementation does O(lg n) passes in which we merge successively
larger sublists. Each pass takes O(n) time. For example:

Input list:     5 -> 3 -> 4 -> 1 -> 2

Iteration 1:    [5] merge [3]
                then
                [4] merge [1]
                then
                [2] merge []

             =  3 -> 5 -> 1 -> 4 -> 2

Iteration 2:    [3 -> 5] merge [1 -> 4]
                then
                [2] merge []

             =  1 -> 3 -> 4 -> 5 -> 2

Iteration 3:    [1 -> 3 -> 4 -> 5] merge [2]

             =  1 -> 2 -> 3 -> 4 -> 5   (Final result).

This solution runs in O(1) space and O(n lg n) time.

"""

import math
import random

# We start with a classic linked-list representation based on cons
# cells, as in Lisp. In this representation, a list is either empty
# (represented by None) or given by a cell having a value and a
# tail. The tail points to another linked list representing the
# remaining values.

class Cons(object):
    """A cell in a singly linked list."""
    def __init__(self, value, tail=None):
        self.value = value
        self.tail = tail

# The sorting logic.

class Sublist(object):
    """Identifies list cells from `start` up to but not including `end`."""
    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end

def merge(sublist_a, sublist_b):
    """Merges two sorted sublists into a sorted list.

    Returns the first and last cells of the list.
    """
    # Helper function: yields the cells in sorted order.
    def merge_sequence(cell_a, cell_b):
        while cell_a is not sublist_a.end or cell_b is not sublist_b.end:
            if cell_b is sublist_b.end or (cell_a is not sublist_a.end
                                           and cell_a.value < cell_b.value):
                yield cell_a
                cell_a = cell_a.tail
            else:
                yield cell_b
                cell_b = cell_b.tail
    # String the ordered cells into a list.
    first_cell = last_cell = None
    for cell in merge_sequence(sublist_a.start, sublist_b.start):
        if first_cell is None:
            first_cell = cell
        if last_cell:
            last_cell.tail = cell
        last_cell = cell
    if last_cell:
        last_cell.tail = None
    return first_cell, last_cell

def take(llist, n):
    """Take n cells from llist. Returns a Sublist."""
    sublist = Sublist(llist)
    while n and llist:
        n -= 1
        llist = llist.tail
    sublist.end = llist
    return sublist

def llist_len(llist):
    """Returns the length of a linked list."""
    n = 0
    while llist:
        n += 1
        llist = llist.tail
    return n

def sort_linked_list(llist):
    """Sorts a linked list, rewriting links as needed."""
    # Lists less than length 2 are already sorted.
    n = llist_len(llist)
    if n < 2:
        return llist
    # Mergesort. We iterate for i = 1, 2, ..., ceil(lg(n)). For each
    # iteration, we scan the list into paired sublists of size 2^(i-1)
    # and merge the pairs, appending them to the list that will be
    # used in the next iteration.
    merge_len = 1  # Start by merging sublists of length 1.
    while merge_len < n:
        next_unmerged_cell = llist
        last_cell = llist = None
        while next_unmerged_cell:
            sublist_a = take(next_unmerged_cell, merge_len)
            sublist_b = take(sublist_a.end, merge_len)
            next_unmerged_cell = sublist_b.end
            merged_first_cell, merged_last_cell = merge(sublist_a, sublist_b)
            if llist is None:
                llist = merged_first_cell
            else:
                last_cell.tail = merged_first_cell
            last_cell = merged_last_cell
        merge_len *= 2  # The merged sublists are twice as long.
    return llist


# Tests.

# Some helper functions to convert between linked and Python lists.
# We use them only for testing.

def to_linked_list(sequence):
    """Converts a Python list into a linked list."""
    cells = map(Cons, sequence)
    cells.append(None)
    for i in range(len(cells) - 1):
        cells[i].tail = cells[i + 1]
    return cells[0]

def from_linked_list(llist):
    """Converts a linked list into a Python list."""
    sequence = []
    while llist:
        sequence.append(llist.value)
        llist = llist.tail
    return sequence

def test():
    for size in range(8):
        for _ in range(math.factorial(size)):
            sequence = [random.randint(-size, size) for _ in range(size)]
            expected = sorted(sequence)
            print '### trying {}'.format(sequence)
            actual = from_linked_list(sort_linked_list(to_linked_list(sequence)))
            assert actual == expected
