import sys
import re
import redbaron
from chatgpt_wrapper import ChatGPT


fbase = sys.argv[1]      # The first shared ancestor
flocal = sys.argv[2]     # Your local file
fremote = sys.argv[3]    # File coming from the remote
fmerge = sys.argv[4]     # File to write the successful merge to

baseInput = open(fbase).readlines()
localInput = open(flocal).readlines()
remoteInput = open(fremote).readlines()
mergeInput = open(fmerge).readlines()

conflictRanges = set()


def findConflicts(input):
    conflicts = []
    conflictStart = -1
    conflictEnd = -1
    conflictMiddle = -1
    local = []
    remote = []
    isLocal = False
    isRemote = False
    for count, line in enumerate(input):
        if "<<<<<<<" in line:
            conflictStart = count+1
            isLocal = True
        elif "=======" in line:
            conflictMiddle = count+1
            isLocal = False
            isRemote = True
        elif ">>>>>>>" in line:
            isRemote = False
            conflictEnd = count+1
            localDiff = []
            remoteDiff = []
            localRemoteCommon = set()

            for line in local:
                if line in remote:
                    localRemoteCommon.add(line)
                else:
                    localDiff.append(line)

            for line in remote:
                if line in local:
                    localRemoteCommon.add(line)
                else:
                    remoteDiff.append(line)

            conflictRanges.update(list((range(conflictStart, conflictEnd+1))))
            for count, line in enumerate(input):
                if line == "\n" and count in conflictRanges:
                    conflictRanges.remove(count)
            conflicts.append(
                ({"conflictStart": conflictStart, "conflictMiddle": conflictMiddle, "conflictEnd": conflictEnd, "local": local, "remote": remote, "localDiff": localDiff, "remoteDiff": remoteDiff, "localRemoteCommon": localRemoteCommon}))
            conflictStart = -1
            conflictMiddle = -1
            conflictEnd = -1
            local = []
            remote = []
        elif isLocal:
            local.append(line)
        elif isRemote:
            remote.append(line)
    return conflicts


def processConflicts(conflicts, input):
    for conflict in conflicts:
        conflictStart = conflict["conflictStart"]
        conflictMiddle = conflict["conflictMiddle"]
        conflictEnd = conflict["conflictEnd"]
        local = conflict["local"]
        remote = conflict["remote"]
        localDiff = conflict["localDiff"]
        remoteDiff = conflict["remoteDiff"]
        localRemoteCommon = conflict["localRemoteCommon"]

        if isImportConflict(localDiff, remoteDiff):
            handleImportConflict(local, remote, input, conflictStart,
                                 conflictEnd, localDiff, remoteDiff, localRemoteCommon)

        elif isFunctionDefinitionNameConflict(localDiff, remoteDiff):
            print("isFunctionDefinitionNameConflict")
            handleFunctionDefinitionNameConflict(
                local, remote, input, conflictStart, conflictEnd)
        elif isFunctionSignatureConflict(localDiff, remoteDiff):
            print("isFunctionSignatureConflict")
            handleFunctionSignatureConflict()
        elif isFormattingConflict(localDiff, remoteDiff, input, conflictStart, conflictEnd):
            print("isFormattingConflict")
            handleFormattingConflict()
        elif isWhitespaceConflict(localDiff, remoteDiff, input, conflictStart, conflictEnd):
            print("isWhitespaceConflict")
            handleWhitespaceConflict(localDiff, remoteDiff, input, conflictStart, conflictEnd)
        elif isSpacingConflict(localDiff, remoteDiff):
            print("isSpacingConflict")
            handleSpacingConflict(localDiff, remoteDiff, input, conflictStart, conflictEnd)
        else:
            print("isElseConflict")
            handleElseConflict(
                local, remote, input, conflictStart, conflictEnd, localDiff, remoteDiff, localRemoteCommon)

    return input


def isImportConflict(localDiff, remoteDiff):
    try:
        return (all(map(lambda l: isinstance(redbaron.RedBaron(l.strip())[0], redbaron.nodes.ImportNode), localDiff)) and all(map(lambda l: isinstance(redbaron.RedBaron(l.strip())[0], redbaron.nodes.ImportNode), remoteDiff)))
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


def handleImportConflict(local, remote, input, conflictStart, conflictEnd, localDiff, remoteDiff, localRemoteCommon):
    localAndRemote = local + remote
    importList = []
    for line in localAndRemote:
        if line[:6] == "import" and line not in importList:
            importList.append(line)
        if line[:6] != "import" and line not in importList and line in localRemoteCommon:
            importList.append(line)
            localRemoteCommon.remove(line)
    while len(importList) < conflictEnd - conflictStart + 1:
        importList.append("\n")
    input[conflictStart-1:conflictEnd] = importList


