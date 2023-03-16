from handlers import *
from recognizers import *
from utils import *
import pytest
import os

current_dir = os.path.dirname(__file__)

file_path_importConflictTest = os.path.join(
    current_dir, 'tests', 'importConflictTest.py')
file_path_lines10000conflictTest = os.path.join(
    current_dir, 'tests', 'lines10000conflictTest.py')
file_path_lines100000conflictTest = os.path.join(
    current_dir, 'tests', 'lines100000conflictTest.py')
file_path_commentConflictTest = os.path.join(
    current_dir, 'tests', 'commentConflictTest.py')
file_path_listAppendConflict = os.path.join(
    current_dir, 'tests', 'listAppendConflict.py')
file_path_whitespaceConflictTest = os.path.join(
    current_dir, 'tests', 'whitespaceConflictTest.py')

with open(file_path_importConflictTest, 'r') as f:
    importConflictTest = f.readlines()
with open(file_path_lines10000conflictTest, 'r') as f:
    lines10000conflictTest = f.readlines()
with open(file_path_lines100000conflictTest, 'r') as f:
    lines100000conflictTest = f.readlines()
with open(file_path_commentConflictTest, 'r') as f:
    commentConflictTest = f.readlines()
with open(file_path_listAppendConflict, 'r') as f:
    listAppendConflict = f.readlines()
with open(file_path_whitespaceConflictTest, 'r') as f:
    whitespaceConflict = f.readlines()
# run formatter on code before passing it to the parser to avoid issues with misplaced newlines


# Fails if test takes longer than 1 second
@pytest.mark.timeout(1)
def test_parser_10000_lines():
    mergeInput = lines10000conflictTest
    foundConflicts = parser(mergeInput)
    processedConflicts = differ(foundConflicts, mergeInput)
    merger(processedConflicts)
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


def test_isImportConflict():
    mergeInput = importConflictTest
    foundConflicts = parser(mergeInput)
    conflict0 = foundConflicts[0]
    conflict1 = foundConflicts[1]
    assert isImportConflict(conflict0["local"], conflict0["remote"],
                            conflict0["localDiff"], conflict0["remoteDiff"]) == True
    assert isImportConflict(conflict1["local"], conflict1["remote"],
                            conflict0["localDiff"], conflict0["remoteDiff"]) == True


def test_isCommentConflict():
    mergeInput = commentConflictTest
    foundConflicts = parser(mergeInput)
    conflict0 = foundConflicts[0]
    conflict1 = foundConflicts[1]
    assert isCommentConflict(conflict0["local"], conflict0["remote"],
                             conflict0["localDiff"], conflict0["remoteDiff"]) == True
    assert isCommentConflict(conflict1["local"], conflict1["remote"],
                             conflict0["localDiff"], conflict0["remoteDiff"]) == True


def test_isListAppendConflict():
    mergeInput = listAppendConflict
    foundConflicts = parser(mergeInput)
    conflict0 = foundConflicts[0]
    conflict1 = foundConflicts[1]
    assert True == isListAppendConflict(conflict0["local"], conflict0["remote"],
                                        conflict0["localDiff"], conflict0["remoteDiff"])
    assert True == isListAppendConflict(conflict1["local"], conflict1["remote"],
                                        conflict0["localDiff"], conflict0["remoteDiff"])


def test_isWhitespaceConflictTest():
    mergeInput = whitespaceConflict
    foundConflicts = parser(mergeInput)
    conflict0 = foundConflicts[0]
    conflict1 = foundConflicts[1]
    assert True == isWhitespaceConflict(conflict0["local"], conflict0["remote"],
                                        conflict0["localDiff"], conflict0["remoteDiff"])
    assert True == isWhitespaceConflict(conflict1["local"], conflict1["remote"],
                                        conflict0["localDiff"], conflict0["remoteDiff"])


def test_handleImportConflict():
    mergeInput = importConflictTest
    foundConflicts = parser(mergeInput)
    conflict0 = foundConflicts[0]
    expected0 = ['import types as f\n', 'import filecmp\n',
                 'import encodings\n', '\n', '# test\n', '\n', '\n', '\n', '\n', '\n']
    output0 = handleImportConflict(conflict0["local"], conflict0["remote"], mergeInput, conflict0["conflictStart"],
                                   conflict0["conflictEnd"], conflict0["localDiff"], conflict0["remoteDiff"], conflict0["localRemoteCommon"])
    print(output0)
    assert output0 == expected0
    conflict1 = foundConflicts[1]
    expected1 = ['import stat\n', 'import bz2\n', 'import collections\n',
                 'import functools\n', 'import filelock\n', '\n', '\n', '\n', '\n', '\n', '\n']
    output1 = handleImportConflict(conflict1["local"], conflict1["remote"], mergeInput, conflict1["conflictStart"],
                                   conflict1["conflictEnd"], conflict1["localDiff"], conflict1["remoteDiff"], conflict1["localRemoteCommon"])
    print(output1)
    assert output1 == expected1


def test_handleCommentConflict():
    mergeInput = commentConflictTest
    foundConflicts = parser(mergeInput)
    conflict0 = foundConflicts[0]
    expected0 = ['# comment 1\n', '# comment 2\n', '\n', '\n', '\n', '\n']
    output0 = handleCommentConflict(conflict0["local"], conflict0["remote"], mergeInput, conflict0["conflictStart"],
                                    conflict0["conflictEnd"], conflict0["localDiff"], conflict0["remoteDiff"], conflict0["localRemoteCommon"])
    assert output0 == expected0
    conflict1 = foundConflicts[1]
    expected1 = ['# comment 1\n', 'variableA = 1\n',
                 '# comment 3\n', '# comment 2\n', '\n', '\n', '\n', '\n']
    output1 = handleCommentConflict(conflict1["local"], conflict1["remote"], mergeInput, conflict1["conflictStart"],
                                    conflict1["conflictEnd"], conflict1["localDiff"], conflict1["remoteDiff"], conflict1["localRemoteCommon"])
    print(output1)
    assert output1 == expected1


