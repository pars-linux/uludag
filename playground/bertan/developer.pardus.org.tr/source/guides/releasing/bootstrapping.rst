.. _bootstrapping:

Bootstrapping
~~~~~~~~~~~~~

:Author: Onur Küçük, Neslihan Şirin
:Date: |today|
:Version: 1.0

This document contains the bootstrap steps and methods carried out on the 32/64-bit processor architecture for Pardus releases. Some compilers and libraries such as gcc and glibc requires themselves. To compile and generate executables of these compilers and libraries we had to use older version of these tools with special parameters.

Bootstrap Steps
===============

- Gaining information about basic concepts and tools to be used for bootstrap process
- Compiling binutils, glibc and gcc software, which is the main core of the bootstrap system
- Installing main software on the new system necessary for using the newly-developed system

Preliminary Preparation – Basic Concepts and Tools Used
=======================================================

Before starting the bootstrap process, it is necessary to remember the basic concepts. The starting can be made with C language compiling model. The compilin process starts with the preprocessor. Preprocessor is the program which produces the output data (it produced) for another program. Preprocessor handles directives for source file #include, macro definition (#define) ve conditional inclusion (#if). After that, the assembly code produced by compiler are transmitted to the assembler, and the object codes created by the assembler and libraries to be used for functioning of the program are given to the linker. As a consequence of such linking, the executable code is obtained. 

To mention briefly the tools used for realizing the referred compiling model.

binutils
--------

Contains commands like as, ld, nm, objdump, ar, ranlib for compiling assembly code to the machine language, and for linking and manipulating the binary object files.

**ar**
  The GNU ar program creates, modifies, and extracts from archives.

**as**
  The portable GNU assembler. GNU as is really a family of assemblers. If you use (or have used) the GNU assembler on one architecture, you should find a fairly similar environment when you use it on another architecture.

**ld**
   ld combines a number of object and archive files, relocates their data and ties up symbol references. Usually the last step in compiling a program is to run ld.

**nm**
  List symbols from object files.

**objdump**
  Display information from object files.

**ranlib**
  Generates an index to the contents of an archive and stores it in the archive. The index lists each symbol defined by a member of an archive that is a relocatable object file.

**pax-utils**
  The tool which can carry out various checks including security on ELF32/64 (executable and linkable format) files.

**strace**
  The tool which indicates the system calls related with a process. A debugger tool which shows system calls received or called by this process, parameters appointed to these calls and returning values.



C Compiler Flags (CFLAGS)
^^^^^^^^^^^^^^^^^^^^^^^^^
The flags used by GCC and GNU Library C to manage some properties of the system during compiling transaction.

**-D_FORTIFY_SOURCE=2**
  Used in case of security gap especially in places where string is used.
**-O2**
  It opens the optimizations which do not exaggerate the software size and do not prevent debugging. It is better than -O2 –O, and generally as secured as it. Default optimization level for Pardus 2009 packets is -O2 as well.
**-fomit-frame-pointer**
  It ensures gcc to skip frame pointer maintenance, which, in turn, helps the code be smaller and faster. Also it empties a register for following uses. 
**-fstack-protector**
  It changes position of the variables on the bulk, and prevents the variables used as buffer store from affecting the other variables in case of overrunning. It places a protection variable onto which a random value is appointed before function returning address. Upon completion of the function, this variable is checked to understand whether there is overrunning or not. Running of the program is stopped if there is a change. In this case, misuse of the memory overrunning errors which change the function returning address.
**-march=<architecture>**
  It ensures gcc to do optimization for certain architecture. If you design software for yourself only, you can specify the architecture on which the software is to work and use all properties of such architecture. 
**-mtune=<architecture>**
  The –mcpu in former versions of gcc is similar to -march flag and has the same options. Besides, -mtune does not distort conformity with former architectures. Desired results can be achieved by means of using -mtune and -march flags together.
**-pipe**
  It prevents gcc from generating temporary files while compiling. Instead, improvement at the time of compiling by directly transferring data to another function.  



Linker Flags (LDFLAGS)
^^^^^^^^^^^^^^^^^^^^^^

The flags used by the linker for managing some properties of the system.

**-Bsymbolic-functions**
  When creating a shared library, bind references to global function symbols to the definition within the shared library, if any. This option is only meaningful on ELF platforms which support shared libraries.
**-Wl,--hash-style=gnu**
  Set the type of linker's hash table(s). Style can be either "sysv" for classic ELF ".hash" section, "gnu" for new style GNU ".gnu.hash" section or "both" for both the classic ELF ".hash" and new style GNU ".gnu.hash" hash tables.  The default is "sysv".
**--as-needed**
  The --as-needed flag is passed to the GNU linker. The flag tells the linker to link in the produced binary only the libraries containing symbols actually used by the binary itself. This binary can be either a final executable or another library.
**--sort-common**
  This option tells ld to sort the common symbols by size when it places them in the appropriate output sections. First come all the one byte symbols, then all the two bytes, then all the four bytes, and then everything else. This is to prevent gaps between symbols due to alignment constraints.
