#!/usr/bin/python
# by Luke Schlather
# Sunday, August 22 2010

import json
import time
import re
import sys
from sys import argv
import os.path
import distutils.dir_util
import shutil
import tempfile
import zipfile
from dwarfmod import *

usage = '''
Usage: dfmod.py install <target-release> <module>
       - Adds the module specified to the target release of Dwarf fortress. i.e.
       dfmod.py install df_linux maydayDFG[.zip]
       
       dfmod.py add <module>
       Like above, but assumes the current directory is <target-release>

       dfmod.py show <module>
       - show contents and description of module

       wishlist:
       dfmod.py validate <module>
       -  check validity of module (probably not worth trouble)
       dfmod.py dry-run <target-release> <module> 
       - don\'t install, just show what would happen
       dfmod.py remove <target-release> <module>
todo: implement zip
'''

if len(argv) < 2:
    print usage
    exit(1)
elif argv[1] == 'install':
    if len(argv) == 3:
        targ = os.path.abspath('') # assume current working directory
        mod = os.path.abspath(argv[2])
    elif len(argv) == 4:
        targ = os.path.abspath(argv[2])
        mod = os.path.abspath(argv[3])
    else:
        print len(argv)
        print 'Error: wrong number of arguments.'
        print usage
        exit(1)

    if not zipfile.is_zipfile(mod):         # Check type of specified module;
        module = dfmodule(mod)              # if it's a zipfile, extract it to
    else:                                   # a temporary directory and
        tmpdir = tempfile.mkdtemp()         # install from there.
        try:
            zipmod = zipfile.ZipFile(mod, 'r')
            zipmod.extractall(tmpdir)       # DANGER WILL ROBINSON - this is
        except zipfile.BadZipfile:          # very  unsafe! Needs sanitization.
            print 'Error: incorrect format or corrupted module file.'
            exit(2)
        module = dfmodule(tmpdir)
    # todo: path sanitization while extracting the module
    # todo: maybe handle this in a less stupid manner (but maybe not, if this works)

    module.install(targ)

elif argv[1] == 'dry-run':
    if len(argv) == 3:
        targ = os.path.abspath('') # assume current working directory
        mod = os.path.abspath(argv[2])
    elif len(argv) == 4:
        targ = os.path.abspath(argv[2])
        mod = os.path.abspath(argv[3])
    else:
        print len(argv)
        print 'Error: wrong number of arguments.'
        print usage
        exit(1)
        
    module = dfmodule(mod)
    module.dryrun(targ)

elif argv[1]=='show' and len(argv) == 3:
    module=dfmodule(os.path.abspath(argv[2]))
    module.pretty_print()
else:
    print usage



exit(0)

