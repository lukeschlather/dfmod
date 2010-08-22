#!/usr/bin/python
# by Luke Schlather
# Sunday, August 22 2010

import sys
sys.path.append('..')
import dwarfmod
import os.path
import shutil

master_init = os.path.abspath("init.txt.31.12_win")
init_patch = os.path.abspath("init.txt.dfpat")
init = os.path.abspath("init.txt")

shutil.copy(master_init,init)

dwarfmod.rawPatchMerge(init_patch,init)
