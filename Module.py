#!/usr/bin/env python3

#
# This code belongs to:
# Ahmet Emre Unal
# S001974
# emre.unal@ozu.edu.tr
#

class Module(object):
    # Fields:
    # - name
    # - inbound

    def __init__(self, name):
        self.name = name
        self.inbound = {}

    def getName(self):
        return self.name

    def addInboundDependency(self, module):
        try:
            self.inbound[module.getName()]
        except KeyError:
            self.inbound[module.getName()] = module

    def getDependencies(self):
        return self.inbound

    def getNumDependencies(self):
        return len(self.inbound)
