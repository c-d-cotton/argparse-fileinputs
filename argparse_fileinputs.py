#!/usr/bin/env python3

import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/')

import argparse

def add_fileinputs(parser, desc = 'file'):
    """
    ap should be specified beforehand as:
    parser = argparse.ArgumentParser()
    And I'll want to add other elements to it.

    desc is how the input is described in argparse - should be in the singular
    """

    # Which files do the search and replace on:
    parser.add_argument("-f", "--" + desc, action = 'append', help="Input a list of " + desc + "s separated using -f file1 -f fil2")
    parser.add_argument("--" + desc + "s_asstring", type=str, help="input a string with " + desc + "s separated by single spaces")
    parser.add_argument("--" + desc + "s_aslines", type=str, help="input a string with " + desc + "s separated by newlines")
    parser.add_argument("--" + desc + "s_infile", type=str, help="Input a file which contains a list of " + desc + "s separated by newlines")
    parser.add_argument("-d", "--" + desc + "s_indir", action = 'append', help="Get " + desc + "s from a directory. Can also run on multiple directories by specifying -d dir1 -d dir2")
    parser.add_argument("--" + desc + "s_inpwd", action = 'store_true', help="get all " + desc + "s in current directory")

    return(parser)


def process_fileinputs(filelist, files_asstring, files_aslines, files_infile, files_indir, files_inpwd):
    """
    Take a list of input choices from argparse and turn them into a file list for infrep

    filelist = list of files

    files_asstring = filenames inputted as a string with spaces in between (filenames should not have spaces)
    """
    import os
    import subprocess
    import sys

    numfileinputs = 0
    if filelist is not None:
        numfileinputs = numfileinputs + 1
    if files_asstring is not None:
        numfileinputs = numfileinputs + 1
    if files_aslines is not None:
        numfileinputs = numfileinputs + 1
    if files_infile is not None:
        numfileinputs = numfileinputs + 1
    if files_indir is not None:
        numfileinputs = numfileinputs + 1
    if files_inpwd is True:
        numfileinputs = numfileinputs + 1
    if numfileinputs != 1:
        raise ValueError('Multiple file input methods')

    if filelist is not None:
        return(filelist)

    if files_asstring is not None:
        return(files_asstring.split(' '))

    if files_aslines is not None:
        return(files_aslines.splitlines())

    if files_infile is not None:
        if not os.path.exists(files_infile):
            raise ValueError('files_infile should be a filename. It does not exist. files_infile: ' + str(files_infile))
        with open(files_infile, 'r') as f:
            filenames = f.read().splitlines()
        return(filenames)

    if files_indir is not None or files_inpwd is True:
        if files_inpwd is True:
            files_indir = [os.path.abspath(os.getcwd())]
        filenames = []
        for thisrootdir in files_indir:
            for root, dirs, files in os.walk(thisrootdir, topdown=False):
                for name in files:
                    filenames.append(os.path.join(root, name))

        return(filenames)


def test_ap():
    """
    This function is called by the functions in test_argparse_fileinputs.py

    Should output list of 1.txt, 2.txt otherwise raises error.
    """

    parser = argparse.ArgumentParser()

    # add filelist elements
    parser = add_fileinputs(parser)

    args = parser.parse_args()

    filelist = process_fileinputs(args.file, args.files_asstring, args.files_aslines, args.files_infile, args.files_indir, args.files_inpwd)

    # adjust filelist so only contains basenames - only relevant for tests with indir/inpwd
    filelist = sorted([os.path.basename(filename) for filename in filelist])
    if filelist != ['1.txt', '2.txt']:
        raise ValueError('Failed to output correct list of files. Outputted list: ' + str(filelist) + '.')


# Run:{{{1
if __name__ == "__main__":
    test_ap()


    
    
