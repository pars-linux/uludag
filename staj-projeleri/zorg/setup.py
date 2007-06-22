#-*- coding: utf-8 -*-

from distutils.core import setup, Extension
import zorg


setup(name="zorg",
      version=zorg.versionString(),
      description="Python Modules for zorg",
      long_description="Python Modules for zorg.",
      license="GNU GPL2",
      author="Fatih Aşıcı",
      author_email="fatih.asici@gmail.com",
      url="http://www.pardus.org.tr/",
      packages = ['zorg'],
      ext_modules = [Extension("zorg.ddc",
                               sources=["zorg/ddc.c",
                                        "zorg/vbe.c",
                                        "zorg/vesamode.c"],
                               libraries=["x86"])]
      )
