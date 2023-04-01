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

# You must provide a valid OpenAI API key in the env variables in order to run this test
# If an API key is not provided, the test will be skipped and thus pass

# Cannot test that the output matches any given expected output because the output from OpenAI is not constant
# Thus we use the workaround of testing that certain lines are in the output
def test_handleElseConflictOpenAiAPI():
    mergeInput = elseConflictTest
    foundConflicts = parser(mergeInput)
    processedConflicts = differ(foundConflicts, mergeInput)
    API_KEY = os.getenv("OPENAI_API_KEY")
    if API_KEY == None or API_KEY == "":
        pytest.skip("No OpenAI API key provided")
    assert API_KEY != None and API_KEY != ""
    assert "    main = 5 + 6\n" in processedConflicts or "    main = 5+6\n" in processedConflicts
    assert "list = []\n" in processedConflicts
    assert "    main += 1\n" in processedConflicts or "    main = main + 1\n" in processedConflicts
    assert "    list.append(1)\n" in processedConflicts or "    list += [1]\n" in processedConflicts
test_handleElseConflictOpenAiAPI()