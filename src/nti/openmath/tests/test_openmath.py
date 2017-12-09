#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import none
from hamcrest import assert_that

import os
import unittest

from nti.openmath import OpenMath2Latex


class TestAssessment(unittest.TestCase):

    inputDir = 'openmath'

    def setUp(self):
        self.translator = OpenMath2Latex()

    def test_simplemath(self):
        result = self.translateOpenMath('simplemath.xml')
        assert_that(result, is_('$31 + 3$'))

        result = self.translateOpenMath('simplemath2.xml')
        assert_that(result, is_('$31 - 3$'))

        result = self.translateOpenMath('simplemath3.xml')
        assert_that(result, is_('$31 * 3$'))

        result = self.translateOpenMath('simplemath4.xml')
        assert_that(result, is_('$-31$'))

    def test_mathwithvars(self):
        result = self.translateOpenMath('varmath.xml')
        assert_that(result, is_('$x + 3$'))

        result = self.translateOpenMath('varmath2.xml')
        assert_that(result, is_('$x - 3$'))

        result = self.translateOpenMath('varmath3.xml')
        assert_that(result, is_('$x * 3$'))

        result = self.translateOpenMath('varmath4.xml')
        assert_that(result, is_('$-x$'))

    def test_basicmacros(self):
        result = self.translateOpenMath('macromath.xml')
        assert_that(result, is_('$\\frac{1}{2}$'))

        result = self.translateOpenMath('macromath2.xml')
        assert_that(result, is_('$\\frac{1}{x}$'))

        result = self.translateOpenMath('macromath3.xml')
        assert_that(result, is_('$\\sqrt{x}$'))

        result = self.translateOpenMath('macromath4.xml')
        assert_that(result, is_('$\\sqrt[3]{64}$'))

    def test_symbol(self):
        result = self.translateOpenMath('symbol.xml')
        assert_that(result, is_('$\\frac{25 * \\pi}{2}$'))

    def test_complex(self):
        result = self.translateOpenMath('complexmath.xml')
        assert_that(result, is_('$\\sqrt[3]{31} + \\frac{q^{2} - 1}{q - 1}$'))

    def test_float(self):
        result = self.translateOpenMath('floatmath.xml')
        assert_that(result, is_('$40000.00 + 3$'))
    
    def test_no_omobj(self):
        result = self.translator.translate('<noombbj xmlns="http://www.openmath.org/OpenMath" />')
        assert_that(result, is_('\\Unknown{noombbj}'))

    def test_no_oma(self):
        content = """
            <OMOBJ xmlns="http://www.openmath.org/OpenMath" version="2.0" cdbase="http://www.openmath.org/cd">
            </OMOBJ>
        """
        result = self.translator.translate(content)
        assert_that(result, is_(none()))
        
        content = """
            <OMOBJ xmlns="http://www.openmath.org/OpenMath" version="2.0" cdbase="http://www.openmath.org/cd">
                <OMI>3</OMI>
            </OMOBJ>
        """
        result = self.translator.translate(content)
        assert_that(result, is_('$3$'))
        
        content = """
            <OMOBJ xmlns="http://www.openmath.org/OpenMath" version="2.0" cdbase="http://www.openmath.org/cd">
                <NoOBJ />
            </OMOBJ>
        """
        result = self.translator.translate(content)
        assert_that(result, is_('\\Unknown{NoOBJ}'))

    def test_unknown_content(self):
        content = """
            <OMOBJ xmlns="http://www.openmath.org/OpenMath" version="2.0" cdbase="http://www.openmath.org/cd">
                <OMA>
                    <OMS cd="arith1" name="xxxx"/>
                </OMA>
            </OMOBJ>
        """
        result = self.translator.translate(content)
        assert_that(result, is_('$\\Unknowncontent{arith1}{xxxx}$'))
        
    def test_no_operator(self):
        content = """
            <OMOBJ xmlns="http://www.openmath.org/OpenMath" version="2.0" cdbase="http://www.openmath.org/cd">
                <OMA>
                    <NoOp />
                    <NoOp />
                </OMA>
            </OMOBJ>
        """
        result = self.translator.translate(content)
        assert_that(result, is_('$\\NoOperatorFound{OMA}$'))

    def translateOpenMath(self, file_name):
        path = os.path.join(os.path.dirname(__file__), 'openmath', file_name)
        with open(path) as xml:
            result = self.translator.translate(xml.read())
        return result
