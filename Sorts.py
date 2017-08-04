# -*- coding: utf-8 -*-
"""
@author: Jacob Rothmel

This file contains sorting functions/classes for use in an external sort for large files.

---------
Contains:
---------
    Functions:
        +qsort_inplace(l, s, e = None)
        -_partition(l, s, e)

----------
CHANGE LOG
----------
    -08-04-17 - Started. Moved all file classes to FileMonsters.py and all sorts to
                    Sorts.py. Also improved qsort_inplace() with a wrapper function.
                    this file will now serve as a main.
"""
import sys
import os

"""
Sorting Functions
-----
"""
def qsort_inplace(l, s, e = None):
    """
    This method provides a wrapper for _qsort_inplace to allow for
    getting the end value if it is not provided and to handle error checking.

     args:
            -l (lst): the list of numbers to sort
            -s (int): position of the first element
            -e (int): position of the last element

    return:
        -N/A
    """
    #type checking
    assert isinstance(l, list), 'qsort l takes a list'
    assert isinstance(s, int), 'qsort s takes an int'

    #get the e value if not proviided.
    if not e:
        e = len(l) - 1
    else:
        assert isinstance(e, int), 'qsort e takes an int'

    def _qsort_inplace(l, s, e):
        """
        This helper function provides a simple implementation of
        an in-place quicksort for integers.

        args:
            -l (lst): the list of numbers to sort
            -s (int): position of the first element
            -e (int): position of the last element

        return:
            -N/A
        """
        #recursion check
        if s >= e:
            return

        #get the partition
        p = _partition(l, s, e)

        #qsort
        _qsort_inplace(l, s, p - 1)
        _qsort_inplace(l, p + 1, e)
        return
    #END INNER DEF

    _qsort_inplace(l, s, e)


def _partition(l, s, e):
    """
    This helper function does the partition part of quicksort.
    For use in qsort_inplace()

    args:
        -l (lst): the list of numbers to sort
        -s (int): position of the first element
        -e (int): position of the last element

    return:
        -p (int): the partition index
    """
    #make partition
    p = s
    for i in xrange(s + 1, e + 1):
        if l[i] <= l[s]:
            #increment pivot
            p += 1

            #exchange values
            l[i], l[p] = l[p], l[i]

    #exchange values
    l[p], l[s] = l[s], l[p]

    #return back partition index
    return p


