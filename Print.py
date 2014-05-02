#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import re
import Module
import Package

#
# This code belongs to:
# Ahmet Emre Unal
# S001974
# emre.unal@ozu.edu.tr
#

ignoredPackages = [r'^(java.)', r'^(org.eclipse.)', r'^(javax.)', r'^(org.osgi.)']
filteringPackages = True


def isIgnored(name):
    for rgx in ignoredPackages:
        if re.search(rgx, name):
            return True
    return False


def isUnwanted(text):
    if filteringPackages:
        return text.find('$') != -1 or isIgnored(text)
    else:
        return text.find('$') != -1


def printName(name):
    if not isUnwanted(name):
        print(name)


def processName(name):
    paran = name.find('(')
    if paran != -1:
        # If there is a parenthesis
        name = name[:paran]
    if not isIgnored(name):
        return name[:name.rindex('.')]
    else:
        return name


def printClassDependencies(item, packageName, level):
    for name in item.findall('name'):
        if not isUnwanted(name.text):
            printName('%s\tClass: %s' % (
                3 * level * '\t', name.text[len(packageName) + 1:]))  # Print class name - packageName + '.'

            printInOutDependencies(item, level)


def printInOutDependencies(item, level):
    print('%s\t\tInbound dependencies:' % (3 * level * '\t'))
    for inDepend in item.findall('inbound'):
        if not isUnwanted(inDepend.text):
            typ = inDepend.get('type')

            if typ != 'class':
                printName('%s\t\t\t-%s: %s' % (
                    3 * level * '\t', typ, processName(inDepend.text)))  # Print inbound dependency name
            else:
                printName('%s\t\t\t-%s: %s' % (3 * level * '\t', typ, inDepend.text))  # Print inbound dependency name

    print('%s\t\tOutbound dependencies:' % (3 * level * '\t'))
    for outDepend in item.findall('outbound'):
        if not isUnwanted(outDepend.text):
            typ = outDepend.get('type')
            if typ != 'class':
                printName('%s\t\t\t-%s: %s' % (
                    3 * level * '\t', typ, processName(outDepend.text)))  # Print outbound dependency name
            else:
                printName('%s\t\t\t-%s: %s' % (3 * level * '\t', typ, outDepend.text))  # Print outbound dependency name


tree = ET.parse('Dependencies.xml')
dependencies = tree.getroot()

for package in dependencies:
    for attr in range(len(package)):
        if not isUnwanted(package[0].text):
            if attr == 0:  # Print package name
                printName('Package: %s' % package[attr].text)
            else:
                printClassDependencies(package[attr], package[0].text, 0)
