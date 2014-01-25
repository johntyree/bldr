#!/usr/bin/env python
# coding: utf8

from setuptools import setup

setup(name='bldr',
      version='0.0.1',
      packages=['bldr'],
      scripts=['bin/bldr'],
      author='John Tyree',
      author_email='johntyree@gmail.com',
      license='LGPL3+',
      url='http://github.com/johntyree/bldr',
      description="Helper for building simple programs",
      keywords="build compile",
      long_description=open('README.md').read(),
      classifiers=[
          "Development Status :: 3 - Alpha",
          "License :: OSI Approved :: "
          "GNU Lesser General Public License v3 or later (LGPLv3+)",
          "Topic :: Utilities",  #FIXME
      ],
      )
