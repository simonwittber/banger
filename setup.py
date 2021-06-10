from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules = [
    Extension(
        r'clock',
        [r'clock/clock.pyx']
    ),
]

setup(
    name='clock',
    ext_modules=cythonize(ext_modules),
)
