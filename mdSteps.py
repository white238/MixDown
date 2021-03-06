# Copyright (c) 2010, Lawrence Livermore National Security, LLC
# Produced at Lawrence Livermore National Laboratory
# LLNL-CODE-462894
# All rights reserved.
#
# This file is part of MixDown. Please read the COPYRIGHT file
# for Our Notice and the LICENSE file for the GNU Lesser General Public
# License.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License (as published by
# the Free Software Foundation) version 3 dated June 2007.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
#  You should have recieved a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import os, tarfile, urllib, mdGit, mdHg, mdSvn, utilityFunctions

from mdLogger import *

def fetch(pythonCallInfo):
    if mdGit.isGitRepo(pythonCallInfo.currentPath):
        if not mdGit.gitCheckout(pythonCallInfo.currentPath, pythonCallInfo.outputPath):
            pythonCallInfo.logger.writeError("Given Git repo '" + pythonCallInfo.currentPath +"' was unable to be checked out")
        else:
            pythonCallInfo.currentPath = pythonCallInfo.outputPath
            pythonCallInfo.success = True
    elif mdHg.isHgRepo(pythonCallInfo.currentPath):
        if not mdHg.hgCheckout(pythonCallInfo.currentPath, pythonCallInfo.outputPath):
            pythonCallInfo.logger.writeError("Given Hg repo '" + pythonCallInfo.currentPath +"' was unable to be checked out")
        else:
            pythonCallInfo.currentPath = pythonCallInfo.outputPath
            pythonCallInfo.success = True
    elif mdSvn.isSvnRepo(pythonCallInfo.currentPath):
        if not mdSvn.svnCheckout(pythonCallInfo.currentPath, pythonCallInfo.outputPath):
            pythonCallInfo.logger.writeError("Given Svn repo '" + pythonCallInfo.currentPath +"' was unable to be checked out")
        else:
            pythonCallInfo.currentPath = pythonCallInfo.outputPath
            pythonCallInfo.success = True
    elif utilityFunctions.isURL(pythonCallInfo.currentPath):
        filenamePath = pythonCallInfo.downloadDir + utilityFunctions.URLToFilename(pythonCallInfo.currentPath)
        if not os.path.exists(pythonCallInfo.downloadDir):
            os.mkdir(pythonCallInfo.downloadDir)
        urllib.urlretrieve(pythonCallInfo.currentPath, filenamePath)
        pythonCallInfo.currentPath = filenamePath
        pythonCallInfo.success = True
    elif os.path.isdir(pythonCallInfo.currentPath):
        if pythonCallInfo.outputSpecified:
            distutils.dir_util.copy_tree(pythonCallInfo.currentPath, pythonCallInfo.outputPath)
            pythonCallInfo.currentPath = self.pythonCallInfo.outputPath
        pythonCallInfo.success = True
    elif os.path.isfile(pythonCallInfo.currentPath):
        pythonCallInfo.success = True

    return pythonCallInfo

def unpack(pythonCallInfo):
    if os.path.isfile(pythonCallInfo.currentPath):
        if tarfile.is_tarfile(pythonCallInfo.currentPath):
            utilityFunctions.untar(pythonCallInfo.currentPath, pythonCallInfo.outputPath, True)
            pythonCallInfo.currentPath = pythonCallInfo.outputPath
            pythonCallInfo.success = True
        else:
            if pythonCallInfo.currentPath.endswith(".tar.gz") or pythonCallInfo.currentPath.endswith(".tar.bz2")\
               or pythonCallInfo.currentPath.endswith(".tar") or pythonCallInfo.currentPath.endswith(".tgz")\
               or pythonCallInfo.currentPath.endswith(".tbz") or pythonCallInfo.currentPath.endswith(".tb2"):
                pythonCallInfo.logger.writeError("Given tar file '" + pythonCallInfo.currentPath +"' not understood by python's tarfile package and possibly corrupt")
            else:
                pythonCallInfo.logger.writeError("Given file '" + pythonCallInfo.currentPath + "' cannot be unpacked")
    elif os.path.isdir(pythonCallInfo.currentPath):
        pythonCallInfo.success = True
    else:
        pythonCallInfo.logger.writeError("Given path '" + pythonCallInfo.currentPath + "' not understood by MixDown's unpack (path should be a file or a directory at this point)")
        pythonCallInfo.success = False

    return pythonCallInfo

