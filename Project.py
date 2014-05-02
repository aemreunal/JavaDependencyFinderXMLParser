#!/usr/bin/env python3

import Package

#
# This code belongs to:
# Ahmet Emre Unal
# S001974
# emre.unal@ozu.edu.tr
#


class Project(object):
    # Fields:
    # - packages

    def __init__(self):
        self.packages = {}

    def addPackage(self, package):
        try:
            self.packages[package.getName()]
        except KeyError:
            self.packages[package.getName()] = package

    def getOrCreatePackage(self, packageName):
        try:
            return self.packages[packageName]
        except KeyError:
            newPackage = Package.Package(packageName)
            self.packages[packageName] = newPackage
            return newPackage

    def getModule(self, fullName):
        (packageName, moduleName) = self.splitPackageAndModuleName(fullName)
        package = self.getOrCreatePackage(packageName)
        return package.getOrCreateModule(moduleName)

    def getPackages(self):
        return self.packages

    def getNumDependencies(self):
        count = 0
        for packageName in self.packages:
            count += self.packages[packageName].getNumDependencies()
        return count

    def printProjectStatistics(self):
        numEdges = 0  # Number of Edges
        numNodes = 0  # Number of Nodes

        sortedPackages = sorted(self.packages, key=lambda packageName: self.packages[packageName].getNumDependencies(), reverse=True)

        for packageName in sortedPackages:
            package = self.packages[packageName]

            numDependencies = package.getNumDependencies()
            numEdges += numDependencies

            numModules = package.getNumModules()
            numNodes += numModules

            print('Package {0} has total of {1} dependencies from a total of {2} modules.'.format(packageName, numDependencies, numModules))
            package.printHighlyCoupledModules()
            print()

        print('Total number of modules (nodes): {0}'.format(numNodes))
        print('Total number of dependencies (edges): {0}'.format(numEdges))

        edgeToNodeRatio = numEdges / numNodes
        print('Edge-to-Node ratio: {0}'.format(edgeToNodeRatio))

        treeImpurity = 2 * (numEdges - numNodes + 1) / ((numNodes - 1)*(numNodes - 2))
        print('Tree impurity: {0}'.format(treeImpurity))

    @staticmethod
    def splitPackageAndModuleName(name):
        dotPos = name.rfind('.')
        packageName = name[:dotPos]
        moduleName = name[dotPos + 1:]
        return (packageName, moduleName)
