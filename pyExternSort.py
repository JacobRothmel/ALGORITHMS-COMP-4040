# -*- coding: utf-8 -*-
"""
@author:  Jacob Rothmel

This file provides  the classes and methods needed to run an external
sort in python.

This involes splitting a large data file into smaller chunk files, quicksorting the chunk files,
and merging them back together.

The steps to do this (asuming there is a single file with all the data) are as follows:
1. Split the data file into equal sized chunk files *
2. Quick sort the chunk files *
3. Merg sort the now sorted chunk files back together.

*Done at same time.

---------
Contains:
---------
Class:
    -FileMutilator()
        +__init__(self, victim, numberOfCuts)
        +list_chunks(self)
        +commit_mutilation(self)
        +hide_remains(self)
        -_hide_corpse(self, chunkNum, chunk)

Helper Function(s):
    +qsort_inplace(l, s, e)
    -_murder_file(file)
    -_partition(l, s, e)


Global(s):
    -_chunk_file_naming_format (string): the format of the file names for chunk files
                                                           (use str.format() to replace the `{0}`)


----------
CHANGE LOG
----------
    -07-15-17 - Started
"""
import argparse
import sys
import os


"""
Globals
-----
"""
_chunk_file_naming_format = 'chunk_file{0}.dat'

#current working directory
_workingDir = os.path.dirname(os.path.realpath(__file__))


class FileMutilator():
    """
    The purpose of this class is to handle all aspects of splitting a data file into blocks
    and handling all clean up needed regarding these files after the sorting is complete.

    Attributes:
        -victim (string): the name of the data file
        -numberOfCuts (int): the numbe rof lines to put into each chunk file
    """
    #holds the names of the chunk files
    _chunkFiles = []

    #tells us if the chunks are sorted
    sortedChunks = False

    def __init__(self, victim, numberOfCuts):
        assert isinstance(victim, str)

        self.victim = os.path.join(_workingDir, victim)
        self.numLines = numberOfCuts

    def get_chunks_list(self):
        """
        This method simply returns a list of the names of chunk files

        args:
            -N/A

        return:
            -list: list of chunk file names
        """
        return self._chunkFiles

    def hide_remains(self):
        """
        This method handles cleanup. This means deleting all of the chunk files.

        args:
            -N/A

        return:
            -N/A
        """
        map(_murder_file, self.chunkFiles)

    def commit_mutilation(self):
        """
        This method splits the victim file into 'self.numLines' line long chunk files
        where each chunk was quick sorted in-place befoer being written to a file and the name
        of that file recorded.
        
        args:
            -N/A
        
        return:
            -None:
        """
        #keep track of the current chunk being created
        chunkNum = 0
        with open(self.victim) as fileHandle:
            notEOF = True

            #iterate through file until end
            while notEOF:
                lines = []
                lineCount = 0

                #read file line by line until number of lines is met and store lines
                while linecount <= self.numLines:
                    line = fileHandle.readline()

                    #the end of file will give empty line
                    if not line:
                        notEOF = False
                        break
                    else:
                        lines.append(int(line))

                    #increment line count
                    lineCount += 1
                #END while linecount <= self.numLines
                #sort and write chunk to chunkFiles
                self._hide_corpse(chunk, chunkNum)
                chunkNum += 1
            #END while notEOF
        #END with

    def _hide_corpse(self, chunk, chunkNum):
        """
        This method writes a chunk to a chunk file and records the name.

        args:
            -chunk (list): a list list of lines to put into a chunk file
            -chunkNum (int): the number to use as part of the chunk file name
        
        return:
            -N/A
        """
        #type checking
        assert isinstance(chunk, list)
        assert isinstance(chunkNum, int)
        
        #build the name
        chunkName = os.path.join(_workingDir, _chunk_file_naming_format.format(chunkNum))

        #store the file name
        self._chunkFiles.append(chunkName)
        
        #save some time and do the quicksort now while values already in memory
        qsort_inplace(chunk, 0, len(chunk))
        
        #write the chunk to file
        with open(chunkName, 'r') as fileHandle:
            try:
                fileHandle.writelines(chunk)
            except Exception as e:
                raise RuntimeError('Failed to write chunk data to file {0}.'.format(chunkName)\
                                    + 'Error was: {0}'.format(e))



"""
Helper Function(s)
-----
"""
def _murder_file(theSheep):
    """
    This helper function is meant to be used in conjunction with map() to delete chunk
    files as part of the FileMutilator's cleanup process.

    args:
        -theSheep (string): a string that is the filepath and name of the file to delete

    return:
        -N/A
    """
    try:
        os.remove(theSheep)
    except Exception as e:
        raise RuntimeError('File {0} could not be deleted becuase of Error: {1}'.format(file, e))


def qsort_inplace(l, s, e):
    """
    This helper function provides a simple implementation of
    an in-place quicksort for integers.

    args:
        -l (lst): the list of numbers to sort
        -s (int): position of the first element
        -e (int): position of the last element

    return:
        -list: the sorted list
    """
    #type checking
    assert isinstance(l, list)
    assert isinstance(s, int)
    assert isinstance(e, int)

    #recursion check
    if s >= e:
        return

    #get the partition
    p = _partition(l, s, e)

    #qsort
    qsort_inplace(l, s, p - 1)
    qsort_inplace(l, p + 1, e)
    return


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
    #type checking
    assert isinstance(l, list)
    assert isinstance(s, int)
    assert isinstance(e, int)

    #make partition
    p = s
    for i in xrange(s + 1, e + 1):
        if l[i] <= l[s]:
            p += 1
            l[i], l[p] = l[p], l[i]
    l[p], l[s] = l[s], l[p]

    #return back partition index
    return p


"""
MAIN
-----
"""
def test(lst):
    qsort_inplace(lst, 0, len(lst) - 1)
    return lst
    
def main(args):
    print('NOT READY TO WORK ON THIS PART YET, JUST A PLACE HOLDER')

    x = [35,200,97,56,103,146,87,512,96,55,33,44,12,1]

    ha = test(x)
    print(ha)
    
    print(x)
    qsort_inplace(x, 0, len(x) - 1)
    print(x)


    i = 0
    with open('data.dat', 'r') as f:
        for chunk in iter(lambda: f.readline(), ""):
            print('\n\n\n CHUNK {0}:\n{1}\nType: {2}'.format(i, chunk, type(chunk)))
            i += 1

            if i == 10:
                return

if __name__ == '__main__':
    #argparse setup
    parser = argparse.ArgumentParser(description='This program sorts data files by breaking them'\
                                                'into chunks, quick sorting the chuncks and merge'\
                                                'sorting them back together.\n The default data file'\
                                                'is named "data.dat", and the default number of lines'\
                                                'per chunk file is 1000',
                                    epilog='And that is how you sort a big file')
    parser.add_argument('-f', '--file',
                                    dest='filename',
                                    action='store',
                                    type=str,
                                    default='data.dat',
                                    help='The name of the data file. must be ".dat"')
    parser.add_argument('-l', '--lines',
                                    dest='linesPerChunk',
                                    action='store',
                                    type=int,
                                    default=1000,
                                    help='The number of lines to put into each chunk *it is -l'\
                                         'where l is lowercase "L"*')


    args = parser.parse_args()
    #argparse error checking
    if args.filename[-4:] != '.dat':
        parser.error('The data file must be ".dat". The one you provided was {0}'.format(args.filename[-4:]))

    print(args)


    #pass args to main
    main(args)