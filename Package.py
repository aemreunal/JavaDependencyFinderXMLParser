#!/usr/bin/env python3

import Module

NUM_MODULES_TO_PRINT = 3


class Package(object):
    # Fields:
    # - name
    # - modules

    def __init__(self, name):
        self.name = name
        self.modules = {}

    def getName(self):
        return self.name

    def addModule(self, module):
        try:
            self.modules[module.getName()]
        except KeyError:
            self.modules[module.getName()] = module

    def getOrCreateModule(self, moduleName):
        try:
            return self.modules[moduleName]
        except KeyError:
            newModule = Module.Module(moduleName)
            self.modules[moduleName] = newModule
            return newModule

    def getModules(self):
        return self.modules

    def getNumDependencies(self):
        count = 0
        for moduleName in self.modules:
            count += self.modules[moduleName].getNumDependencies()
        return count

    def getNumModules(self):
        return len(self.modules)

    def printHighlyCoupledModules(self):
        sortedModules = sorted(self.modules, key=lambda moduleName: self.modules[moduleName].getNumDependencies(), reverse=True)
        for moduleName in sortedModules[:NUM_MODULES_TO_PRINT]:
            print('\tModule {0} has {1} dependencies.'.format(moduleName, self.modules[moduleName].getNumDependencies()))
