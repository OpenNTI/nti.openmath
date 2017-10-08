#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import six

from xml.dom.minidom import Text
from xml.dom.minidom import parseString

OMS = 'OMS'
OMA = 'OMA'
OMV = 'OMV'
OMI = 'OMI'
OMF = 'OMF'
OMOBJ = 'OMOBJ'

logger = __import__('logging').getLogger(__name__)


def binaryOperator(op, arg1, arg2):
    return '%s %s %s' % (arg1, op, arg2)


def unaryOperator(op, arg1):
    return '%s%s' % (op, arg1)


def latexMacro(macro, *args):
    result = ['%s' % macro]
    for arg in args:
        result.append('{%s}' % arg)
    return ''.join(result)


def sqrt(arg1, arg2):
    result = ['\\sqrt']
    if arg2 != '2':
        result.append('[%s]' % arg2)
    result.append('{%s}' % arg1)
    return ''.join(result)


def power(x, y):
    return '%s^{%s}' % (x, y)

arith1 = {
    'root': [sqrt, '#1', '#2'],
    'power': [power, '#1', '#2'],
    'plus': [binaryOperator, '+', '#1', '#2'],
    'unary_minus': [unaryOperator, '-', '#1'],
    'minus': [binaryOperator, '-', '#1', '#2'],
    'times': [binaryOperator, '*', '#1', '#2'],
    'divide': [latexMacro, '\\frac', '#1', '#2'],
}

nums1 = {'pi': '\\pi'}


class OpenMath2Latex(object):

    contentDicts = {
        'nums1': nums1,
        'arith1': arith1
    }

    def translate(self, openMathXML):
        dom = parseString(openMathXML)
        
        omobj = dom.firstChild
        if omobj.localName != OMOBJ:
            logger.warn('Expected %s but found %s.  Are you sure this is open math',
                        OMOBJ, omobj.localName)
            return '\\Unknown{%s}' % omobj.localName

        oma = self.getChild(omobj, OMA)
        handler = self.handleOMA
        if oma is None or oma.localName != OMA:
            # find first non text node
            i = 0
            while   i < len(omobj.childNodes) \
                and isinstance(omobj.childNodes[i], Text):
                i += 1
            if i < len(omobj.childNodes):
                # process first node found
                attrib = 'handle' + omobj.childNodes[i].localName
                if hasattr(self, attrib):
                    handler = getattr(self, attrib)
                    oma = omobj.childNodes[i]
                else:
                    oma = omobj.childNodes[i].localName
                    logger.warn('Expected %s but found %s',
                                OMA, oma)
                    return '\\Unknown{%s}' % oma
            else:
                logger.warn('No open math element found')
                return None

        result = '$%s$' % handler(oma)
        return result

    def getChild(self, node, childName):
        for child in node.childNodes or ():
            if child.localName == childName:
                return child
        return None

    def handleOMS(self, node):
        """
        Returns a tuple of the contentdictionary
        add operator name.

        <OMS cd="arith1" name="unary_minus"/>
        returns
        (arith1, unary_minus)

        e.g.
        """

        cd = node.getAttribute('cd')
        name = node.getAttribute('name')
        return (cd, name)

    def handleOMA(self, node):
        # First child should be the operator
        children = node.childNodes

        args = None
        translator = None
        possibleArgs = []

        for child in children or ():

            if child.localName == OMS:

                cdname, opname = self.handleOMS(child)
                cd = self.contentDicts[cdname]

                content = cd.get(opname) if cd else None
                if content is None:
                    logger.warn('Unknown content for %s:%s', cdname, opname)
                    return '\\Unknowncontent{%s}{%s}' % (cdname, opname)

                if isinstance(content, six.string_types):
                    possibleArgs.append(content)
                    continue

                translator = content[0]
                args = content[1:]

            elif child.localName == OMI:
                possibleArgs.append(self.handleOMI(child))

            elif child.localName == OMV:
                possibleArgs.append(self.handleOMV(child))

            elif child.localName == OMA:
                possibleArgs.append(self.handleOMA(child))

            elif child.localName == OMF:
                possibleArgs.append(self.handleOMF(child))
            else:
                logger.warn('Unhandle element %s', child.localName)

        if not translator:
            logger.warn('No operator found')
            return '\\NoOperatorFound{%s}' % node.localName

        translatorArgs = []

        for arg in args or ():
            if arg[0] == '#':
                translatorArgs.append(possibleArgs.pop(0))
            else:
                translatorArgs.append(arg)

        return self.executeTranslator(translator, translatorArgs)

    def executeTranslator(self, func, args):
        return func(*args)

    def handleOMF(self, node):
        """
        OMF has a dec attribute that contains
        the value.  e.g. <OMF decimal="40000"/>
        """
        return node.getAttribute('dec')

    def handleOMV(self, node):
        """
        OMV has a name attribute that contains
        the variable name.  e.g. <OMV name="a"/>
        """
        return node.getAttribute('name')

    def handleOMI(self, node):
        """
        OMI should have on child that is a text node
        e.g. <OMI>4</OMI>
        """
        return node.firstChild.data
