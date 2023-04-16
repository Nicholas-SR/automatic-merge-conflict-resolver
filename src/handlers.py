from chatgpt_wrapper import ChatGPT
from recognizers import *
import black
import openai
import os


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


def handleWhitespaceConflict(local, remote, input, conflictStart, conflictEnd, localDiff, remoteDiff, localRemoteCommon):
    formattedOutputRemote = []
    for line in remote:
        stripped_line = line.strip()
        idx = line.index(stripped_line)
        formattedOutputRemote.append(
            line[0:idx] + black.format_str(line, mode=black.Mode()))
    return formattedOutputRemote


def handleElseConflict(input):
    prompt = "resolve the merge conflict in this code and output only the code in a code block. resolve the merge conflict in this code and output only the code in a code block. do not modify the formatting or spacing of the code, do not add or remove new line characters:\n" + \
        ''.join(input)
    API_KEY = os.getenv("OPENAI_API_KEY")
    if API_KEY == None or API_KEY == "":
        print("Using unofficial ChatGPT Wrapper, specify an OpenAI API Key to use the official API")
        bot = ChatGPT()
        response = bot.ask(prompt)
        if response:
            return response[1].splitlines(keepends=True)[1:-1]
        else:
            raise Exception("Unofficial ChatGPT Wrapper is not setup correctly or it has been deprecated.")
    else:
        openai.api_key = API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        if response:
            return response.choices[0].message.content.splitlines(keepends=True)[1:-1]
        else:
            raise Exception("Invalid OpenAI API Key")
