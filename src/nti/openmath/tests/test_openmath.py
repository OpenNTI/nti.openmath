#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
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

	def translateOpenMath(self, file_name):
		xml = open(os.path.join( os.path.dirname(__file__), 'openmath', file_name))
		try:
			result = self.translator.translate(xml.read())
		finally:
			xml.close()
		return result