def test_handleListAppendConflict():
    mergeInput = listAppendConflict
    foundConflicts = parser(mergeInput)

    conflict0 = foundConflicts[0]
    expected0 = ['    lst += [item]\n', '\n', '\n', '\n', '\n']
    output0 = handleListAppendConflict(conflict0["local"], conflict0["remote"], mergeInput, conflict0["conflictStart"],
                                       conflict0["conflictEnd"], conflict0["localDiff"], conflict0["remoteDiff"], conflict0["localRemoteCommon"])
    assert output0 == expected0

    conflict1 = foundConflicts[1]
    expected1 = ['    lst.append(item)\n', '\n', '\n', '\n', '\n']
    output1 = handleListAppendConflict(conflict1["local"], conflict1["remote"], mergeInput, conflict1["conflictStart"],
                                       conflict1["conflictEnd"], conflict1["localDiff"], conflict1["remoteDiff"], conflict1["localRemoteCommon"])
    assert output1 == expected1

    conflict2 = foundConflicts[2]
    expected2 = ['    var = 2\n',
                 '    lst.append(item)\n', '    # comment\n', '\n', '\n', '\n', '\n']
    output2 = handleListAppendConflict(conflict2["local"], conflict2["remote"], mergeInput, conflict2["conflictStart"],
                                       conflict2["conflictEnd"], conflict2["localDiff"], conflict2["remoteDiff"], conflict2["localRemoteCommon"])
    assert output2 == expected2


def test_handleWhitespaceConflict():
    mergeInput = whitespaceConflict
    foundConflicts = parser(mergeInput)

    conflict0 = foundConflicts[0]
    expected0 = ['    main = 5 + 6\n',
                 '    print("Hello World!")\n', '    main += 1\n']
    output0 = handleWhitespaceConflict(conflict0["local"], conflict0["remote"], mergeInput, conflict0["conflictStart"],
                                       conflict0["conflictEnd"], conflict0["localDiff"], conflict0["remoteDiff"], conflict0["localRemoteCommon"])
    assert output0 == expected0

    conflict1 = foundConflicts[1]
    expected1 = ['    main = 5 + 6\n', '    # comment 1\n',
                 '    print("Hello World!")\n', '    main += 1\n']
    output1 = handleWhitespaceConflict(conflict1["local"], conflict1["remote"], mergeInput, conflict1["conflictStart"],
                                       conflict1["conflictEnd"], conflict1["localDiff"], conflict1["remoteDiff"], conflict1["localRemoteCommon"])
    assert output1 == expected1


def test_importConflictEndToEnd():
    mergeInput = importConflictTest
    foundConflicts = parser(mergeInput)
    processedConflicts = differ(foundConflicts, mergeInput)
    expected = ['import farmhash\n', 'import libs\n', 'import redbaron\n', '# comment\n', 'import logging\n', 'import math\n', 'import os\n', 'import sys\n', 'import base64\n', 'import types as f\n', 'import filecmp\n', 'import encodings\n', '\n', '# test\n', '\n', '\n', '\n', '\n', '\n', 'import calendar\n',
                'import types\n', 'import getopt\n', 'import stat\n', 'import bz2\n', 'import collections\n', 'import functools\n', 'import filelock\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', 'def helloWorld():\n', '    main = 5 + 6\n', '    print("Hello World!")\n', '    main += 1\n', '\n', 'helloWorld()']
    assert processedConflicts == expected


def test_commentConflictEndToEnd():
    mergeInput = commentConflictTest
    foundConflicts = parser(mergeInput)
    processedConflicts = differ(foundConflicts, mergeInput)
    expected = ['# comment 1\n', '# comment 2\n', '\n', '\n', '\n', '\n', '\n', '\n', '# comment 1\n', 'variableA = 1\n', '# comment 3\n', '# comment 2\n',
                '\n', '\n', '\n', '\n', '\n', '\n', 'def helloWorld():\n', '    main = 5 + 6\n', '    print("Hello World!")\n', '    main += 1\n', '\n', 'helloWorld()']
    assert processedConflicts == expected


def test_listAppendConflictEndToEnd():
    mergeInput = listAppendConflict
    foundConflicts = parser(mergeInput)
    processedConflicts = differ(foundConflicts, mergeInput)
    expected = ['def appendToList(lst, item):\n', '    lst += [item]\n', '\n', '\n', '\n', '\n', '\n', '\n', '    lst.append(item)\n',
                '\n', '\n', '\n', '\n', '\n', '    var = 2\n', '    lst.append(item)\n', '    # comment\n', '\n', '\n', '\n', '\n', '    return lst']
    assert processedConflicts == expected


def test_isImportConflict_fail():
    local = ["import A"]
    remote = ["var = B"]
    localDiff = ["import A"]
    remoteDiff = ["var = B"]
    assert False == isImportConflict(local, remote, localDiff, remoteDiff)
    assert False == isImportConflict(remote, local, remoteDiff, localDiff)


def test_isCommentConflict_fail():
    local = ["# comment"]
    remote = ["var = B"]
    localDiff = ["# comment"]
    remoteDiff = ["var = B"]
    assert False == isCommentConflict(local, remote, localDiff, remoteDiff)
    assert False == isCommentConflict(remote, local, remoteDiff, localDiff)