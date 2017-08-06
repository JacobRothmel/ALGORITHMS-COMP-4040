# -*- coding: utf-8 -*-
"""
@author: Jacob Rothmel

This File contains File manipulation classes for use in an external sort for large files.

---------
Contains:
---------
Classes:
    -FileMutilator()
        +__init__(self, victim, chunkSize)
        +list_chunks(self)
        +commit_mutilation(self)
        +hide_remains(self)
        -_hide_corpse(self, chunkNum, chunk)
        -_chunk_file_naming_format

    -AmmoRack()
        -__init__(self, files)
        +make_war_plans(self)
        +reload(self)
        +unload(self, index)

    -FileSurgeon()
        +__init__(self, sPlan)
        +start_stitching(self, patients, targetFileName, chunkSize)
        +prep_for_surgery(self, patients, chunkSize)

    -FileSuture()
        +pick_target(self, thread)

Helper Function(s):
    -_murder_file(file)

Global(s):
    -_workingDir: The current working directory

----------
CHANGE LOG
----------
    -08/04/17 - Started. Moved all file manipulation code to this file. added in code to merge
                    chunk files back together and a filepicker for nway merging.
    -08/05/17 - Formatting fixes and documentation added.
"""
import sys
import os

import Sorts
"""
Globals
-----
"""
#current working directory
_workingDir = os.path.dirname(os.path.realpath(__file__))


"""
FileMutilator class
-----
"""
class FileMutilator():
    """
    The purpose of this class is to handle all aspects of splitting a data file into blocks
    and handling all clean up needed regarding these files after the sorting is complete.

    Attributes:
        -victim (string): the name of the data file
        -chunkSize (int): the size in bytes to be read and written
    """
    #format for chunk file naming
    _chunk_file_naming_format = 'chunk_file{0}.dat'

    #holds the names of the chunk files
    _chunkFiles = []

    #tells us if the chunks are sorted
    sortedChunks = False

    def __init__(self, victim, chunkSize):
        assert isinstance(victim, str)
        assert isinstance(chunkSize, int)

        self.victim = os.path.join(_workingDir, victim)
        self.chunkSize = chunkSize

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
        map(_murder_file, self._chunkFiles)

    def commit_mutilation(self):
        """
        This method splits the victim file into 'self.chunkSize' long chunk files
        where each chunk was quick sorted in-place before being written to a file and the name
        of that file recorded.

        args:
            -N/A

        return:
            -None:
        """
        #keep track of the current chunk being created
        chunkNum = 0
        with open(self.victim) as fileHandle:
            while True:
                #use readlines so we get a list of lines that can be sorted.
                chunk = fileHandle.readlines(self.chunkSize)

                #if the chunk is empty we are @ EOF; so break
                if not chunk:
                    break

                #sort and write chunk to chunkFiles
                self._hide_corpse(chunk, chunkNum)

                #increment for next chunk file so they are uniquely named
                chunkNum += 1

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
        chunkName = os.path.join(_workingDir, FileMutilator._chunk_file_naming_format.format(chunkNum))

        #store the file name
        self._chunkFiles.append(chunkName)

        #save some time and do the quicksort now while values already in memory
        Sorts.qsort_inplace(chunk, 0, len(chunk) - 1)

        #turn the chunk lines into a string we can write
        toWrite = ''.join(chunk)

        #write the chunk to file
        with open(chunkName, 'w') as fileHandle:
            try:
                fileHandle.write(toWrite)
            except Exception as e:
                raise RuntimeError('Failed to write chunk data to file {0}.'.format(chunkName)\
                                    + 'Error was: {0}'.format(e))



"""
AmmoRack class
-----
"""
class AmmoRack(object):
    """
    This class is for keeping track of chunk files.

    Attributes:
        -files (list of strings): list of file paths
    """
    def __init__(self, files):
        self.rounds = files

        self.spent = set()
        self.roundCount = len(files)
        self.blanks = {i: None for i in range(self.roundCount)}

    def make_war_plans(self):
        """
        The purpose of this method is is return a dictionary of the blanks.

        args:
            -N/A

        return:
            dict: the dict of the blanks
        """
        try:
            #try to build the dictionary
            warPlan = {i: self.blanks[i] for i in range(self.roundCount) if i not in self.spent}
        except Exception as e:
            raise RuntimeError('Failed to make war plans with error: {0}'.format(e))

        return warPlan

    def reload(self):
        """
        The purpose of this method is to refresh the values in AmmoRack as changes are
        being made.

        This is intended to be used in a while loop like `while obj.reload():`

        args:
            -N/A

        return:
            -bool: True if done; else False
        """
        #loop through files
        for i in range(self.roundCount):
            #check for EOF and already seen
            if self.blanks[i] is None and i not in self.spent:
                #reload a blank
                self.blanks[i] = self.rounds[i].readline()

                #if the black reload failed, record that that one is out of ammo
                if self.blanks[i] == '':
                    self.spent.add(i)

        #done with all files
        if len(self.spent) == self.roundCount:
            return False

        #still working on files
        return True

    def unload(self, index):
        """
        The purpose of this method is to provide a quick way to remove a value from
        the blanks list and replace it with null.

        args:
            index (int): the index you want to unload

        return:
            -int: the value at the index
        """
        #get value
        value = self.blanks[index]

        #set to None
        self.blanks[index] = None

        return value



"""
FileSurgeon class
-----
"""
class FileSurgeon(object):
    """
    This class provides the utility to merge a bunch of chunk files back together.

    Attributes:
        -sPlan (obj): the way we are going to merge the files back together
    """
    def __init__(self, sPlan):
        self.sugery_plan = sPlan

    def prep_for_surgery(self, patients, chunkSize):
        """
        This method prepares chunk files for reading by opening the files.

        args:
            -patients (list of strings): list of file names
            -chunkSize (int): max size of files in bytes

        return:
            -dict: the open files
        """
        waitingRoom = {}

        #open files and store pointers to them
        for i in range(len(patients)):
            waitingRoom[i] = open(patients[i], 'r', chunkSize)

        return waitingRoom

    def start_stitching(self, patients, targetFileName, chunkSize):
        """
        This method actually does the file merge.

        args:
            -patients (list of strings): the files
            -targetFileName (string): the name for the outfile
            -chunkSize (int): max size of files in bytes

        return:
            -N/A
        """
        #prepare for battle
        ammo = AmmoRack(self.prep_for_surgery(patients, chunkSize))

        #open the target file
        with open(targetFileName, 'w', chunkSize) as targetFile:
            #WAR
            while ammo.reload():
                #get target
                selectedTarget = self.sugery_plan.pick_target(ammo.make_war_plans())

                #bombs away
                targetFile.write(ammo.unload(selectedTarget))


"""
FileSuture class
-----
"""
class FileSuture(object):
    """
    This class provides provides an nway merger select

    Attributes:
        -N/A
    """
    def pick_target(self, thread):
        """
        This method picks a file from a list of files.

        args:
            -thread (list of strings): list of file names
        """
        incisionPoint = -1
        pathToCut = None

        #find the right file
        for i in range(len(thread)):
            if pathToCut is None or thread[i] < pathToCut:
                incisionPoint = i

        return incisionPoint


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
