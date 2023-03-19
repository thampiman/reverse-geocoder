import pathlib

import setuptools

#from setuptools.command.build_ext import build_ext as _build_ext


PYPI_NAME = "reverse-geocoder-whl".replace("-", "_")
MODULE_NAME = PYPI_NAME.replace("-", "_")
EXT_SRC = pathlib.Path("c++") / "lib"

EXT_SOURCE_FILES = [
    str(p)
    for ext in ("c", "cpp")
    for p in EXT_SRC.glob(f"**/*.{ext}")
]

ext_modules = [
    setuptools.Extension(
        name=MODULE_NAME,
        # Sort input source files to ensure bit-for-bit reproducible builds
        sources=sorted(EXT_SOURCE_FILES),
    ),
]


"""
# Handling scipy dependency. See: http://stackoverflow.com/a/38276716
class build_ext(_build_ext):
    def finalize_options(self):
      _build_ext.finalize_options(self)
      # Prevent numpy from thinking it is still in its setup process:
      __builtins__.__NUMPY_SETUP__ = False
      import numpy
      self.include_dirs.append(numpy.get_include())
"""


setuptools.setup(
    name=PYPI_NAME,
    url='https://github.com/TalAmuyal/reverse-geocoder-whl',
    packages=setuptools.find_packages(),
    package_dir={'reverse_geocoder_whl': f"./{MODULE_NAME}"},
    package_data={'reverse_geocoder_whl': ['rg_cities1000.csv']},
    #cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules,
)
