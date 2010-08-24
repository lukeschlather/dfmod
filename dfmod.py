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

    if not zipfile.is_zipfile(mod):
        module = dfmodule(mod)
		module.install(targ)
    else:
        tmpdir = tempfile.mkdtemp()
        zipmod = zipfile.ZipFile(mod, 'r')
        for member in zipmod.infolist():
            path = os.path.normpath(os.path.join(tmpdir, member.filename))
            if re.match(tmpdir + ".*", path):
                zipmod.extract(member, tmpdir)
            else:
                print "Warning: skipping out-of-path file " + path + " (possibly malicious module?)"
				if not promptYesNo("Continue with installation?", 0):
                    shutil.rmtree(tmpdir)
                    exit(1)
        module = dfmodule(tmpdir)
        module.install(targ)
        shutil.rmtree(tmpdir)
		
    # todo: maybe handle this in a less stupid manner (but maybe not, if this works)

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

