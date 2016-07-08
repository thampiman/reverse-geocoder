# setup.py
import os
from distutils.core import setup

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(name='reverse_geocoder',
	version='1.4',
      author='Ajay Thampi',
      author_email='ajay.thampi@gmail.com',
      url='https://github.com/thampiman/reverse-geocoder',
      packages=['reverse_geocoder'],
      package_dir={'reverse_geocoder': './reverse_geocoder'},
      package_data={'reverse_geocoder': ['rg_cities1000.csv']},
      setup_requires=[
            'numpy',
            'scipy',
      ],
      install_requires=[
            'numpy',
            'scipy',
      ],
      description='Fast, offline reverse geocoder',
      license='lgpl',
      long_description=read('README.txt')
)