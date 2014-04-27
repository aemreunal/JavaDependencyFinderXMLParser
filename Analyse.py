#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import re
import Module
import Package
import Project

dependencies = ET.parse('Dependencies.xml').getroot()
project = Project.Project()

ignoredPackages = [r'^(java.)', r'^(org.eclipse.)', r'^(javax.)', r'^(org.osgi.)']
filteringPackages = True


def main():
    for package in dependencies:
        packageName = package[0].text
        if not isUnwanted(packageName):
            for attr in range(len(package)):
                if attr != 0:  # Skip package name attribute
                    createPackage(package[attr], packageName)
    project.printProjectStatistics()


def isIgnored(name):
    if not filteringPackages:
        return False
    else:
        for rgx in ignoredPackages:
            if re.search(rgx, name):
                return True
        return False


def isUnwanted(text):
    return text.find('$') != -1 or isIgnored(text)


def printName(name):
    if not isUnwanted(name):
        print(name)


def processName(name):
    parenthesisLocation = name.find('(')
    if parenthesisLocation != -1:
        # If there is a parenthesis
        name = name[:parenthesisLocation]
    if not isIgnored(name):
        return name[:name.rindex('.')]
    else:
        return name


def createPackage(item, packageName):
    package = project.getOrCreatePackage(packageName)

    for name in item.findall('name'):
        if not isUnwanted(name.text):
            moduleName = name.text[len(packageName) + 1:]
            module = package.getOrCreateModule(moduleName)
            addDependencyRelations(item, module)


def addDependencyRelations(item, module):
    # Inbound dependencies
    addRelationType(item, module, 'inbound', addInDependency)

    # Outbound dependencies
    addRelationType(item, module, 'outbound', addOutDependency)


def addRelationType(item, module, typ, action):
    for dependency in item.findall(typ):
        if not isUnwanted(dependency.text):
            dependencyName = dependency.text
            if dependency.get('type') != 'class':
                dependencyName = processName(dependencyName)
            action(dependencyName, module)


def addInDependency(dependencyName, module):
    module.addInboundDependency(project.getModule(dependencyName))


def addOutDependency(dependencyName, module):
    project.getModule(dependencyName).addInboundDependency(module)


if __name__ == "__main__":
    main()
