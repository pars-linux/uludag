.. _pisitools:

Pisitools
=========

:Author: Semen Cirit
:Date: |today|
:Version: 0.1


dobin
-----

::

    dobin(sourceFile, destinationDirectory = '/usr/bin')

Moves the sourceFile' in work directory to destinationDirectory. The default
value for destinationDirectory is /usr/bin.

Examples::

    pisitools.dobin("sed/sed", "/bin")
    pisitools.dobin("zipsplit")


dodir
-----

::

    dodir(destinationDirectory)

Creates a directory tree in the install path.

Examples::

    pisitools.dodir("/usr/include/awk")
    pisitools.dodir("/usr/" + get.HOST() + "/include")
    pisitools.dodir("/usr/share/doc/%s/examples" % get.srcTAG())


dodoc
-----

::

    dodoc(sourceFiles)

Copies the sourceFiles into /usr/share/doc/PACKAGE under the install directory.

Example::

    pisitools.dodoc("README")
    pisitools.dodoc("*.html")
    pisitools.dodoc("FAQ", "README", "ChangeLog.*", "algorithm.txt") 


doexe
-----

::

    doexe(sourceFile, destinationDirectory)

Copies the executable source file from work directory to destination directory
under the install directory.

Example::

    pisitools.doexe("extras/scsi-devfs.sh", "/etc/udev/scripts/")
    pisitools.doexe("etc/hotplug/*.rc", "/etc/hotplug/")


dohtml
------

::

    dohtml(sourceFiles)

Copies the given html files into /usr/share/doc/PACKAGE/html under the install
directory.

The allowed extentions for html files are ".png, .gif, .html, .htm, .jpg, .css,
.js"

Examples::

    pisitools.dohtml("index.html")
    pisitools.dohtml("doc/*") 

doinfo
------

::

    doinfo(sourceFiles)

Copies the given info files into /usr/share/info under the install directory.

Examples::

    pisitools.doinfo("*.info")


dolib
-----

::

    dolib(sourceFile, destinationDirectory = '/usr/lib')

Copies the library files into /usr/lib under the install directory.

Examples::

    pisitools.dolib("libz.a")
    pisitools.dolib("lib/libpci.a")
    pisitools.dolib("libbz2.so.1.0.2", "/lib") 


dolib_a
-------

::

    dolib_a(sourceFile, destinationDirectory = '/usr/lib')

Copies the static library files into /usr/lib with permission 0644 under the
install directory.

Example::

    pisitools.dolib_a("lib/libpci.a")
    pisitools.dolib_a("libdb1.a") 


dolib_so
--------

::

    dolib_so(sourceFile, destinationDirectory = '/usr/lib')

Copies the shared library files into /usr/lib with permission 0755 under the
install directory.

Example::

    pisitools.dolib_so("libdb1.so.2") 


doman
-----

::

    doman(sourceFiles)

Copies the  manual files into /usr/share/man/ under the install directory.

Examples::

    pisitools.doman("logrotate.8")
    pisitools.doman("doc/bash.1", "doc/bashbug.1", "doc/builtins.1", "doc/rbash.1")
    pisitools.doman("*.[1-8]") 


domo
----

::

    domo(sourceFile, locale, destinationFile )

Makes a mo destinationFile for locale language from the sourceFile po file in
/usr/share/locale/LOCALE/LC_MESSAGES.

Example::

    pisitools.domo("po/tr.po", "tr", "pam_login.mo") 


domove
------

::

    domove(sourceFile, destination, destinationFile)

Moves the source file to destination directory under install directory.

Example::

    pisitools.domove("/usr/bin/passwd", "/bin/")
    pisitools.domove("/usr/bin/yacc", "/usr/bin", "yacc.bison")
    pisitools.domove("/usr/docs/", "/usr/share/doc/%s/html/" % get.srcTAG()) 


dosed
-----

::

    dosed(sourceFile, findPattern, replacePattern)

Replaces the findPattern to replacePattern in sourceFile via sed.

Examples::

    pisitools.dosed("gcc/version.c", "<URL:http://gcc.gnu.org/bugs.html>" , "<URL:http://bugs.uludag.org.tr>")
    pisitools.dosed("sshd_config", "(?m)(#UsePAM ).*", r"UsePAM yes")
    pisitools.dosed("unix/Makefile", "-O3", get.CFLAGS())
    pisitools.dosed("Make.Rules", "HAVE_NDBM_H=yes", "HAVE_NDBM_H=no")
    pisitools.dosed("Makefile.def", "CC=cc", "CC=%s" % get.CC())
    pisitools.dosed("automake.texi", "(?m)(@setfilename.*)automake", r"\1automake1.7") 


dosbin
------

::

    dosbin(sourceFile, destinationDirectory = '/usr/sbin')

Moves the sourceFile in work directory to destinationDirectory under install
directory. The default value for destinationDirectory is /usr/sbin.

Examples::

    pisitools.dosbin("traceroute6")
    pisitools.dosbin("extras/scsi_id/scsi_id", "/sbin") 


dosym
-----

::

    dosym(sourceFile, destinationFile)

Creates a symbolic link from the sourceFile to destinationFile.

Examples::

    pisitools.dosym("gzip", "/bin/gunzip")
    pisitools.dosym("libdb1.so.2", "/usr/lib/libdb.so.2")
    pisitools.dosym("../bin/lsmod", "/sbin/lsmod")
    pisitools.dosym("/usr/X11R6/include/X11", "/usr/include/X11") 


insinto
-------

::

    insinto (destinationDirectory, sourceFile,  destinationFile = '', sym = True)

Copies a sourceFile into destinationDirectory as a destinationFile with same
uid/guid/permissions'. destinationFile parameter is optional and it can be used
when sourceFile name need to be changed.

Examples::

    pisitools.insinto("/opt/rar/bin", "rar")
    pisitools.insinto("/etc/", "doc/nanorc.sample", "nanorc")
    pisitools.insinto("/etc/hotplug", "etc/hotplug/*map") 

newdoc
------

::

    newdoc(sourceFile, destinationFile)

Copies the sourceFile to /usr/share/doc/PACKAGE/ under installation directory.

Examples::

    pisitools.newdoc("extras/volume_id/README", "README_volume_id")
    pisitools.newdoc("gprof/ChangeLog.linux", "gprof/ChangeLog.linux")
    pisitools.newdoc("bfd/PORTING", "bfd/PORTING") 


newman
------

::

    newman(sourceFile, destinationFile)

Copies the sourceFile to /usr/share/man/manPREFIX/ with a new name under
installation directory.

Examples::

    pisitools.newman("less.nro", "less.1") 


remove
------

::

    remove(sourceFile)

Deletes the sourceFile under the install directory.

Example::

    pisitools.remove("/usr/lib/libdb_cxx.so")


rename
------

::

    rename(sourceFile, destinationFile)

Renames the sourceFile as destinationFile.

Examples::

    pisitools.rename("/usr/bin/bash", "bash.old") 

The new file would be existed in /usr/bin/bash.old.

removeDir
---------

::

    removeDir(destinationDirectory)

Deletes the 'destinationDirectory and all files inside.

Examples::

      pisitools.removeDir("/usr/lib")


