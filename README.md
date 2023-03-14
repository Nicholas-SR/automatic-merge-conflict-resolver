# automatic-merge-conflict-resolver
Automatic Merge Conflict Resolver automatically resolves common git merge conflicts.

# Setup
1. Run the following command in the root directory:
```git config --local include.path ../.gitconfig```

2. Install and configure the [chatgpt-wrapper](https://github.com/mmabrouk/chatgpt-wrapper) package

# Execution
After getting a merge conflict, run this command:
```git mergetool -t amcr PATH/TO/FILE/WITH/MERGE/CONFLICT.py```

# Development
An alias is included to speed up development and testing. It aborts the merge, starts a new merge, then runs the mergetool.

Windows: ```mergeAlias.bat``` or ```bash mergeAlias.sh```

MacOS: ```bash mergeAlias.sh```

# Testing
To run tests, execute ```pytest``` in the terminal from the home directory