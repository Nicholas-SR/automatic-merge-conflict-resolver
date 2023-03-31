from handlers import *
from recognizers import *
from utils import *
import os


# You must login to OpenAI's ChatGPT in Playright's browser in order to run this test
# You must not have an OpenAI API key defined in the env variables in order to run this test (export  OPENAI_API_KEY="")

current_dir = os.path.dirname(__file__)

file_path_elseConflictTest = os.path.join(
    current_dir, 'tests', 'elseConflictTest.py')


with open(file_path_elseConflictTest, 'r') as f:
    elseConflictTest = f.readlines()

# Cannot test that the output matches any given expected output because the output from OpenAI is not constant
# Thus we use the workaround of testing that certain lines are in the output
def test_handleElseConflictChatGPTWrapper():
    mergeInput = elseConflictTest
    output0 = handleElseConflict(mergeInput)
    assert "    main = 5 + 6\n" in output0 or "    main = 5+6\n" in output0
    assert "list = []\n" in output0
    assert "    main += 1\n" in output0 or "    main = main + 1\n" in output0
    assert "    list.append(1)\n" in output0 or "    list += [1]\n" in output0