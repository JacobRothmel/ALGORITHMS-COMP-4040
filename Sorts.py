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

    Class:
        -ExternSort()
            +__init__(self, chunkSize, victim)
            +run_extern_sort(self)
            +get_timeing_info(self
            -_setup_tools(self)
            -_set_chunkCount(self)
            -_set_needleSize(self)

----------
CHANGE LOG
----------
    -08/04/17 - Started. Moved all file classes to FileMonsters.py and all sorts to
                    Sorts.py. Also improved qsort_inplace() with a wrapper function.
                 this file will now serve as a main.
    -08/05/17 - Finished external sort, and added more documentation
"""
import time
import sys
import os

import FileMonsters

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



"""
ExternSort class
-----
"""
class ExternSort(object):
    """
    The purpose of this class is to provide a simple way to
    run an external sort on on a large data file.

    Attributes:
        -chunkSize (int): The size of chunk files in bytes
        -chunkCount (int): The number of chunk files that will be needed
        -needleSize (int): The buffer size in bytes
        -victim (path): The file to sort
        -victimSize (int): Size of the victim file in bytes
        -startTime (time): The time the object was created
        -endTime (time): The time the sort finished
    """
    def __init__(self, victim, chunkSize):
        self.chunkSize = chunkSize
        self.victim = victim
        self.victimSize = None
        self.chunkCount = None
        self.targetFile = self.victim + '.sorted.out'
        self.startTime = time.time()
        self.endTime = None

    def run_extern_sort(self):
        """
        This function runs the external sort by using the FileMutilator
        class to split up target data file into sorted chunk files.

        It then uses the FileSurgeon class to merge the sorted chunk files
        into a sorted version of the original file.

        args:
            -N/A

        return:
            -N/A
        """
        #get start time for logging.
        #get how many chunk files we need and the text buffer size for writing
        self._setup_tools()

        #set up the file splitter
        mutilator = FileMonsters.FileMutilator(self.victim, self.chunkSize)
        
        print('splitting')
        #split and quicksort chunk files
        mutilator.commit_mutilation()

        #prepare medic to merge chunk files
        medic = FileMonsters.FileSurgeon(FileMonsters.FileSuture())

        #get the chunk files to be merged
        patients = mutilator.get_chunks_list()
        
        print('starting to merge back')
        #merge the chunk files
        medic.start_stitching(patients, self.targetFile, self.needleSize)

        #delete all the used chunk files
        mutilator.hide_remains()

        #set endTime for logging later
        self.endTime = time.time()

    def _setup_tools(self):
        """
        This method calls the two private methods _set_chunkCount(self) and
        _set_needleSize(self) to pass to the methods needed.

        args:
            -N/A

        return:
            -N/A
        """
        #get the number of chunks files
        self._set_chunkCount()

        #get the size of buffers
        self._set_needleSize()

    def _set_chunkCount(self):
        """
        This method calculates the number of chunk files that will be needed
        and stores the value.

        args:
            -N/A

        return:
            -N/A
        """
        self.victimSize = os.stat(self.victim).st_size
        self.chunkCount = (self.victimSize / self.chunkSize) + 1

    def _set_needleSize(self):
        """
        This method calculates the size to use for text buffers.

        args:
            -N/A

        return:
            -N/A
        """
        self.needleSize = self.chunkSize / (self.chunkCount + 1)

    def get_timeing_info(self):
        """
        The purpose of this method is to calculate how long
        the external sort took to run.

        args:
            -N/A

        return:
            -string: time report
        """
        #calculate the total number of seconds
        totalSeconds = self.endTime - self.startTime

        #calculate minutes and seconds
        m, s = divmod(totalSeconds, 60)

        #calculate hours and minutes
        h, m = divmod(m, 60)

        return 'Running External Sort on '\
                '{0}, size: {1}, took: {2}H:{3}M:{4}S'.format(self.victim,
                                                            self.victimSize,
                                                            h, m, s)