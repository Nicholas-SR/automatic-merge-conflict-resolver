import redbaron
import re


def isListAppendConflict(localDiff, remoteDiff):
    # global variables for handler functions
    global localstatus, remotestatus

    # Edge case only for single line conflicts
    if len(remoteDiff) == 1 and len(localDiff) == 1:

        # Traverse line to find 'append' and '+='
        spacelesslocal, spaceslessremote = localDiff[0].replace(
            " ", ""), remoteDiff[0].replace(" ", "")
        i = 0
        while i < len(spacelesslocal):
            if spacelesslocal[i] == spaceslessremote[i]:
                i += 1
                continue
            elif spacelesslocal[i] == '.' and spaceslessremote[i] == '+':
                if spacelesslocal[i:i+7] == '.append' and spaceslessremote[i:i+2] == '+=':
                    localstatus = 'keep'
                    remotestatus = 'discard'
                    return True
            elif spacelesslocal[i] == '+' and spaceslessremote[i] == '.':
                if spacelesslocal[i:i+2] == '+=' and spaceslessremote[i:i+7] == '.append':
                    remotestatus = 'keep'
                    localstatus = 'discard'
                    return True
            return False

    else:
        return False


def isImportAsConflict(localDiff, remoteDiff):
    try:
        isImport = (all(map(lambda l: isinstance(redbaron.RedBaron(l.strip())[0], redbaron.nodes.ImportNode), localDiff)) and all(
            map(lambda l: isinstance(redbaron.RedBaron(l.strip())[0], redbaron.nodes.ImportNode), remoteDiff)))
        isAs = (all(map(lambda l: l.split()[2] == 'as', localDiff)) and all(
            map(lambda l: l.split()[2] == 'as', remoteDiff)))
        return isImport and isAs
    except:
        return False


def isImportConflict(localDiff, remoteDiff):
    try:
        anyImportLocal = (any(map(lambda l: isinstance(redbaron.RedBaron(l)[0], redbaron.nodes.ImportNode), localDiff)))
        anyImportRemote = (any(map(lambda l: isinstance(redbaron.RedBaron(l)[0], redbaron.nodes.ImportNode), remoteDiff)))
        allImportOrNewLineOrComment = (all(map(lambda l: isinstance(redbaron.RedBaron(l)[0], redbaron.nodes.ImportNode) | isinstance(redbaron.RedBaron(l)[0], redbaron.nodes.EndlNode) | isinstance(redbaron.RedBaron(l)[0], redbaron.nodes.CommentNode), localDiff)) and all(map(lambda l: isinstance(redbaron.RedBaron(l)[0], redbaron.nodes.ImportNode) | isinstance(redbaron.RedBaron(l)[0], redbaron.nodes.EndlNode) | isinstance(redbaron.RedBaron(l)[0], redbaron.nodes.CommentNode), remoteDiff)))
        return anyImportLocal and anyImportRemote and allImportOrNewLineOrComment
    except:
        return False


def isCommentConflict(localDiff, remoteDiff):
    try:
        return (all(map(lambda l: isinstance(redbaron.RedBaron(l.strip())[0], redbaron.nodes.CommentNode), localDiff)) and all(map(lambda l: isinstance(redbaron.RedBaron(l.strip())[0], redbaron.nodes.CommentNode), remoteDiff)))
    except:
        return False


def isFunctionDefinitionNameConflict(local, remote):
    try:
        return (len(local) == 1 and local[0][0:4] == "def " and len(remote) == 1 and remote[0][0:4] == "def ")
    except:
        return False


def isFunctionCallNameConflict(localDiff, remoteDiff):
    try:
        return (all(map(lambda l: isinstance(redbaron.RedBaron(l.strip())[0][-1], redbaron.nodes.CallNode), localDiff)) and all(map(lambda l: isinstance(redbaron.RedBaron(l.strip())[0][-1], redbaron.nodes.CallNode), remoteDiff)))
    except:
        return False


def isVariableNameConflict(localDiff, remoteDiff):
    try:
        return (all(map(lambda l: isinstance(redbaron.RedBaron(l.strip())[0], redbaron.nodes.AssignmentNode) or l == "", localDiff))
                and all(map(lambda l: isinstance(redbaron.RedBaron(l.strip())[0], redbaron.nodes.AssignmentNode) or l == "", remoteDiff)))
    except:
        return False


def isFunctionSignatureConflict(localDiff, remoteDiff):
    # Extract function signatures from local and remote parts
    localSignature = re.search("(?<=def )\w+\([^\)]*\)", localDiff)
    remoteSignature = re.search("(?<=def )\w+\([^\)]*\)", remoteDiff)

    if not localSignature or not remoteSignature:
        # The merge conflict does not involve a function
        return False

    # Extract parameter lists from local and remote function signatures
    localParams = re.search("\((.*?)\)", localSignature.group()).group(1)
    remoteParams = re.search("\((.*?)\)", remoteSignature.group()).group(1)

    if localParams == remoteParams:
        # The function signature conflict does not involve new parameters
        return False

    # Check if a new parameter was added to the remote function signature
    if remoteParams.startswith(localParams):
        new_param = remoteParams[len(localParams):].split(",")[0].strip()
        return True

    return False


def isFormattingConflict(localDiff, remoteDiff):

    # Strip formatting from local and remote parts
    localStripped = re.sub("[\s\n]+", "", localDiff)
    remoteStripped = re.sub("[\s\n]+", "", remoteDiff)

    # Compare stripped local and remote parts
    return localStripped == remoteStripped


def isWhitespaceConflict(local, remote):
    # Remove leading/trailing whitespace and split lines
    localLines = [line.strip() for line in local.split("\n")]
    remoteLines = [line.strip() for line in remote.split("\n")]

    # Check if there are any lines with whitespace differences
    for i, line in enumerate(localLines):
        if line != remoteLines[i]:
            return True

    return False


def isSpacingConflict(local, remote):
    # Checks if a merge conflict is due to differences in spacing
    local_lines = local.splitlines()
    remote_lines = remote.splitlines()

    for i in range(len(local_lines)):
        local_line = local_lines[i]
        remote_line = remote_lines[i]

        local_spacing = len(local_line) - len(local_line.lstrip())
        remote_spacing = len(remote_line) - len(remote_line.lstrip())

        if local_spacing != remote_spacing:
            return True

    return False
