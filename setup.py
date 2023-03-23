#! /usr/bin/env python

from setuptools import setup
import sys

print("No unit tests have been created yet.")

dependencies = ['numpy >= 1.21.0',
                'matplotlib >= 3.6.0',]

setup(
  name = 'emberpy',
  packages = ['emberpy'],
  version = '0.1',
  description = 'Emberpy manual calibration tool.',
  author = 'Wesley Fraser',
  author_email = 'westhefras@gmail.com',
  url = 'https://github.com/fraserw/emberpy',
  #download_url = 'https://github.com/fraserw/trippy/tarball/0.1',
  keywords = ['3D Printing', 'ember prototype'],
  license = 'GNU',
  install_requires=dependencies,
  classifiers = [],
  python_requires='>3.6.0',
)
