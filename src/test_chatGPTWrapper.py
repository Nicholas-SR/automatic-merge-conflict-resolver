from handlers import *
from recognizers import *
from utils import *
import pytest
import os

current_dir = os.path.dirname(__file__)

file_path_elseConflictTest = os.path.join(
    current_dir, 'tests', 'elseConflictTest.py')

with open(file_path_elseConflictTest, 'r') as f:
    elseConflictTest = f.readlines()

# You must login to OpenAI's ChatGPT in Playright's browser in order to run this test

# Cannot test that the output matches any given expected output because the output from OpenAI is not constant
# Thus we use the workaround of testing that certain lines are in the output
def test_handleElseConflictChatGPTWrapper():
    API_KEY = os.getenv("OPENAI_API_KEY")
    os.environ['OPENAI_API_KEY'] = ''
    mergeInput = elseConflictTest
    print("HERE",API_KEY)
    foundConflicts = parser(mergeInput)
    processedConflicts = differ(foundConflicts, mergeInput)
    print("THERE",(processedConflicts)==['* Run this program with the `install` parameter and log in to ChatGPT.\n'])
    if API_KEY:
        os.environ['OPENAI_API_KEY'] = API_KEY
    if processedConflicts == ['* Run this program with the `install` parameter and log in to ChatGPT.\n']:
        pytest.skip("ChatGPT not logged in on Playwright Browser")
    assert "    main = 5 + 6\n" in processedConflicts or "    main = 5+6\n" in processedConflicts
    assert "list = []\n" in processedConflicts
    assert "    main += 1\n" in processedConflicts or "    main = main + 1\n" in processedConflicts
    assert "    list.append(1)\n" in processedConflicts or "    list += [1]\n" in processedConflicts
test_handleElseConflictChatGPTWrapper()