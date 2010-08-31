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
Usage: dfmod.py install [target-release] <module>
       - Adds the module specified to the target release of Dwarf fortress. i.e.
       dfmod.py install df_linux maydayDFG
       - If target-release is unspecified, will use the current directory as
       the target

       dfmod.py dry-run [target-release] <module>
       - Like install, but doesn't change any files (only shows changes)

       dfmod.py show <module>
       - show contents and description of module

       wishlist:
       dfmod.py validate <module>
       - check validity of module (probably not worth trouble)
       dfmod.py remove <target-release> <module>
'''

# Determine installation target
if len(argv) <= 2 or len(argv) >= 5:
    print usage
    exit(1)
elif len(argv) == 3:
	targ = os.path.abspath('')	# assume current working directory
	mod = os.path.abspath(argv[2])
elif len(argv) == 4:
	targ = os.path.abspath(argv[2])
	mod = os.path.abspath(argv[3])
else:
	print usage
	exit(1)

# Prepare installation source
if not zipfile.is_zipfile(mod):
	is_zipmod = False
	module = dfmodule(mod)
else:
    is_zipmod = True
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
else:
	print usage
	exit(1)

# Cleanup temporary directories
if is_zipmod:
	shutil.rmtree(tmpdir)

exit(0)
