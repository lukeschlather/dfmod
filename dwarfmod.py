#!/usr/bin/python
# by Luke Schlather
# Sunday, August 22 2010

import json
import time
import re
from sys import argv
import sys
import os.path
import distutils.dir_util
import shutil



# equivalent to cp -pr : 
# distutils.dir_util.copy_tree(src,dest)
# copy_tree(  	src, dst[preserve_mode=1, preserve_times=1, preserve_symlinks=0, update=0, verbose=0, dry_run=0])

# shutil.copytree(src, dst[, symlinks=False[, ignore=None]])
# equivalent to cp -r, except it won't work if the directory exists.

# 
# shutil.rmtree(path)
# equivalent to rm -r path

def promptYesNo(prompt,assume=0):
    valid = {"yes":1,   "y":1,"Y":1,
             "no":0,     "n":0, "N":0, "":assume}
    if assume == 0:
        print prompt + " [y/N] "
    else:
        print prompt + " [Y/n] "
    
    response = sys.stdin.readline().rstrip()
    return valid[response]
        
def rawPatchMerge(modPath,targetPath):
    shutil.copy(targetPath,targetPath+".old")
    buffer = ''
    with open(modPath) as patchfile:
        newOptions = dict()
        for line in patchfile.readlines():
            m = re.match('\[(.*):.*\]',line)
            if m:
                newOptions[line] = re.compile("\[" + m.group(1) + ":")
        with open(targetPath) as rawfile:
            for line in rawfile.readlines():
                done = 0
                for option in newOptions:
                    if newOptions[option].match(line):
                        buffer+= option
                        done=1
                        break
                if not done:
                    buffer+=line
    with open(targetPath,'w') as rawfile:
        rawfile.write(buffer)
    return 1


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

            #todo: basic path sanitizing to keep them from breaking out of the current directory tree
            # s/..//g would probably do it, though maybe I'm being too paranoid. 
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
                print "Deleting " + targetPath
                shutils.rmtree(targetPath)
                print "Copying " + modPath + " to " + targetPath
                shutils.copytree(modPath,targetPath)
                
            print "\nThis package copies the following files/directories (overwriting files if they exist):"
            for copyfile in self.copy:
                targetPath = os.path.join(target_release, copyfile)
                modPath = os.path.join(self.directory, copyfile)
                print "Copying " + modPath + " to " + targetPath
                distutils.dir_util.copy_tree(modPath,targetPath)
            print "\nThis package patches the following files:"
            for patchfile in self.patch:
                targetPath = os.path.join(target_release, copyfile)
                modPath = os.path.join(self.directory, copyfile)
                print "Applying " + modPath + " to " + targetPath
                rawPatchMerge(modPath,targetPath)
            # todo: handle existing savegames
        return

                
            


    def dryrun(self,target_release):
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
