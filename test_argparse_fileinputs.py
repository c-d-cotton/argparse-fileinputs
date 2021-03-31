#!/usr/bin/env python3

import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/')

import subprocess

def test_filename():
    subprocess.check_call([__projectdir__ / Path('argparse_fileinputs.py'), '-f', '1.txt', '--filename', '2.txt'])


def test_files_asstring():
    subprocess.check_call([__projectdir__ / Path('argparse_fileinputs.py'), '--files_asstring', '1.txt 2.txt'])


def test_files_aslines():
    subprocess.check_call([__projectdir__ / Path('argparse_fileinputs.py'), '--files_aslines', '1.txt\n2.txt'])


def test_files_aslines():
    subprocess.check_call([__projectdir__ / Path('argparse_fileinputs.py'), '--files_aslines', '1.txt\n2.txt'])


def test_files_infile():
    subprocess.check_call([__projectdir__ / Path('argparse_fileinputs.py'), '--files_infile', str(__projectdir__ / Path('test/filelist.txt'))])


def test_files_indir():
    subprocess.check_call([__projectdir__ / Path('argparse_fileinputs.py'), '--files_indir', str(__projectdir__ / Path('test/indir/'))])


def test_files_inpwd():
    # change to directory containing 1.txt, 2.txt
    cwd = os.getcwd()
    os.chdir(__projectdir__ / Path('test/indir/'))

    subprocess.check_call([__projectdir__ / Path('argparse_fileinputs.py'), '--files_inpwd'])

    # change back
    os.chdir(cwd)


def test_all():
    test_filename()
    test_files_asstring()
    test_files_aslines()
    test_files_infile()
    test_files_indir()
    test_files_inpwd()


# Run:{{{1
if __name__ == "__main__":
    test_all()
