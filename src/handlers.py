from chatgpt_wrapper import ChatGPT
from recognizers import *
import re


def handleImportConflict(local, remote, input, conflictStart, conflictEnd, localDiff, remoteDiff, localRemoteCommon):
    localAndRemote = local + remote
    importList = []
    for line in localAndRemote:
        if line not in importList:
            importList.append(line)
    while len(importList) < conflictEnd - conflictStart + 1:
        importList.append("\n")
    return importList


def handleCommentConflict(local, remote, input, conflictStart, conflictEnd, localDiff, remoteDiff, localRemoteCommon):
    localAndRemote = local + remote
    commentList = []
    for line in localAndRemote:
        if line not in commentList:
            commentList.append(line)
    while len(commentList) < conflictEnd - conflictStart + 1:
        commentList.append("\n")
    return commentList



def handleListAppendConflict(local, remote, input, conflictStart, conflictEnd, localDiff, remoteDiff, localRemoteCommon):
    # Prioritizes remote changes over local changes
    localAndRemote = remote + local
    lst = []
    listNames = set()
    for line in localAndRemote:
        if (".append" not in line) and ("+= [" not in line) and line not in lst:
            lst.append(line)
        elif (".append" in line) and (line[0:line.index(".append")] not in listNames) and line not in lst:
            lst.append(line)
            listNames.add(line[0:line.index(".append")])
        elif ("+= [" in line) and (line[0:line.index("+")-1] not in listNames) and line not in lst:
            lst.append(line)
            listNames.add(line[0:line.index("+")-1])
    while len(lst) < conflictEnd - conflictStart + 1:
        lst.append("\n")
    return lst

# def handleFunctionDefinitionNameConflict(local, remote, input, conflictStart, conflictEnd):
#     localSplit = re.split(', |\(|\)|\ ', local[0])
#     remoteSplit = re.split(', |\(|\)|\ ', remote[0])
#     if localSplit[1] != remoteSplit[1] and localSplit[2:] == remoteSplit[2:]:
#         lst = [local[0].replace(localSplit[1], remoteSplit[1])]
#         while len(lst) < conflictEnd - conflictStart + 1:
#             lst.append("\n")
#         # rename function definition
#         return lst


# def handleFunctionSignatureConflict(local, remote, input, conflictStart, conflictEnd):
#     # Extract function signatures from local and remote parts
#     localSignature = re.search("(?<=def )\w+\([^\)]*\)", local)
#     remoteSignature = re.search("(?<=def )\w+\([^\)]*\)", remote)

#     # Extract parameter lists from local and remote function signatures
#     localParams = re.search("\((.*?)\)", localSignature.group()).group(1)
#     remoteParams = re.search("\((.*?)\)", remoteSignature.group()).group(1)

#     # Get the new parameter added in the remote function signature
#     newParam = remoteParams[len(localParams):].split(",")[0].strip()

#     # Replace the local function signature with the remote one
#     newSignature = remoteSignature.group()

#     # Replace the local function call with the new signature
#     newLocalPart = re.sub(localSignature.group(), newSignature, local)

#     # Merge the local and remote parts
#     mergedPart = newLocalPart

#     return mergedPart[0:-3] + mergedPart[-1]


# def handleFormattingConflict(local, remote, input, conflictStart, conflictEnd):
#     # Split the function signature lines into function name and parameter lists
#     localParts = local.strip().replace(")", "(").split("(")
#     remoteParts = remote.strip().replace(")", "(").split("(")

#     # Combine the function name with the union of parameter lists
#     parameters = set(localParts[1].split(",") + remoteParts[1].split(","))
#     if localParts[1] == '' or remoteParts[1] == '':
#         parameters.remove('')
#     return localParts[0] + "(" + ",".join(sorted(parameters, reverse=True)) + ")" + ":"


# def handleWhitespaceConflict(local, remote, input, conflictStart, conflictEnd):
#     # Remove leading/trailing whitespace and split lines
#     localLines = [line.strip() for line in local.split("\n")]
#     remoteLines = [line.strip() for line in remote.split("\n")]

#     # Use the remote version of any lines with whitespace differences
#     mergedLines = [remoteLines[i] if line != remoteLines[i]
#                    else line for i, line in enumerate(localLines)]

#     # Join the merged lines back together and return the result
#     return "\n".join(mergedLines)


# def handleSpacingConflict(local, remote, input, conflictStart, conflictEnd):
#     # Split the content into lines
#     localLines = local.splitlines()
#     remoteLines = remote.splitlines()

#     # Create a list to hold the resolved lines
#     resolvedLines = []

#     # Iterate over the lines and use the code with less spaces as the standard for spacing
#     for localLine, remoteLine in zip(localLines, remoteLines):
#         # Get the number of spaces for each line
#         localSpaces = len(localLine) - len(localLine.lstrip())
#         remoteSpaces = len(remoteLine) - len(remoteLine.lstrip())

#         # Use the code with less spaces as the standard for spacing
#         if localSpaces <= remoteSpaces:
#             resolvedLines.append(localLine)
#         else:
#             resolvedLines.append(remoteLine)

#     return "\n".join(resolvedLines)


def handleElseConflict(local, remote, input, conflictStart, conflictEnd, localDiff, remoteDiff, localRemoteCommon):
    prompt = "resolve the merge conflict in this code and output only the code in a code block:\n" + \
        ''.join(input)
    bot = ChatGPT()
    response = bot.ask(prompt)
    if response:
        return response.splitlines(keepends=True)[1:-1]
