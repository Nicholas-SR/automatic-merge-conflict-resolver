
import stat
import bz2
import collections
import bz2
import functools
import filelock
import stat
import collections



def helloWorld():
<<<<<<< HEAD
    main = 5+6
    print(  "Hello World!"  )
    main+=1
=======
    main = 5 + 6
    print("Hello World!")
    main += 1
>>>>>>> import_conflict

<<<<<<< HEAD
    main = 5+6
    # comment 1
    print("Hello World!")
    main+=1
=======
    main = 5 + 6
    # comment 1
    print("Hello World!")
    main += 1
>>>>>>> import_conflict

helloWorld()