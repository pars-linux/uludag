.. _shelltools:

Shelltools
==========

:Author: Semen Cirit
:Date: |today|
:Version: 0.1


can_access_file
---------------

::

    can_access_file(sourceFilePath)

Checks if the sourceFile is accessible.

Examples::

    shelltools.can_access_file("/usr/share/terminfo/%s" % termfile) 
    shelltools.can_access_file("%s/texk/%s/%s" % (get.curDIR(), dir, file))


can_access_directory
--------------------

::

    can_access_directory(destinationDirectory)

Checks if the directory is accessible and test readability, writability and
executablility of the directory.

Examples::

    shelltools.can_access_directory("%s/texk/%s" % (get.curDIR(), dir))

makedirs
--------

::

    makedirs(destinationDirectory)

Creates the destinationDirectory.

Examples::

    shelltools.makedirs("%s/build" % get.workDIR())
    shelltools.makedirs("%s/build-default-i686-pc-linux-gnu-nptl" % get.workDIR())


echo
----

::

    echo(destionationFile, content)

Append the given content to the given file.

Examples::

    shelltools.echo('conf-cc',"%s %s -O1 -fomit-frame-pointer -malign-double -fPIC -DPIC" % (get.CC(),get.CFLAGS()))
    shelltools.echo("driver/ghc/Makefile","GHC_CFLAGS = %s -Wa,--noexecstack"  % get.CFLAGS())
    shelltools.echo(CONFIGFILE, "CONFIG_READLINE=y")
    shelltools.echo("%s/etc/pardus-release" % get.installDIR(), "Pardus 2009.1 Anthropoides virgo")

chmod
-----

::

    chmod(sourceFilePath, mode = 0755)

Changes permissions of sourceFile. The default mode parameter is "0755".

Examples::

    shelltools.chmod("config/config.sub")
    shelltools.chmod(get.installDIR() + "/lib/libz.so.*")
    shelltools.chmod("%s/usr/lib/misc/pt_chown" % get.installDIR(), 4711)
    shelltools.chmod(get.installDIR() + "/etc/ssh/sshd_config", 0600) 

chown
-----

::

    chown(filePath, uid = 'root', gid = 'root')

Changes the owner and group id of filePath with given  uid and gid.

Examples::

     shelltools.chown("%s/var/run/openct" % get.installDIR(), gid="pnp")
     shelltools.chown("%s/var/run/openct" % get.installDIR(), gid="pnp")
     shelltools.chown("%s/var/run/memcached" % get.installDIR(), "memcached", "memcached")

sym
---

::

    sym(sourceFile, destinationFile)

Crates symbolic link.

Examples::

    shelltools.sym("/usr/share/fonts/Type1/c059013l.pfb", "%s/usr/share/pokerth/data/fonts/c059013l.pfb" % get.installDIR())
    shelltools.sym("libcompface.so", "libcompface.so.1")
    shelltools.sym("config/configure.in", "configure.in")

unlink
------

::

    unlink(sourceFile)

Deletes the sourceFile.

Examples::

    shelltools.unlink(get.workDIR() + '/' + get.srcDIR() + "/missing") 
    shelltools.unlink("%s/%s/doc/auctex.info" % (get.workDIR(), get.srcDIR()))
    shelltools.unlink("config.sh")


unlinkDir
---------

::

    unlinkDir(sourceDirectory)

Deletes the sourceDirectory and all subdirectories.

Examples::

    shelltools.unlinkDir(get.workDIR() + "/tmpbuild") 
    shelltools.unlinkDir("%s/e2fsprogs-%s/tests/f_ext_journal/" % (get.workDIR(), get.srcVERSION()))


move
----

::

    move(source, destination)

Recursively moves a "source" file or directory to "destination.

Examples::

    shelltools.move("ac-wrapper.sh", "%s/usr/lib/misc/" % get.installDIR())
    shelltools.move("proc/*.h", "%s/usr/include/proc/" % get.installDIR())
    shelltools.move("x11-ssh-askpass.man", "x11-ssh-askpass.1")
    shelltools.move("tmp/*", ".")