**-Wl,-z,relro**
  Provides a read-only relocation table area in the final ELF. This option paves the way for using -z now which forces all relocations to be resolved at run-time (which would cause some additional initial load delay), providing an even higher level of protection to the relocation table -- it could then be entirely read-only which can be used to further harden long-running programs like daemons.
**-no-unneeded**
  Using --no-unneeded during build handles all cases.

Preparing Environment Necessary for Compiling the System
========================================================

At this stage; as request was made for compiling another system on the existing system, potential risks such as permanent damage on the existing system to be made by the bootstrap transaction must be considered and a suitable method must be selected. Of all methods, the most suitable one- though relatively a long process – is to make an isolated part on the existing system and to conduct transactions on this environment. For this, firstly a new user is created. The new user is named *bootstrap* on this application; almost all of the subsequent transactions will be conducted in the user name bootstrap. First of all; directories are created for conducting transactions in the bootstrap area and using the new system as root directory.
::

     bootstrap@pardus ~ $ mkdir -p newroot/sysroot

In the bootstrap to contain root codes of the programs to be compiled, a sources directory and a src directory is created under newroot to compile programs.
::

    bootstrap@pardus ~ $ mkdir sources
    bootstrap@pardus ~/newroot $ mkdir src

After that, we can save the variables to be frequently used including subdirectory and path in the .bashrc file, and use the shortcuts valid for that crust.
::

    bootstrap@pardus ~ $ vi .bashrc

Following lines are included in the .bashrc file:
::

    export TARGET=x86_64-pc-linux-gnu
    export CROSS_COMPILE=${TARGET}-
    export PREFIX=/home/bootstrap/newroot
    export SYSROOT=${PREFIX}/sysroot
    export PATH=${PREFIX}/bin:${PREFIX}/sysroot/bin:${PATH}
    export MYDESTDIR=/home/bootstrap/newroot/installdir
    export CC=${CROSS_COMPILE}gcc
    export AR=${CROSS_COMPILE}ar
    export RANLIB=${CROSS_COMPILE}ranlib
    export AS=${CROSS_COMPILE}as
    export LD=${CROSS_COMPILE}ld

TARGET refers to the architecture of the new system to be compiled, CROSS_COMPILE to the target system tools to be compiled, PREFIX to the path to conduct transactions, SYSROOT to root directory of the new system, PATH to paths regarding the new system, MYDESTDIR to the directory to include the programs to be compiled after compiling basic tools; CC, AR, RANLIB, AS and LD to the system tools required to be used during compiling.

Compiling Binutils, GCC and GlibC
=================================

GNU binutils
-------------

The source code of the binutils to be used for the new system is located into the sources directory, and opens into the src directory under the newroot.
::

    cd ${PREFIX}/src
    tar xvf binutils-xxx
    mkdir -p build/binutils-stage1
    cd build/binutils-stage1

So far, source codes have been opened in the src, the build directory to be used for the compiling and binutils-stage1 directory to host binutils under the former have been created. The next step is for compiling binutils.
::

    ../../binutils-xxx/configure --prefix=${PREFIX} --target=${TARGET} --with-sysroot=${SYSROOT}
    make
    make install

In the steps above; the binutils source codes opening into src were configured with the configuration settings, relatively. According to the additional parameters given here, the variables formerly added to the .bashrc file were used. Therefore; binutils was established under the target architecture and root directory of the new system in the path given. 

**After compiling binutils, it is necessary to compile gcc; but the former gcc/glibc version is different from the new gcc/glibc to be compiled. Basic programs must be parallel with each other. It is understood that interdependence to arise between the two programs from incompliant versions will be a problem. Firstly, glibc was compiled as an intermediate step as a solution for this problem.**


GNU Library C
-------------

For the glibc to be compiled for the new system, there is kernel-headers (heading files used by glibc and the other user space applications) dependence. Therefore; firstly, the pisi packet received by means of
::

    pisi fetch kernel-headers


opens into the newroot/sysroot by means of the following order.
::

   unpisi kernel-headers-xxx.pisi

Then, it may come to the steps necessary for compiling glibc. Source code of the glibc to be used for the new system is located into the sources directory, and it opens into the src directory under the newroot.
::

    cd ${PREFIX}/src
    tar xvf glibc-xxx
    mkdir -p build/glibc-stage1
    cd build/glibc-stage1

Source codes open into the src; in this way, glibc-stage1 directory is created under the build to be used for compiling.
::

    ../../glibc-xxx/configure --prefix=usr  --target=${TARGET} --without-__thread --enable-add-ons=linuxthreads --with-headers=${SYSROOT}/usr/include
    make
    make install_root=${SYSROOT} install

glibc is configured and installed by using the orders above.

*As a point of consideration; as the existing host architecture is the same as the target architecture, the parameters above are sufficient.. If any other architecture weretargeted, the configuration order would be as follows.*
::

     BUILD_CC=gcc CC=${CROSS_COMPILE}gcc AR=${CROSS_COMPILE}ar RANLIB=${CROSS_COMPILE}ranlib AS=${CROSS_COMPILE}as LD=${CROSS_COMPILE}ld ../../glibc-xxx/configure --prefix=usr  --target=${TARGET} --without-__thread --enable-add-ons=linuxthreads --with-headers=${SYSROOT}/usr/include

