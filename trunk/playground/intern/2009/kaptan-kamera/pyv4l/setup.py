# setup.py
from distutils.core import setup, Extension

setup(
    name="pyv4l",
    version="0.5.0",
    description="V4L Python Extension",
    author="Michael Dove",
    author_email="pythondeveloper@optushome.com.au",
    url="http://members.optushome.com.au/pythondeveloper/programming/python/pyv4l/",
    license="GPL",
    ext_modules=[Extension("v4l", ["v4l.c"], library_dirs=["/usr/X11R6/lib"], libraries=["X11", "Xxf86dga", "Xext", "v4l1"], extra_compile_args=["-g3", "-ggdb"])]
    )

