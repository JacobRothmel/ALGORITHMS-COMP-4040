# -*- coding: utf-8 -*-
"""
@author: Jacob Rothmel

This script provides methods to generate numeric data.

Numeric data can be generated as:
- random unique data

- random non-unique data with possible repetitions

- sorted data unique

- sorted data with possible repetitions

- reverse sorted data unique

- reverse sorted data with possible repetitions

The data can be sent to a file outputed by the script for use with command line.

Contains
-----------

----------------
CHANGE LOG
----------------
    -06/29/17 - started
"""
import logging
import argparse
import array
import random
import time

def main(args):
    start_time = time.time()
    
    #create unique data
    if args.do_unique:
        #sequence becuae it is an already sorted value
        a = array.array('I', xrange(args.numCount))
        
        #create sorted data
        if args.do_sort:
            #create reversed sorted data
            if args.do_reverse:
                with open(args.outFileName, 'w') as file:
                    for i in list(reversed(a)):
                        file.write(str(i).zfill(8) + '\n')
            #create ascending sorted data
            else:
                with open(args.outFileName, 'w') as file:
                    for i in a:
                        file.write(str(i).zfill(8) + '\n')
        #create random unique order data
        else:
            random.shuffle(a)
            with open(args.outFileName, 'w') as file:
                    for i in a:
                        file.write(str(i).zfill(8) + '\n')
    
    #create random data
    else:
        a = []
        current = 0
        while current <= args.numCount:
                #generate a random number
                rand = random.randint(1, 99999999)
                a.append(rand)
                current += 1
        
        if args.do_sort:
            a.sort()
            if args.do_reverse:
                with open(args.outFileName, 'w') as file:
                    for i in list(reversed(a)):
                        file.write(str(i).zfill(8) + '\n')
            else:
                with open(args.outFileName, 'w') as file:
                    for i in a:
                        file.write(str(i).zfill(8) + '\n')
        
        else:
            with open(args.outFileName, 'w') as file:
                    for i in a:
                        file.write(str(i).zfill(8) + '\n')
    
    print("--- %s seconds ---" % (time.time() - start_time))
    print(args)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This tool generates large lists of numeric data')
    parser.add_argument('-u', '--Unique', dest='do_unique', action='store_true', help='Makes the data and unique (no repetitions).')
    parser.add_argument('-s', '--Sorted', dest='do_sort', action='store_true', help='Makes the sorted.')
    parser.add_argument('-r', '--Reversed', dest='do_reverse', action='store_true', help='Reverse data if --Sorted was used')
    parser.add_argument('-p', '--print', dest='do_print', action='store_true', help='Print the data to stdout instead of to a file.')
    parser.add_argument('-z', '--datalength', dest='numCount', action='store', type=int, help='Number of numbers to generate')
    parser.add_argument('-o', '--out', dest='outFileName', action='store', type=str, help='The name of the output file')
    args = parser.parse_args()
    
    if args.do_reverse and not args.do_sort:
        parser.error('You can not reverse the data if it is not sorted. Use -r and -s together.')
    
    if not args.numCount:
        parser.error('You must tell us how many numbers to generate. use -z/--datalength and a number')
        
    if not args.outFileName:
        parser.error('You must supply an outfile name, use -o/--out')
        
    main(args)
    