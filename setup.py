import pathlib

import setuptools

from setuptools.command.build_ext import build_ext as _build_ext


NAME = "reverse-geocoder-whl".replace("-", "_")
PY_SRC = NAME.replace("-", "_")
EXT_SRC = pathlib.Path("c++") / "lib"

EXT_SOURCE_FILES = [
    str(p)
    for ext in ("c", "cpp", "h", "hpp")
    for p in EXT_SRC.glob(f"**/*.{ext}")
]

ext_modules = [
    setuptools.Extension(
        name=NAME,
        # Sort input source files to ensure bit-for-bit reproducible builds
        sources=sorted(EXT_SOURCE_FILES),
        include_dirs=[],
        library_dirs=[],
        libraries=[],
        language="c++",
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
    name=NAME,
    author_email='ajay.thampi@gmail.com',
    url='https://github.com/TalAmuyal/reverse-geocoder-whl',
    packages=[NAME],
    package_dir={'reverse_geocoder_whl': './reverse_geocoder_whl'},
    package_data={'reverse_geocoder_whl': ['rg_cities1000.csv']},
    cmdclass={'build_ext': build_ext},
)
