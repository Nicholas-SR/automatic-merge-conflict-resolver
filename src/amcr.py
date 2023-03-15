import sys
from handlers import *
from recognizers import *
from utils import *

fbase = sys.argv[1]      # The first shared ancestor
flocal = sys.argv[2]     # Your local file
fremote = sys.argv[3]    # File coming from the remote
fmerge = sys.argv[4]     # File to write the successful merge to

baseInput = open(fbase).readlines()
localInput = open(flocal).readlines()
remoteInput = open(fremote).readlines()
mergeInput = open(fmerge).readlines()

foundConflicts = parser(mergeInput)

processedConflicts = differ(foundConflicts, mergeInput)

removedNewNewLines = merger(processedConflicts)

joined = unparser(removedNewNewLines, fmerge)

print(joined)
print("----------------------")
