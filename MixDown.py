#! /usr/bin/env python

import os, sys, tarfile, urllib

from mdOptions import *
from mdProject import *
from mdTarget import *
from utilityFunctions import *
from mdPreConfigure import *
from mdConfigure import *
from mdBuild import *
from mdLogger import *

#--------------------------------Main---------------------------------
def main():
    printProgramHeader()

    project, options = setup()
    for target in project.targets:
        preConfigure(target, options)
        configure(target, options)
        build(target, options)
        deploy(project, options)    
    cleanup(options)
    
    sys.exit()
        
#--------------------------------Setup---------------------------------
def setup():
    options = Options()
    print "Processing commandline options..."
    options.processCommandline()
    SetLogger(options.logger)
    
    if options.verbose:
        Logger().writeMessage(str(options))

    #Clean workspaces if told to clean before
    #TODO: Clean output directories in all targets
    if options.cleanBefore:
        Logger().writeMessage("Cleaning MixDown directories...")
        try:
            removeDir(options.buildDir)
            removeDir(options.downloadDir)
            removeDir(options.installDir)
            removeDir(options.logDir)
        except IOError, e:
            print e
            sys.exit()
    if not os.path.isdir(options.buildDir):
        os.makedirs(options.buildDir)
    if not os.path.isdir(options.downloadDir):
        os.makedirs(options.downloadDir)
    if not os.path.isdir(options.installDir):
        os.makedirs(options.installDir)
    
    #Read project file
    project = Project(options.projectFile)
    
    #Convert all targetPaths to folders (download and/or unpack if necessary)
    Logger().writeMessage("Converting all targets to local directories...")

    #Check for files that need to be downloaded
    for currTarget in project.targets:
        currPath = currTarget.path
        if (not os.path.isdir(currPath)) and (not os.path.isfile(currPath)) and isURL(currPath):
            filenamePath = options.downloadDir + URLToFilename(currPath)
            urllib.urlretrieve(currPath, filenamePath)
            currTarget.path = filenamePath
    
    #Untar and add trailing path delimiter to any folders
    targetList = project.targets[:]
    targetList.reverse()
    for currTarget in targetList:
        currPath = currTarget.path
        if os.path.isdir(currPath):
            targetPaths[i] = includeTrailingPathDelimiter(currPath)
        elif os.path.isfile(currPath):
            if tarfile.is_tarfile(currPath):
                if currTarget.output == "":
                    outDir = includeTrailingPathDelimiter(options.buildDir + splitFileName(currPath)[0])
                else:
                    outDir = currTarget.output
                untar(currPath, outDir, True)
                currTarget.path = outDir
            else:
                fileExt = os.path.splitext(currPath)[1]
                if basename.endswith(".tar.gz") or basename.endswith(".tar.bz2") or basename.endswith(".tar") or basename.endswith(".tgz") or basename.endswith(".tbz") or basename.endswith(".tb2"):
                    Logger().writeError("Given tar file '" + currPath +"' not understood by python's tarfile package", exit=True)
                else:
                    Logger().writeError("Given target '" + currPath + "' not understood (folders, URLs, and tar files are acceptable)", exit=True)
        else:
            Logger().writeError("Given target '" + currPath + "' does not exist", exit=True)
            
    for currTarget in project.targets:
        currTarget.examine()

    return project, options

#------------------------------Deploy---------------------------------
def deploy(project, options):
    print "TODO: deploy not implemented yet"
    
#-----------------------------Clean up--------------------------------
def cleanup(options):
    if options.cleanAfter:
        Logger().writeMessage("Cleaning MixDown Build and Download directories...")
        try:
            removeDir(options.buildDir)
            removeDir(options.downloadDir)
        except IOError, e:
            Logger().writeError(e, exit=True)

#----------------------------------------------------------------------        
def printProgramHeader():
    print "MixDown - A tool to simplify building\n"
    
def printUsageAndExit(errorStr = ""):
    printUsage(errorStr)
    sys.exit()

def printUsage(errorStr = ""):
    if errorStr != "":
        print "Error: " + errorStr + "\n"
    
    printProgramHeader()
    print "    Example Usage: ./MixDown.py foo.md\\\n\
\n\
    Required:\n\
    <path to .md file>   Path to MixDown project file\n\
\n\
    Optional:\n\
    -b<path>      Override build directory\n\
    -d<path>      Override deploy directory\n\
    -u<path>      Override unpack folder\n\
    -cb           Cleanup before running (deletes unpack, build, and deploy directories)\n\
    -ca           Cleanup after deploy (deletes unpack and build directories)\n\
\n\
    Default Directories:\n\
    build: mdBuild/\n\
    deploy: mdDeploy/\n\
    unpack: mdUnpack/\n"
    
#---------------------------------------------------------------------

if __name__ == "__main__":
    main()