import codecs
from setuptools import setup, find_packages

VERSION = '0.0.0'

entry_points = {
}

TESTS_REQUIRE = [
	'nose',
	'nose-pudb',
	'nose-timer',
	'nose-progressive',
	'nose2[coverage_plugin]',
	'pyhamcrest',
	'nose_traceback_info'
]

setup(
	name = 'nti.openmath',
	version = VERSION,
	author = 'Jason Madden',
	author_email = 'jason@nextthought.com',
	description = "Support for parsing openmath XML",
	long_description = codecs.open('README.rst', encoding='utf-8').read(),
	license = 'Proprietary',
	keywords = 'Math parsing',
	classifiers = [
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: Implementation :: CPython',
	],
	packages=find_packages('src'),
	package_dir={'': 'src'},
	namespace_packages=['nti',],
	tests_require=TESTS_REQUIRE,
	install_requires=[
		'setuptools',
	],
	entry_points=entry_points,
	extras_require={
		'test': TESTS_REQUIRE,
	},
	dependency_links=[
		'git+https://github.com/NextThought/nti.nose_traceback_info.git#egg=nti.nose_traceback_info'
	],
)
