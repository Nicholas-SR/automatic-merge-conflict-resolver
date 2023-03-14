from handlers import *
from recognizers import *
from utils import *


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
