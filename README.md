# automatic-merge-conflict-resolver
Automatic Merge Conflict Resolver automatically resolves common git merge conflicts.

# Setup
1. Run the following command in the root directory:
```git config --local include.path ../.gitconfig```

2. Install and configure the [chatgpt-wrapper](https://github.com/mmabrouk/chatgpt-wrapper) package and the packages in requirements.txt

# Execution
After getting a merge conflict, run this command:
```git mergetool -t amcr PATH/TO/FILE/WITH/MERGE/CONFLICT.py```

Or leave the file path unspecified to run the mergetool on all files in the directory and subdirectories with merge conflicts:
```git mergetool -t amcr```


# Development
An alias is included to speed up development and testing. It aborts the merge, starts a new merge, then runs the mergetool.

Windows: ```mergeAlias.bat``` or ```bash mergeAlias.sh```

MacOS: ```bash mergeAlias.sh```

# Testing
To run tests, execute ```pytest``` in the terminal from the home directory