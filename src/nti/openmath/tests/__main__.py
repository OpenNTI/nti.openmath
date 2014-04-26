#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

import os

from unittest import TextTestRunner
from unittest import defaultTestLoader

def runner(path, pattern="*.py"):
	suite = defaultTestLoader.discover(path, pattern)
	try:
		runner = TextTestRunner(verbosity=3)
		for test in suite:
			runner.run(test)
	finally:
		pass

def main():
	dirname = os.path.dirname( __file__ )
	if not dirname:
		dirname = '.'
	runner( dirname )

if __name__ == '__main__':
	main()
