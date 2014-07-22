#!/usr/bin/python

""" C extension for faster TimeUUID creation and comparison. """

__version_info__ = (0, 3, 5)
__version__ = '.'.join(map(str, __version_info__))

import os

from distutils.command.sdist import sdist
from distutils.core import setup
from distutils.extension import Extension
from glob import glob

try:
  from Cython.Compiler.Version import version as cython_version
  from Cython.Compiler import Main
  from Cython.Distutils import build_ext
  USE_CYTHON = True
  print 'Building with Cython %s' % cython_version
except ImportError:
  USE_CYTHON = False
  print 'Building without Cython'

EXTENSION = 'pyx' if USE_CYTHON else 'c'
README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
REQUIREMENTS = [
  line.strip() for line in open(os.path.join(os.path.dirname(__file__),
                                             'requirements.txt')).readlines()
  ]

ext_modules = [Extension('timeuuid.timeuuid',
                         sources=['timeuuid/timeuuid.%s' % EXTENSION],
                         libraries=['uuid'])]

setup_kwargs = {}

if USE_CYTHON:
  class Sdist(sdist):
    def __init__(self, *args, **kwargs):
      for src in glob('timeuuid/*.pyx'):
        print src
        Main.compile(glob('timeuuid/*.pyx'),
                     Main.default_options)
      sdist.__init__(self, *args, **kwargs)

  setup_kwargs = {
    'cmdclass': {
      'build_ext': build_ext,
      'sdist': Sdist
      }
    }
else:
  setup_kwargs = {}

setup(
  name='python-timeuuid',
  version=__version__,
  description=('python-timeuuid is a fast Python library for sensibly dealing '
               'with Version 1 UUID (or TimeUUID).'),
  author='GoDaddy',
  author_email='devs@locu.com',
  license='MIT License',
  url='https://github.com/chronology/python-timeuuid/',
  packages = ['timeuuid'],
  ext_modules=ext_modules,
  classifiers=[
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Cython',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    ],
  long_description=README,
  **setup_kwargs
  )
