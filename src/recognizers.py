import re


def isImportConflict(local, remote, localDiff, remoteDiff):
    anyImportLocal = False
    anyImportRemote = False
    anyImportLocalDiff = False
    anyImportRemoteDiff = False
    anyNonImportConflictLocalDiff = False
    anyNonImportConflictRemoteDiff = False
    for line in local:
        if line.strip()[:6] == "import":
            anyImportLocal = True
    for line in remote:
        if line.strip()[:6] == "import":
            anyImportRemote = True
    for line in localDiff:
        if line.strip()[:6] == "import":
            anyImportLocalDiff = True
        else:
            if line not in remote:
                anyNonImportConflictLocalDiff = True
                break
    for line in remoteDiff:
        if line.strip()[:6] == "import":
            anyImportRemoteDiff = True
        else:
            if line not in local:
                anyNonImportConflictRemoteDiff = True
                break
    if localDiff == [] and remoteDiff == []:
        return anyImportLocal and anyImportRemote
    if anyNonImportConflictLocalDiff or anyNonImportConflictRemoteDiff:
        return False
    return anyImportLocal and anyImportRemote and (anyImportLocalDiff or anyImportRemoteDiff)


def isCommentConflict(local, remote, localDiff, remoteDiff):
    anyCommentLocal = False 
    anyCommentRemote = False
    anyCommentLocalDiff = False
    anyCommentRemoteDiff = False
    anyNonCommentConflictLocalDiff = False
    anyNonCommentConflictRemoteDiff = False
    for line in local:
        if line.strip()[:1] == "#":
            anyCommentLocal = True
    for line in remote:
        if line.strip()[:1] == "#":
            anyCommentRemote = True
    for line in localDiff:
        if line.strip()[:1] == "#":
            anyCommentLocalDiff = True
        else:
            if line not in remote:
                anyNonCommentConflictLocalDiff = True
                break
    for line in remoteDiff:
        if line.strip()[:1] == "#":
            anyCommentRemoteDiff = True
        else:
            if line not in remote:
                anyNonCommentConflictRemoteDiff = True
                break
    if localDiff == [] and remoteDiff == []:
        return anyCommentLocal and anyCommentRemote
    if anyNonCommentConflictLocalDiff or anyNonCommentConflictRemoteDiff:
        return False
    return anyCommentLocal and anyCommentRemote and (anyCommentLocalDiff or anyCommentRemoteDiff)


def isListAppendConflict(local, remote, localDiff, remoteDiff):
    try:
        anyListAppendLocal = (
            any(map(lambda l: "+= [" in l or ".append" in l, local)))
        anyListAppendRemote = (
            any(map(lambda l: "+= [" in l or ".append" in l, remote)))
        anyListAppendLocalDiffPlus = (
            any(map(lambda l: "+= [" in l, localDiff)))
        anyListAppendLocalDiffAppend = (
            any(map(lambda l: ".append" in l, localDiff)))
        anyListAppendRemoteDiffPlus = (
            any(map(lambda l: "+= [" in l, remoteDiff)))
        anyListAppendRemoteDiffAppend = (
            any(map(lambda l: ".append" in l, remoteDiff)))
        anyNonListAppendConflictLocalDiff = (
            any(map(lambda l: (not("+= [" in l)) and (not(".append" in l)), localDiff)))
        anyNonListAppendConflictRemoteDiff = (
            any(map(lambda l: (not("+= [" in l)) and (not(".append" in l)), remoteDiff)))
        if (anyNonListAppendConflictLocalDiff or anyNonListAppendConflictRemoteDiff):
            return False
        return anyListAppendLocal and anyListAppendRemote and ((anyListAppendLocalDiffPlus or anyListAppendRemoteDiffAppend) or (anyListAppendLocalDiffAppend or anyListAppendRemoteDiffPlus))
    except Exception as e:
        print("RECOGNIZER ERROR: ", e, local, remote, localDiff, remoteDiff)
        return False


def isWhitespaceConflict(local, remote):
    if len(local) != len(remote):
        return False
    i = 0
    while i < len(local):
        # Strip formatting from local and remote parts
        if re.sub("[\s\n]+", "", local[i]) != re.sub("[\s\n]+", "", remote[i]):
            return False
        i += 1
    return True
