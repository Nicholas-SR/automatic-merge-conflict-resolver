from handlers import *
from recognizers import *
from utils import *
from pathlib import Path
import pytest
import time
from os import path

import os

current_dir = os.path.dirname(__file__)

file_path_importConflictTest = os.path.join(current_dir, 'tests', 'importConflictTest.py')
file_path_lines10000conflictTest = os.path.join(current_dir, 'tests', 'lines10000conflictTest.py')
file_path_lines100000conflictTest = os.path.join(current_dir, 'tests', 'lines100000conflictTest.py')

file_path_commentConflictTest = os.path.join(current_dir, 'tests', 'commentConflictTest.py')

with open(file_path_importConflictTest, 'r') as f:
    importConflictTest = f.readlines()
with open(file_path_lines10000conflictTest, 'r') as f:
    lines10000conflictTest = f.readlines()
with open(file_path_lines100000conflictTest, 'r') as f:
    lines100000conflictTest = f.readlines()
with open(file_path_commentConflictTest, 'r') as f:
    commentConflictTest = f.readlines()



# run formatter on code before passing it to the parser to avoid issues with misplaced newlines


# Fails if test takes longer than 1 second
@pytest.mark.timeout(1)
def test_parser_10000_lines():
    mergeInput = lines10000conflictTest
    foundConflicts = parser(mergeInput)
    processedConflicts = differ(foundConflicts, mergeInput)
    removedNewNewLines = merger(processedConflicts)

    # Commented out unparser() as we don't want to write to the file and break future test runs
    # The unparser() function takes a trivial amount of time to run so it doesn't affect the testing
    # unparser(removedNewNewLines, fmerge)

# UNCOMMENT FOR FINAL SUBMISSION, commented for performance reasons for now.

# Testing if AMCR crashes when given a file with 100,000 lines
# def test_parser_100000_lines():
#     mergeInput = lines100000conflictTest
#     foundConflicts = parser(mergeInput)
#     processedConflicts = differ(foundConflicts, mergeInput)
#     removedNewNewLines = merger(processedConflicts)

    # Commented out unparser() as we don't want to write to the file and break future test runs
    # The unparser() function takes a trivial amount of time to run so it doesn't affect the testing
    # unparser(removedNewNewLines, fmerge)

def test_handleImportConflict():
    local = ['import types\n', 'import filecmp\n', 'import encodings\n']
    remote = ['import encodings\n', 'import filecmp\n']
    input = ['import farmhash\n', 'import libs\n', 'import redbaron\n', '# comment\n', 'import logging\n', 'import getopt\n', 'import stat\n', 'import bz2\n', 'import collections\n', 'import functools\n', 'import filelock\n', 'import math\n', 'import os\n', 'import sys\n', 'import base64\n', '<<<<<<< HEAD\n',
             'import types\n', 'import filecmp\n', 'import encodings\n', '=======\n', 'import encodings\n', 'import filecmp\n', '>>>>>>> import_conflict\n', 'import calendar\n', 'import types\n', '\n', '\n', 'def helloWorld():\n', '    main = 5 + 6\n', '    print("Hello World!")\n', '    main += 1\n', '\n', 'helloWorld()']
    conflictStart = 16
    conflictEnd = 23
    localDiff = ['import types\n']
    remoteDiff = []
    localRemoteCommon = {'import filecmp\n', 'import encodings\n'}
    expected = ['import types\n', 'import filecmp\n',
                'import encodings\n', '\n', '\n', '\n', '\n', '\n']
    assert handleImportConflict(
        local, remote, input, conflictStart, conflictEnd, localDiff, remoteDiff, localRemoteCommon) == expected












# def test_isImportConflict():
#     localDiff = ["import A"]
#     remoteDiff = ["import B"]
#     assert isImportConflict(localDiff, remoteDiff) == True


# def test_isImportConflict_fail():
#     localDiff = ["import A"]
#     remoteDiff = ["print('hello')"]
#     assert isImportConflict(localDiff, remoteDiff) == False


# def test_isFunctionSignatureConflict():
#     localDiff = "def function():"
#     remoteDiff = "def function(a):"
#     assert isFunctionSignatureConflict(localDiff, remoteDiff) == True


# def test_isFunctionSignatureConflict_fail():
#     localDiff = "def function():\n  print('hello')"
#     remoteDiff = "def function():"
#     assert isFunctionSignatureConflict(localDiff, remoteDiff) == False


# def test_isFormattingConflict():
#     localDiff = "def function(): \n"
#     remoteDiff = "def function():"
#     assert isFormattingConflict(localDiff, remoteDiff) == True


# def test_isFormattingConflict_fail():
#     localDiff = "def function():"
#     remoteDiff = "def function():\n print('hello')"
#     assert isFormattingConflict(localDiff, remoteDiff) == False


# def test_isWhitespaceConflict():
#     localDiff = "  def function(): \uFEFF"
#     remoteDiff = "def function():"
#     assert isWhitespaceConflict(localDiff, remoteDiff) == True


# def test_isWhitespaceConflict_fail():
#     localDiff = "def function(): "
#     remoteDiff = "def function():"
#     assert isWhitespaceConflict(localDiff, remoteDiff) == False


# def test_isSpacingConflict():
#     localDiff = "    def function():"
#     remoteDiff = "  def function():"
#     assert isSpacingConflict(localDiff, remoteDiff) == True


# def test_isSpacingConflict_fail():
#     localDiff = "  def function(): \n"
#     remoteDiff = "  def function():"
#     assert isSpacingConflict(localDiff, remoteDiff) == False


# def test_handleFunctionSignatureConflictOneParam():
#     localDiff = "def function():"
#     remoteDiff = "def function(a):"

#     assert handleFunctionSignatureConflict(
#         localDiff, remoteDiff, "", "", "") == "def function(a):"


# def test_handleFunctionSignatureConflictTwoParams():
#     localDiff = "def function():"
#     remoteDiff = "def function(b, a):"

#     assert handleFunctionSignatureConflict(
#         localDiff, remoteDiff, "", "", "") == "def function(b, a):"


# def test_handleFormattingConflictTwoParams():
#     localDiff = "def function(a):"
#     remoteDiff = "def function(a, b):"

#     assert handleFormattingConflict(
#         localDiff, remoteDiff, "", "", "") == "def function(a, b):"


# def test_handleFormattingConflictOneParam():
#     localDiff = "def function():"
#     remoteDiff = "def function(a):"

#     assert handleFormattingConflict(
#         localDiff, remoteDiff, "", "", "") == "def function(a):"


# def test_handleWhitespaceConflict():
#     localDiff = "def function(a): "
#     remoteDiff = "def function(a):"

#     assert handleWhitespaceConflict(
#         localDiff, remoteDiff, "", "", "") == "def function(a):"


# def test_handleWhitespaceConflictBothWhitespace():
#     localDiff = "def function(a): "
#     remoteDiff = "def function(a):  "

#     assert handleWhitespaceConflict(
#         localDiff, remoteDiff, "", "", "") == "def function(a):"


# def test_handleSpacingConflict():
#     localDiff = "  def function(a):"
#     remoteDiff = "    def function(a):"

#     assert handleSpacingConflict(
#         localDiff, remoteDiff, "", "", "") == "  def function(a):"


# def test_handleSpacingConflictLargerWhitespace():
#     localDiff = "    def function(a):"
#     remoteDiff = "        def function(a):"

#     assert handleSpacingConflict(
#         localDiff, remoteDiff, "", "", "") == "    def function(a):"
