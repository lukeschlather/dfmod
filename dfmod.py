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

# Determine installation target
if len(argv) <= 2:
    print usage
    exit(1)
elif len(argv) == 3:
	targ = os.path.abspath('')	# assume current working directory
elif len(argv) == 4:
	targ = os.path.abspath(argv[2])
else
	print usage
	exit(1)

# Prepare installation source
if not zipfile.is_zipfile(mod):
	is_zipmod = false
    module = dfmodule(mod)
else:
	is_zipmod = true
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

# Perform specified action
if argv[1] == 'install':
	module.install(targ)
elif argv[1] == 'dry-run':
	module.dryrun(targ)
elif argv[1] == 'show':
	module.pretty_print()
else
	print usage
	exit(1)

# Cleanup temporary directories
if is_zipmod:
	shutil.rmtree(tmpdir)

exit(0)
