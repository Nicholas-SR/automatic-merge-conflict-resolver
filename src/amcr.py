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
