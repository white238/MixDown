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

import os, sys, unittest, mdTestUtilities

if not ".." in sys.path:
    sys.path.append("..")
import mdAutoTools, mdLogger, utilityFunctions

class Test_mdAutoTools(unittest.TestCase):
    def test_isAutoToolsProject1(self):
        self.assertTrue(mdAutoTools.isAutoToolsProject("cases/simpleGraphAutoTools/TestCaseA"), "Failed to detect AutoTools project.")
        self.assertFalse(mdAutoTools.isAutoToolsProject("cases/cmake/hello/main"), "False positive when given CMake project.")

    def test_isAutoToolsProject2(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tempFile = utilityFunctions.includeTrailingPathDelimiter(tempDir) + "configure"
            mdTestUtilities.createBlankFile(tempFile)
            self.assertTrue(mdAutoTools.isAutoToolsProject(tempDir), "Failed to detect AutoTools project.")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_isAutoToolsProject3(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tempFile = utilityFunctions.includeTrailingPathDelimiter(tempDir) + "configure.in"
            mdTestUtilities.createBlankFile(tempFile)
            self.assertTrue(mdAutoTools.isAutoToolsProject(tempDir), "Failed to detect AutoTools project.")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_isAutoToolsProject4(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tempFile = utilityFunctions.includeTrailingPathDelimiter(tempDir) + "configure.ac"
            mdTestUtilities.createBlankFile(tempFile)
            self.assertTrue(mdAutoTools.isAutoToolsProject(tempDir), "Failed to detect AutoTools project.")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_getInstallDir1(self):
        installDir = mdAutoTools.getInstallDir("configure --prefix=/usr/local")
        self.assertEquals(installDir, "/usr/local", "Wrong install directory returned.")

    def test_getInstallDir2(self):
        installDir = mdAutoTools.getInstallDir("./configure --prefix=/usr/local")
        self.assertEquals(installDir, "/usr/local", "Wrong install directory returned.")

    def test_getInstallDir3(self):
        installDir = mdAutoTools.getInstallDir("./configure --prefix=/usr/local --with-A=/usr/local/a")
        self.assertEquals(installDir, "/usr/local", "Wrong install directory returned.")

    def test_getInstallDir4(self):
        installDir = mdAutoTools.getInstallDir("./configure --prefix=foobarbaz")
        self.assertEquals(installDir, "foobarbaz", "Wrong install directory returned.")

    def test_getInstallDir5(self):
        installDir = mdAutoTools.getInstallDir("./configure --prefix=")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir6(self):
        installDir = mdAutoTools.getInstallDir("./configure --prefix= --with-A=/usr/local/a")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir7(self):
        installDir = mdAutoTools.getInstallDir("test && ./configure --prefix= --with-A=/usr/local/a")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir8(self):
        #False positive
        installDir = mdAutoTools.getInstallDir("./cmake --prefix=foobarbaz")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir9(self):
        #False positive
        installDir = mdAutoTools.getInstallDir("./configure --prefixasdf=temp/")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir10(self):
        #False positive
        installDir = mdAutoTools.getInstallDir("./configure --with-prefix=temp/")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir11(self):
        #False positive
        installDir = mdAutoTools.getInstallDir("--with-prefix=temp/")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getDependancies1(self):
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/simpleGraphAutoTools/TestCaseA")
            dependancies = mdAutoTools.getDependancies(tempDir, verbose=False)
            dependancies.sort()
            self.assertEquals(dependancies, ['testcaseb', 'testcasec'], "Wrong dependancies found in AutoTools project")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_getDependancies2(self):
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/simpleGraphAutoTools/TestCaseB")
            dependancies = mdAutoTools.getDependancies(tempDir, verbose=False)
            self.assertEquals(dependancies, ['testcasec'], "Wrong dependancies found in AutoTools project")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_getDependancies3(self):
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/simpleGraphAutoTools/TestCaseC")
            dependancies = mdAutoTools.getDependancies(tempDir, verbose=False)
            self.assertEquals(dependancies, ['testcased'], "Wrong dependancies found in AutoTools project")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_getDependancies4(self):
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/simpleGraphAutoTools/TestCaseD")
            dependancies = mdAutoTools.getDependancies(tempDir, verbose=False)
            self.assertEquals(dependancies, [], "Wrong dependancies found in AutoTools project")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_getDependancies5(self):
        #False positive
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/cmake/hello/main")
            dependancies = mdAutoTools.getDependancies(tempDir, verbose=False)
            self.assertEquals(dependancies, None, "Wrong dependancies found in AutoTools project")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_getDependancies6(self):
        #False positive
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/cmake/hello/hello1")
            dependancies = mdAutoTools.getDependancies(tempDir, verbose=False)
            self.assertEquals(dependancies, None, "Wrong dependancies found in AutoTools project")
        finally:
            utilityFunctions.removeDir(tempDir)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_mdAutoTools))
    return suite

if __name__ == "__main__":
    mdLogger.SetLogger("Console")
    unittest.main()