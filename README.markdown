dfmod is a program that hopefully will at the least ease updating of graphics packs for Dwarf Fortress like Phoebus, Mayday, and others. There's also some basic functionality for merging changes to raw files.

The basic way to use this on the command line is somewhat reminiscent of a Linux package manager:

    dfmod install <target> <module>
    
By convention I'm expecting we'll name dfmodules with the extension ".dfm" so if you're installing the example mayday.dfm, you should use 

    dfmod install ~/games/df_linux ~/games/dfmods/mayday.dfm
    
Assuming you unzip the latest release of Dwarf Fortress to ~/games and you save mayday.dfm to ~/games/dfmods/mayday.dfm.

To make a dfmodule, you should create a directory with a structure that mirrors the Dwarf Fortress release, only containing files you want to modify. Then, create a manifest in this format:

    {
        "name":"maydayDFG",
        "url": "http://mayday.w.staszic.waw.pl/DFGtutorial.php",
        "creator":"Mike Mayday",
        "description":"Mike Mayday's Dwarf Fortress pack.",
        "targetVersionMin":"0.31.12",
	"targetVersionMax":"0.31.12",
        "purge": [
    	"raw"
        ],
	// "purge" is meant for directories that you want to delete, 
        // then overwrite
        "copy": [
    	"data/art",
    	"data/init/embark_profiles.txt",
    	"data/init/colors.txt",
    	"data/init/d_init.txt"
        ],
	// "copy" is for files and directories - it will not delete 
	// anything, though it will overwrite files with those in your package
        "patch": [
    	"data/init/init.txt"
        ]
	// patch should merge in changes to raw files of the form 	// [OPTION:SOMETHING]
    }

Note: The JSON spec does not actually allow comments, see the actual manifest in the example mayday.dfm for what this should look like. (This might merit a switch to yml or xml.)


==Bugs
Patch will only change existing options. In other words, if you include [FONT:mayday.png] in your init.txt.dfpat file, it will only end up in the init.txt file if you have [FONT:somefile] in your existing init.txt file. This shouldn't be a problem for a clean release, which presumably includes all options. 

==Needs work

* Currently a .dfm is a directory. It should be zipfile (or at least have support for zipped dfm's. 
* Patch should be gutted.
* If json is a bad idea, that should change very soon.
* Doesn't actually do version checking. Should check 'release notes.txt' for version. Smart checking could also check 'file changes.txt' to see what files have changed since the last release, and only warn the user if files used by the module have changed.
* Jython or IronPython edition for the platform that doesn't come with Python installed. 
* Cross-platform GUI - only halfway decent option for this appears to be Swing via Jython. GUI should enable user to browse available df installs/modules, and see a good representation of the modules' manifests. 

Questions, comments, concerns, or code, let me know.
