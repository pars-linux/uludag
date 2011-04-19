.. _scons:

Scons
=====

:Author: Semen Cirit
:Date: |today|
:Version: 0.1


make
----

::

    make(parameters)

Setup the package with scons construction tool.

Examples::

      scons.make("build=release \
                  build_id=%s \
                  install_prefix=/usr \
                  bindir=bin \
                  buildlocale \
                  datadir=share/widelands" % geat.srcVERSION())

install
-------

::

    install(parameters = 'install', prefix = get.installDIR(), argument='prefix')

Install the package with scons construction tool. The default variables for
parameters is install, prefix is get.installDIR(), argument is prefix.

It runs the "'scons %s=%s %s' % (argument, prefix, parameters)" for installation.

Examples::

    scons.install("PREFIX='%s/usr' swig_install install" % get.installDIR())
    scons.install("install prefix=/usr \
                   install_root=%s/usr \
                   qtdir=%s \
                   djconsole=1 \
                   portmidi=0 \
                   optimize=1 \
                   script=1 \
                   shoutcast=1 \
                   tonal=1 \
                   m4a=1 \
                   ladspa=1 \
                   ipod=1" % (get.installDIR(), get.qtDIR()))

