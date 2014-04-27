#!/usr/bin/env python3

import Package


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

    def printHighlyCoupledPackages(self):
        sortedPackages = sorted(self.packages, key=lambda packageName: self.packages[packageName].getNumDependencies(), reverse=True)
        for packageName in sortedPackages:
            package = self.packages[packageName]
            print('Package {0} has {1} dependencies.'.format(packageName, package.getNumDependencies()))
            package.printHighlyCoupledModules()
            print()

    @staticmethod
    def splitPackageAndModuleName(name):
        dotPos = name.rfind('.')
        packageName = name[:dotPos]
        moduleName = name[dotPos + 1:]
        return (packageName, moduleName)
