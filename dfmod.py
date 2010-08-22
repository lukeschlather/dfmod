#!/usr/bin/python
# by Luke Schlather
# Sunday, August 22 2010

import json
import time
import re
from sys import argv
import sys
import os.path

def promptYesNo(prompt,assume=0):
    valid = {"yes":1,   "y":1,"Y":1,
             "no":0,     "n":0, "N":0, "":assume}
    if assume == 0:
        print prompt + " [y/N] "
    else:
        print prompt + " [Y/n] "
    
    response = sys.stdin.readline().rstrip()
    return valid[response]
        


class dfmodule:
    "A module for the game Dwarf Fortress"
    def __init__(self , direct):
        self.directory = direct
        manifest = os.path.join(self.directory,'manifest.json')
        with open(manifest) as manifestFile:
            metadata = json.load(manifestFile)
            self.name = metadata['name']
            self.url = metadata['url']
            self.description = metadata['description']
            self.purge = metadata['purge']
            self.copy = metadata['copy']
            self.patch = metadata['patch']
            self.targetVersions = (metadata['targetVersionMin'],metadata['targetVersionMax'])

    def install(self,target_release):
        # todo: version checking. 
        # Grep 'release notes.txt' for version, check against metadata.

        # todo: fuzzy version checking
        # Grep 'file changes.txt' to see if Toady changed any files included in this module, and 
        # if so warn the user. 

        self.pretty_print()
        if promptYesNo("Are you sure you want to install this package? "):
            print "Installing..."
            print "This package deletes and replaces the following directories:"
            for purgedir in self.purge:
                targetPath = os.path.join(target_release, purgedir)
                modPath = os.path.join(self.directory, purgedir)
                print "Delete " + targetPath
                print "Copy " + modPath + " to " + targetPath
            print "\nThis package copies the following files/directories (overwriting files if they exist):"
            for copyfile in self.copy:
                targetPath = os.path.join(target_release, copyfile)
                modPath = os.path.join(self.directory, copyfile)
                print "Copy " + modPath + " to " + targetPath
            print "\nThis package patches the following files:"
            for patchfile in self.patch:
                targetPath = os.path.join(target_release, copyfile)
                modPath = os.path.join(self.directory, copyfile)
                print "Apply " + modPath + " to " + targetPath

            # todo: handle existing savegames
        #exit(0)
        

    def pretty_print(self):
        "==Dwarf Fortress Module=="
        print "Name: " + self.name
        print "URL: " + self.url
        print "Description: " + self.description
        print "Compatible with Dwarf Fortress Versions " + self.targetVersions[0] + " through " + self.targetVersions[1]
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
        
    module = dfmodule(mod)
    module.install(targ)
elif argv[1]=='show' and len(argv) == 3:
    module=dfmodule(os.path.abspath(argv[2]))
    module.pretty_print()
else:
    print usage



exit(0)

