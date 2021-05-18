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
    parser.add_argument("--" + desc + "s_single", action = 'append', help="Input a list of " + desc + "s one at a time using --" + desc + "s_single arg1 --" + DESC + "s_single arg2")
    parser.add_argument("--" + desc + "s_asstring", type=str, help="input a string with " + desc + "s separated by single spaces")
    parser.add_argument("--" + desc + "s_aslines", type=str, help="input a string with " + desc + "s separated by newlines")
    parser.add_argument("--" + desc + "s_infile", type=str, help="Input a file which contains a list of " + desc + "s separated by newlines")
    parser.add_argument("--" + desc + "s_indir", action = 'append', help="Get " + desc + "s from a directory. Can also run on multiple directories by specifying -d dir1 -d dir2")
    parser.add_argument("--" + desc + "s_inpwd", action = 'store_true', help="get all " + desc + "s in current directory")

    return(parser)


def process_fileinputs(files_single, files_asstring, files_aslines, files_infile, files_indir, files_inpwd):
    """
    Take a list of input choices from argparse and turn them into a file list for infrep

    files = list of files

    files_asstring = filenames inputted as a string with spaces in between (filenames should not have spaces)
    """
    filelist = []

    if files_single is not None:
        filelist = filelist + files_single

    if files_asstring is not None:
        filelist = filelist + files_asstring.split(' ')

    if files_aslines is not None:
        filelist = filelist + files_aslines.splitlines()

    if files_infile is not None:
        if not os.path.exists(files_infile):
            raise ValueError('files_infile should be a filename. It does not exist. files_infile: ' + str(files_infile))
        with open(files_infile, 'r') as f:
            filenames = f.read().splitlines()
        filelist = filelist + filenames

    if files_indir is not None or files_inpwd is True:
        if files_indir is None:
            files_indir = []
        if files_inpwd is True:
            files_indir = files_indir + [os.path.abspath(os.getcwd())]
        for thisrootdir in files_indir:
            for root, dirs, files in os.walk(thisrootdir, topdown=False):
                for name in files:
                    filelist.append(os.path.join(root, name))

    return(filelist)


def process_fileinputs(args, desc = "file"):
    """
    Take a list of input choices from argparse and turn them into a file list for infrep

    files = list of files

    files_asstring = filenames inputted as a string with spaces in between (filenames should not have spaces)
    """
    filelist = []

    files_single = getattr(args, desc + "s_single")
    files_asstring = getattr(args, desc + "s_asstring")
    files_aslines = getattr(args, desc + "s_aslines")
    files_infile = getattr(args, desc + "s_infile")
    files_indir = getattr(args, desc + "s_indir")
    files_inpwd = getattr(args, desc + "s_inpwd")

    if files_single is not None:
        filelist = filelist + files_single

    if files_asstring is not None:
        filelist = filelist + files_asstring.split(' ')

    if files_aslines is not None:
        filelist = filelist + files_aslines.splitlines()

    if files_infile is not None:
        if not os.path.exists(files_infile):
            raise ValueError('files_infile should be a filename. It does not exist. files_infile: ' + str(files_infile))
        with open(files_infile, 'r') as f:
            filenames = f.read().splitlines()
        filelist = filelist + filenames

    if files_indir is not None or files_inpwd is True:
        if files_indir is None:
            files_indir = []
        if files_inpwd is True:
            files_indir = files_indir + [os.path.abspath(os.getcwd())]
        for thisrootdir in files_indir:
            for root, dirs, files in os.walk(thisrootdir, topdown=False):
                for name in files:
                    filelist.append(os.path.join(root, name))

    return(filelist)


def test_ap():
    """
    This function is called by the functions in test_argparse_fileinputs.py

    Should output list of 1.txt, 2.txt otherwise raises error.
    """

    parser = argparse.ArgumentParser()

    # add filelist elements
    parser = add_fileinputs(parser)

    args = parser.parse_args()

    # filelist = process_fileinputs(args.files_single, args.files_asstring, args.files_aslines, args.files_infile, args.files_indir, args.files_inpwd)
    filelist = process_fileinputs(args)

    # adjust filelist so only contains basenames - only relevant for tests with indir/inpwd
    filelist = sorted([os.path.basename(filename) for filename in filelist])
    if filelist != ['1.txt', '2.txt']:
        raise ValueError('Failed to output correct list of files. Outputted list: ' + str(filelist) + '.')


# Run:{{{1
if __name__ == "__main__":
    test_ap()


    
    
