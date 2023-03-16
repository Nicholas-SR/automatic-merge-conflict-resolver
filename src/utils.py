from handlers import *
from recognizers import *

conflictRanges = set()


def parser(input):  # Finds conflicts in the merge file
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


def differ(conflicts, input):  # Processes the conflicts
    for conflict in conflicts:
        conflictStart = conflict["conflictStart"]
        conflictMiddle = conflict["conflictMiddle"]
        conflictEnd = conflict["conflictEnd"]
        local = conflict["local"]
        remote = conflict["remote"]
        localDiff = conflict["localDiff"]
        remoteDiff = conflict["remoteDiff"]
        localRemoteCommon = conflict["localRemoteCommon"]

        if isImportConflict(local, remote, localDiff, remoteDiff):
            input[conflictStart-1:conflictEnd] = handleImportConflict(local, remote, input, conflictStart,
                                                                      conflictEnd, localDiff, remoteDiff, localRemoteCommon)
            print("---| Import Conflict |---")

        elif isCommentConflict(local, remote, localDiff, remoteDiff):
            input[conflictStart-1:conflictEnd] = handleCommentConflict(local, remote, input, conflictStart,
                                                                       conflictEnd, localDiff, remoteDiff, localRemoteCommon)
            print("---| Comment Conflict |---")

        elif isListAppendConflict(local, remote, localDiff, remoteDiff):
            input[conflictStart-1:conflictEnd] = handleListAppendConflict(local, remote, input, conflictStart,
                                                                          conflictEnd, localDiff, remoteDiff, localRemoteCommon)
            print("---| List Append Conflict |---")

        elif isWhitespaceConflict(local, remote):
            input[conflictStart-1:conflictEnd] = handleWhitespaceConflict(local, remote, input, conflictStart,
                                                                          conflictEnd, localDiff, remoteDiff, localRemoteCommon)
            print("---| Whitespace Conflict |---")

        else:
            print("isElseConflict")
            input[conflictStart-1:conflictEnd] = handleElseConflict(
                local, remote, input, conflictStart, conflictEnd, localDiff, remoteDiff, localRemoteCommon)

    return input


def merger(input):  # Removes the new new lines
    for count, line in enumerate(input):
        if line == "\n" and count+1 in conflictRanges:
            input[count] = ""
    return ''.join(input)


def unparser(input, fmerge):  # Converts the tokenized form of the merged code back into non-tokenized string version and writes it to the merge file
    joined = ''.join(input)
    open(fmerge, 'w').write(joined)
    return joined
