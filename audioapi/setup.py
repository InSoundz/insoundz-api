#!/usr/bin/env python

try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup
import importlib

def version():
  loader = importlib.machinery.SourceFileLoader("src.version", "src/version.py")
  module = loader.load_module()
  return module.__version__

setup(
    name='audioapi',
    version=version(),
    description="InSoundz audioapi client implementation \
        to produce audio enhancement.",
    readme="README.md",
    license_files=('LICENSE',),
    python_requires=">=3.7",
    package_dir={"audioapi": "src"},
    packages=['audioapi'],
    install_requires=[
                        'requests',
                        'wget',
                        'tqdm',
                        'halo',
                        'validators',
    ],
 )
