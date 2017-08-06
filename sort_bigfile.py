# -*- coding: utf-8 -*-
"""
@author: Jacob Rothmel

This file provides the main method for running an external sort for a large file in python.

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
    +main(args)

----------
CHANGE LOG
----------
    -07/15/17 - Started
    -08/04/17 - Moved all file classes to FileMonsters.py and all sorts to
                    Sorts.py. Also improved qsort_inplace() with a wrapper function.
                    Renamed this file to sort_bigfile.py.
    -08/06/17 - Finished main
"""
import argparse
import logging
import sys
import os

from Sorts import ExternSort

"""
Logging
-------
"""
#This logger will pick up log messages from the TabUndocumentedAPI class
LOG_FILENAME = 'sort.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format='%(levelname)s - %(asctime)s - %(message)s')


"""
MAIN
-----
"""
def main(args):
    """
    This main function serves as a way to use the external sort from the command
    line.

    args:
        args (dict): incoming command line arguments

    return:
        -N/A
    """
    #set up the external sort
    externalSorter = ExternSort(args.filename, args.sizePerChunk)

    #run the external sort
    externalSorter.run_extern_sort()
    
    logging.info('{0}'.format(externalSorter.get_timeing_info()))


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
    parser.add_argument('-c', '--chunksize',
                                    dest='sizePerChunk',
                                    action='store',
                                    type=int,
                                    default=209715200,
                                    help='Size to make each chun in bytes.')


    args = parser.parse_args()
    #argparse error checking
    if args.filename[-4:] != '.dat':
        parser.error('The data file must be ".dat". The one you provided was {0}'.format(args.filename[-4:]))

    print(args)


    #pass args to main
    main(args)