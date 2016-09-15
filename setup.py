# setup.py
import os
from distutils.core import setup
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

# Handling scipy dependency. See: http://stackoverflow.com/a/38276716
class build_ext(_build_ext):
    def finalize_options(self):
      _build_ext.finalize_options(self)
      # Prevent numpy from thinking it is still in its setup process:
      __builtins__.__NUMPY_SETUP__ = False
      import numpy
      self.include_dirs.append(numpy.get_include())

setup(name='reverse_geocoder',
      version='1.5.1',
      author='Ajay Thampi',
      author_email='ajay.thampi@gmail.com',
      url='https://github.com/thampiman/reverse-geocoder',
      packages=['reverse_geocoder'],
      package_dir={'reverse_geocoder': './reverse_geocoder'},
      package_data={'reverse_geocoder': ['rg_cities1000.csv']},
      setup_requires=['numpy>=1.11.0',],
      cmdclass={'build_ext': build_ext},
      install_requires=['numpy>=1.11.0', 'scipy>=0.17.1',],
      description='Fast, offline reverse geocoder',
      license='lgpl',
      long_description=read('README.txt'))
