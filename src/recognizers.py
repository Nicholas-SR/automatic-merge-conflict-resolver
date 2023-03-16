import redbaron
import re


def isImportConflict(local, remote, localDiff, remoteDiff):
    try:
        anyImportLocal = (any(map(lambda l: isinstance(
            redbaron.RedBaron(l)[0], redbaron.nodes.ImportNode), local)))
        anyImportRemote = (any(map(lambda l: isinstance(
            redbaron.RedBaron(l)[0], redbaron.nodes.ImportNode), remote)))
        anyImportLocalDiff = (any(map(lambda l: isinstance(
            redbaron.RedBaron(l)[0], redbaron.nodes.ImportNode), localDiff)))
        anyImportRemoteDiff = (any(map(lambda l: isinstance(
            redbaron.RedBaron(l)[0], redbaron.nodes.ImportNode), remoteDiff)))
        return anyImportLocal and anyImportRemote and (anyImportLocalDiff or anyImportRemoteDiff)
    except Exception as e:
        print("RECOGNIZER ERROR: ", e)
        return False


def isCommentConflict(local, remote, localDiff, remoteDiff):
    try:
        anyCommentLocal = (any(map(lambda l: isinstance(
            redbaron.RedBaron(l)[0], redbaron.nodes.CommentNode), local)))
        anyCommentRemote = (any(map(lambda l: isinstance(
            redbaron.RedBaron(l)[0], redbaron.nodes.CommentNode), remote)))
        anyCommentLocalDiff = (any(map(lambda l: isinstance(
            redbaron.RedBaron(l)[0], redbaron.nodes.CommentNode), localDiff)))
        anyCommentRemoteDiff = (any(map(lambda l: isinstance(
            redbaron.RedBaron(l)[0], redbaron.nodes.CommentNode), remoteDiff)))
        return anyCommentLocal and anyCommentRemote and (anyCommentLocalDiff or anyCommentRemoteDiff)
    except Exception as e:
        print("RECOGNIZER ERROR: ", e)
        return False


def isListAppendConflict(local, remote, localDiff, remoteDiff):
    print("YO")
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
        return anyListAppendLocal and anyListAppendRemote and ((anyListAppendLocalDiffPlus or anyListAppendRemoteDiffAppend) or (anyListAppendLocalDiffAppend or anyListAppendRemoteDiffPlus))
    except Exception as e:
        print("RECOGNIZER ERROR: ", e)
        return False


def isWhitespaceConflict(local, remote, localDiff, remoteDiff):
    if len(local) != len(remote):
        return False
    i = 0
    while i < len(local):
        # Strip formatting from local and remote parts
        if re.sub("[\s\n]+", "", local[i]) != re.sub("[\s\n]+", "", remote[i]):
            return False
        i += 1
    return True
