# automatic-merge-conflict-resolver
Automatic Merge Conflict Resolver automatically resolves common git merge conflicts.

# Setup
Run the following command in the root directory:
```git config --local include.path ../.gitconfig```

# Execution
After obtaining a merge conflict, run this command:
```git mergetool -t amcr PATH/TO/FILE/WITH/MERGE/CONFLICT.py```