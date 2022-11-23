import sys

fbase = sys.argv[1]      # The first shared ancestor
flocal = sys.argv[2]     # Your local file
fremote = sys.argv[3]    # File coming from the remote
fmerge = sys.argv[4]     # File to write the successful merge to

base = open(fbase).readlines()
local = open(flocal).readlines()
remote = open(fremote).readlines()
merge = open(fmerge).readlines()