GCC
---

The source code of the gcc to be used for the new system is located into the sources directory, and opens into the src directory under the newroot.
::

    cd ${PREFIX}/src
    tar xvf gcc-xxx
    mkdir -p build/gcc-stage1
    cd build/gcc-stage1

Source codes open into the src; in this way, gcc-stage1 directory is created under the build to be used for compiling.
::

    ../../gcc-xxx/configure --prefix=${PREFIX} --target=${TARGET} --enable-languages=c  --with-build-sysroot=/ --with-sysroot=${SYSROOT} --with-headers=${SYSROOT}
    make
    make install

gcc is configured and installed by using the orders above.

After the compilation of binutils, gcc and glibc the major part of the bootstrapping is completed.

Compiling of zlib, ncurses and bash
===================================

The last step consist of compiling of zlib, ncurses and bash tools for using the new system. This process needs add to new data in the .bashrc file.
::

    alias autotools.configure="./configure --prefix=/usr --mandir=/usr/share/man --infodir=/usr/share/info"
    alias autotools.install="make prefix=$MYDESTDIR/usr infodir=$MYDESTDIR/usr/share/info mandir=$MYDESTDIR/usr/share/man install"

**zlib**
  General purpose data compression / decompression library.

The zlib package in the Pardus package repository
::

    pisi build --unpack http://svn.pardus.org.tr/pardus/2009/devel/system/base/zlib/pspec.xml

copy zlib* directory which under the /var/pisi/zlib-xxx/work/ directory and then going to the directory. Execute the intructions step by step in the actions.pyfile which is a part of the zlib package.
::

    mkdir m4
    autoreconf -fi
    autotools.configure --disable-static
    make
    autotools.install

In the steps above, required to using with *pisitools* but, the new system does not include the pisitools. Ongoing steps will realize in newroot/installdir. (xxx means version number)
::

    mv usr/lib/libz* lib
    ln -s lib/libz.so.xxx  usr/lib/libz.so.xxx
    ln -s libz.so.xxx  usr/lib/libz.so.1
    ln -s libz.so.1  usr/lib/libz.so
    cp zconf.h  usr/include
    cp zlib.h  usr/include
    cp zutil.h  usr/include

after the steps above, revome all ".la" files and then copy content of the installdir/ to under the newroot/sysroot directory. zlib is configured and installed by using the orders above.

**ncurses**
  A programming library providing an API, allowing the programmer to write text user interfaces in a terminal-independent manner.

The ncurses package in the Pardus package repository
::

    pisi build --unpack http://svn.pardus.org.tr/pardus/2009/devel/system/base/ncurses/pspec.xml

copy ncurses* directory which under the /var/pisi/ncurses-xxx/work/ directory and then going to the directory. Execute the intructions step by step in the actions.py file which is a part of the ncurses package.
::

    autotools.configure --without-debug --without-profile --disable-rpath --enable-const \
                        --enable-largefile --enable-widec --with-terminfo-dirs='/etc/terminfo:/usr/share/terminfo'\
                        --disable-termcap --with-shared --with-rcs-ids --with-chtype='long'\
                        --with-mmask-t='long'  --without-ada --enable-symlinks··

    make
    make DESTDIR=$MYDESTDIR install

for the ongoing steps under the newroot/installdir
::

    rm -rf usr/lib/*.a
    ln -s usr/lib/*w.* usr/lib/*.*

after the steps above, remove all ".la" files. Another ncurses package unpisi in any dummy directory and then copy consist of /etc directory newroot/sysroot. zlib is configured and installed by using the orders above.

**bash**
  Bash  is  an  sh-compatible command language interpreter that executes commands read from the standard input or from a file.

The ncurses package in the Pardus package repository
::

    pisi build --unpack http://svn.pardus.org.tr/pardus/2009/devel/system/base/bash/pspec.xml

copy bash* directory which under the /var/pisi/bash-xxx/work/ directory and then going to the directory. Execute the intructions step by step in the actions.py file which is a part of the bash package.
::

    autoconf
    autotools.configure --without-installed-readline --disable-profiling --without-gnu-malloc --with-curses
    make
    autotools.install

for the ongoing steps under the newroot/installdir
::

    mv usr/bin/bash  bin/
    ln -s bin/bash  bin/sh
    ln -s bin/bash  bin/rbash

bash is configured and installed by using the orders above.

After the compilation of zlib, ncurses and bash the bootstrapping is completed.


Resources
=========

- Linux man pages
- `Building a GNU/Linux ARM Toolchain <http://frank.harvard.edu/~coldwell/toolchain/>`_
- `CFLAGS <http://en.gentoo-wiki.com/wiki/CFLAGS>`_
- `Compilation Optimization Guide <http://www.gentoo.org/doc/en/gcc-optimization.xml>`_
- `D_FORTIFY_SOURCE=2 <https://wiki.ubuntu.com/CompilerFlags#-D_FORTIFY_SOURCE=2>`_
- `Options for Code Generation Conventions <http://gcc.gnu.org/onlinedocs/gcc/Code-Gen-Options.html>`_