def handleFunctionDefinitionNameConflict(local, remote, input, conflictStart, conflictEnd):
    localSplit = re.split(', |\(|\)|\ ', local[0])
    remoteSplit = re.split(', |\(|\)|\ ', remote[0])
    if localSplit[1] != remoteSplit[1] and localSplit[2:] == remoteSplit[2:]:
        lst = [local[0].replace(localSplit[1], remoteSplit[1])]
        while len(lst) < conflictEnd - conflictStart + 1:
            lst.append("\n")
        # rename function definition
        input[conflictStart -
              1:conflictEnd] = lst


def handleFunctionSignatureConflict(local, remote, input, conflictStart, conflictEnd):
    # Extract function signatures from local and remote parts
    localSignature = re.search("(?<=def )\w+\([^\)]*\)", local)
    remoteSignature = re.search("(?<=def )\w+\([^\)]*\)", remote)

    # Extract parameter lists from local and remote function signatures
    localParams = re.search("\((.*?)\)", localSignature.group()).group(1)
    remoteParams = re.search("\((.*?)\)", remoteSignature.group()).group(1)

    # Get the new parameter added in the remote function signature
    newParam = remoteParams[len(localParams):].split(",")[0].strip()

    # Replace the local function signature with the remote one
    newSignature = remoteSignature.group()

    # Replace the local function call with the new signature
    newLocalPart = re.sub(localSignature.group(), newSignature, local)

    # Add the new parameter to the function call in the remote part
    newRemotePart = re.sub(localSignature.group(), newSignature, remote)
    newRemotePart = newRemotePart.replace("(", f"({newParam}, ")

    # Merge the local and remote parts
    mergedPart = newLocalPart + newRemotePart[len(remote):]

    input[conflictStart-1:conflictEnd] = mergedPart


def handleFormattingConflict(local, remote, input, conflictStart, conflictEnd):
    # Split the function signature lines into function name and parameter lists
    localParts = local.strip().split("(")
    remoteParts = remote.strip().split("(")

    # Combine the function name with the union of parameter lists
    parameters = set(localParts[1].split(",") + remoteParts[1].split(","))
    combinedPart = localParts[0] + "(" + ",".join(sorted(parameters)) + ")"

    input[conflictStart-1:conflictEnd] = combinedPart


def handleWhitespaceConflict(local, remote, input, conflictStart, conflictEnd):
    # Remove leading/trailing whitespace and split lines
    localLines = [line.strip() for line in local.split("\n")]
    remoteLines = [line.strip() for line in remote.split("\n")]

    # Use the remote version of any lines with whitespace differences
    mergedLines = [remoteLines[i] if line != remoteLines[i] else line for i, line in enumerate(localLines)]

    # Join the merged lines back together and return the result
    input[conflictStart-1:conflictEnd] = "\n".join(mergedLines)


def handleSpacingConflict(local, remote, input, conflictStart, conflictEnd):
    # Split the content into lines
    localLines = local.splitlines()
    remoteLines = remote.splitlines()

    # Create a list to hold the resolved lines
    resolvedLines = []

    # Iterate over the lines and use the code with less spaces as the standard for spacing
    for localLine, remoteLine in zip(localLines, remoteLines):
        # Get the number of spaces for each line
        localSpaces = len(localLine) - len(localLine.lstrip())
        remoteSpaces = len(remoteLine) - len(remoteLine.lstrip())

        # Use the code with less spaces as the standard for spacing
        if localSpaces <= remoteSpaces:
            resolvedLines.append(localLine)
        else:
            resolvedLines.append(remoteLine)

    input[conflictStart-1:conflictEnd] = "\n".join(resolvedLines)


def handleElseConflict(local, remote, input, conflictStart, conflictEnd, localDiff, remoteDiff, localRemoteCommon):
    prompt = "resolve the merge conflict in this code and output only the code in a code block:\n" + \
        ''.join(input)
    bot = ChatGPT()
    response = bot.ask(prompt)
    if response:
        input.clear()
        input.extend(response.splitlines(keepends=True)[1:-1])


def removeNewNewLines(input):
    for count, line in enumerate(input):
        if line == "\n" and count+1 in conflictRanges:
            input[count] = ""
    return input


def writeToMerge(input):
    open(fmerge, 'w').write(input)


foundConflicts = findConflicts(mergeInput)

processedConflicts = processConflicts(foundConflicts, mergeInput)

removedNewNewLines = removeNewNewLines(processedConflicts)

joined = ''.join(removedNewNewLines)

writeToMerge(joined)

print(joined)
print("----------------------")