copy
----

::

    copy(source, destination)

Recursively copies a "source" file or directory to "destination.

Examples::

    shelltools.copy("Makefile.pre.in", "%s/usr/lib/python2.3/config/" % get.installDIR())
    shelltools.copy("scripts/*", "%s/usr/bin/" % get.installDIR()) 


copytree
--------

::

    copytree(source, destination, sym=True)

Recursively copy an entire directory tree rooted at source.

Example::

    shelltools.copytree("data/library/blpython/widgets", "%s/usr/share/cel-1.3/data/library/blpython/" % get.installDIR())
    shelltools.copytree("include/asm-generic/", "%s/usr/include/asm-generic/" % get.installDIR())


touch
-----

::

    touch(sourceFilePath)

Changes the access time of the file(s), or creates it if it is not exist.

Examples::

    shelltools.touch(get.workDIR() + "aclocal.m4")
    shelltools.touch("gcc/c-gperf.h")
    shelltools.touch("man/*.1")

cd
--

::

    cd(directoryName)

Changes the current working directory to directoryName.

Examples::

    shelltools.cd("%s/build-default-i686-pc-linux-gnu-nptl" % get.workDIR())
    shelltools.cd("../")


ls
--

::

    ls(source)

Returns a list of all files and directories in the source directory.

Examples::

    shelltools.ls("*.tex")
    shelltools.ls(get.installDIR() + "/lib/libncursesw.so*")
    shelltools.ls("*-*")
    shelltools.ls(".")


export
------

::

    export(key, value)

Sets the environment variable value for key.

Examples::

    shelltools.export("CFLAGS", cflags)
    shelltools.export("CXXFLAGS", "%s -DPTYMODE=0620 -DPTYGROUP=5 -DUSE_PAM" % get.CXXFLAGS())
    shelltools.export("LDFLAGS", "%s -pie -Wl,-z,relro,-z,now"  % get.LDFLAGS())


system
------

::

    system(command)

Executes the command in the system shell.

Examples::

    shelltools.system("texi2dvi -q -c --language=latex ./glossaries.dtx")
    shelltools.system("cc -o bbox bbox.c")
    shelltools.system("./update-pciids.sh &> /dev/null") 


isLink
------

::

    isLink(sourceFilePath)

Returns "True" if the file refers to a symbolic link.

Examples::

    shelltools.isLink(get.installDIR() + '/maybe/link')

isFile
------

::

    isFile(sourceFilePath)

Returns "True" if the file is an existing regular file.

Examples::

    shelltools.isFile("alsaaudio.o")
    shelltools.isFile("%s/etc/ld.so.cache" % get.installDIR())
    shelltools.isFile("configure")

isDirectory
-----------

::

    isDirectory(sourceDirectoryPath)

Returns True if the directory is an existing directory.

Examples::

    shelltools.isDirectory("%s/usr/share" % get.installDIR())
    shelltools.isDirectory("install")

isEmpty
-------

::

    isEmpty(path)

Returns True if the given path is an empty file or directory.

Examples::

    shelltools.isEmpty("%s/usr/share" % get.installDIR())
    shelltools.isEmpty("install")

realPath
--------

::

    realPath(sourceFilePath)

Returns the canonical path of the specified filename, eliminating any symbolic
links encountered in the path

Examples::

    shelltools.realPath(get.installDIR() + link)


baseName
--------

::

    baseName(sourceFilePath)

Returns the base pathname of given file.

Example::

    shelltools.baseName("%s/etc/ld.so.cache" % get.installDIR())


dirName
-------

::

    dirName(sourceFilePath)

Returns the directory of the given file.

Example::

    HAL_FDI= "usr/share/hal/fdi/information/20thirdparty/10-camera-libgphoto2.fdi"
    shelltools.dirName(HAL_FDI)



