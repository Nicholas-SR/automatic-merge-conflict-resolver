import sys

fbase = sys.argv[1]      # The first shared ancestor
flocal = sys.argv[2]     # Your local file
fremote = sys.argv[3]    # File coming from the remote
fmerge = sys.argv[4]     # File to write the successful merge to

baseInput = open(fbase).readlines()
localInput = open(flocal).readlines()
remoteInput = open(fremote).readlines()
mergeInput = open(fmerge).readlines()


def removeNewLine(input):
    output = []
    for line in input:
        if line == "\n":
            output.append("")
        elif line[-1:] == "\n":
            size = len(line)
            output.append(line[:size - 1])
        else:
            output.append(line)
    return output


def addNewLine(input):
    output = []
    for count, line in enumerate(input):
        if line == "":
            output.append("\n")
        elif count == len(input)-1:
            output.append(line)
        else:
            output.append(line+"\n")
    return output


def findConflicts(input):
    conflicts = []
    conflictStart = -1
    conflictEnd = -1
    local = []
    remote = []
    isLocal = False
    isRemote = False
    for count, line in enumerate(input):
        if "<<<<<<<" in line:
            conflictStart = count+1
            isLocal = True
        elif "=======" in line:
            isLocal = False
            isRemote = True
        elif ">>>>>>>" in line:
            isRemote = False
            conflictEnd = count+1
            conflicts.append(
                (conflictStart, conflictEnd, local, remote))
            conflictStart = -1
            conflictEnd = -1
        elif isLocal:
            local.append(line)
        elif isRemote:
            remote.append(line)
    return conflicts


def isImportConflict(local, remote):
    isImportLocal = all(map(lambda l: l[:6] == "import" or l == "", local))
    isImportRemote = all(map(lambda l: l[:6] == "import" or l == "", remote))
    return isImportLocal and isImportRemote


def handleImportConflict(local, remote):
    importSet = set()
    importSet.update(local)
    importSet.update(remote)
    return list(importSet)


def handleConflicts(conflicts):
    resolvedConflicts = []
    for (start, end, local, remote) in conflicts:
        if isImportConflict(local, remote):
            resolvedConflict = start, end, (addWhitespace(
                start, end, handleImportConflict(local, remote)))
            resolvedConflicts.append(resolvedConflict)
    return resolvedConflicts


def insertResolvedConflicts(resolvedConflicts):
    mergeCopy = removeNewLine(mergeInput)
    for (start, end, resolvedConflict) in resolvedConflicts:
        mergeCopy[start-1:end] = resolvedConflict
    return mergeCopy


def addWhitespace(start, end, resolvedConflict):
    resolvedConflictCopy = resolvedConflict.copy()
    neededLineCount = end - start - 2
    linesToAddCount = neededLineCount - len(resolvedConflict)
    if linesToAddCount > 0:
        linesToAdd = [""]*linesToAddCount
        resolvedConflictCopy += linesToAdd
    return resolvedConflictCopy


def removeWhitespaceAfterInsert(conflicts, resolvedMerge):
    whitespaceRemoved = []
    mergedLines = set()
    for (start, end, local, remote) in conflicts:
        mergedLines.update(range(start, end+1))
    for count, line in enumerate(resolvedMerge):
        if count not in mergedLines or line != "\n":
            whitespaceRemoved.append(line)
    return whitespaceRemoved


def unParse(input):
    return ''.join(input)


def writeToMerge(input):
    open(fmerge, 'w').write(input)


removedNewLine = removeNewLine(mergeInput)
print(removedNewLine)

parsedForConflicts = findConflicts(removedNewLine)

handleConflicts = handleConflicts(parsedForConflicts)

insertResolvedConflicts = insertResolvedConflicts(handleConflicts)

addNewLine = addNewLine(insertResolvedConflicts)

removeWhitespaceAfterInsert = removeWhitespaceAfterInsert(
    parsedForConflicts, addNewLine)

unParse = unParse(removeWhitespaceAfterInsert)
print(unParse)

writeToMerge(unParse)
