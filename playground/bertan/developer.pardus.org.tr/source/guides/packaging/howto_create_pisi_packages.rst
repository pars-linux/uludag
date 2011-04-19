.. _howto-create-pisi-packages:

How to Create Pisi Packages
===========================

**Last Modified Date:** |today|

:Author: Semen Cirit

:Version: 0.5

Creating Package
----------------

This document is specifically about creating pspec.xml files. In order to see 
basic dynamics of a packaging please see: :ref:`packaging-guidelines`,
:ref:`package-naming`, and :ref:`building-pisi-package`

This document briefly explains different pieces of pspec.xml and explain them specifically.

If you want to make packages and be a Pardus Package Maintainer please follow :ref:`how-to-be-contributor`.

Creating pspec.xml
------------------

You first need to create a pspec.xml file under the package named directory.
 See :ref:`package-naming`.

Creating Empty pspec.xml File
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to create an empty pspec.xml file, you only need to run the below
command under package named directory.

::

    cd package-name
    vi pspec.xml

**This is the empty pspec.xml**

::

    <?xml version="1.0" ?>
    <!DOCTYPE PISI SYSTEM "http://www.pardus.org.tr/projeler/pisi/pisi-spec.dtd">
    <PISI>
        <Source>
        <Name></Name>
        <Homepage>http://</Homepage>
        <Packager>
            <Name></Name>
            <Email></Email>
        </Packager>
        <ExcludeArch></ExcludeArch>
        <License>GPLv2</License>
        <Icon></Icon>
        <IsA></IsA>
        <Summary></Summary>
        <Description></Description>
        <Archive sha1sum="" type="">http://</Archive>
        <BuildDependencies>
            <Dependency></Dependency>
        </BuildDependencies>
        <Patches>
            <Patch level=""></Patch>
        </Patches>
    </Source>

    <Package>
        <Name></Name>
         <BuildType></BuildType>
         <BuildDependencies>
            <Dependency></Dependency>
        </BuildDependencies>
        <RuntimeDependencies>
            <AnyDependency>
                <Dependency></Dependency>
            </AnyDependency>
            <Dependency versionFrom=""></Dependency>
        </RuntimeDependencies>
         <Conflicts>
            <Package versionTo=""></Package>
            <Package releaseTo=""></Package>
        </Conflicts>
        <Replaces>
            <Package></Package>
            <Package></Package>
        </Replaces>
        <Files>
            <Path fileType="config">/etc</Path>
            <Path fileType="executable">/usr/bin</Path>
            <Path fileType="header">/usr/include</Path>
            <Path fileType="library">/usr/lib</Path>
            <Path fileType="localedata">/usr/share/locale</Path>
            <Path fileType="man">/usr/share/man</Path>
            <Path fileType="doc">/usr/share/doc</Path>
            <Path fileType="data">/usr/share</Path>
        </Files>
        <AdditionalFiles>
            <AdditionalFile owner="root" permission="0644" target=""></AdditionalFile>
        </AdditionalFiles>
        <Provides>
            <COMAR script=""></COMAR>
        </Provides>
    </Package>

    <History>
        <Update release="1">
            <Date>YYYY-MM-DD</Date>
            <Version></Version>
            <Comment>First release.</Comment>
            <Requires>
                <Action>reverseDependencyUpdate</Action>
                <Action package="">reverseDependencyUpdate</Action>
                <Action package="">systemRestart</Action>
                <Action package="">serviceRestart</Action>
            </Requires>
            <Name></Name>
            <Email></Email>
        </Update>
    </History>
    </PISI>

**An example pspec.xml file for texlive-core package:**

::

    <?xml version="1.0" ?>
    <!DOCTYPE PISI SYSTEM "http://www.pardus.org.tr/projeler/pisi/pisi-spec.dtd">
    <PISI>
    <Source>
        <Name>texlive-core</Name>
        <Homepage>http://www.tug.org/texlive</Homepage>
        <Packager>
            <Name>Semen Cirit</Name>
            <Email>scirit@pardus.org.tr</Email>
        </Packager>
        <License>GPLv2</License>
        <IsA>data:doc</IsA>
        <Summary>Essential part of TeXLive</Summary>
        <Description>texlive-core is the essential part of TeXLive.</Description>
        <Archive sha1sum="05f3e5557feec0c1e71eaaab3258101a2b7f5d7f" type="tarbz2">http://cekirdek.pardus.org.tr/~semen/dist/texlive/2009/texlive-core-20091107.tar.bz2</Archive>
        <BuildDependencies>
            <Dependency>ed</Dependency>
            <Dependency>fontconfig</Dependency>
            <Dependency>teckit</Dependency>
            <Dependency>poppler</Dependency>
            <Dependency>libXmu</Dependency>
            <Dependency>libXpm</Dependency>
            <Dependency>libXaw</Dependency>
            <Dependency>libXfont</Dependency>
            <Dependency>silgraphite</Dependency>
        </BuildDependencies>
        <Patches>
            <Patch>040_all_texmfdirs.patch</Patch>
            <Patch>020_all_poppler.patch</Patch>
            <Patch>030_all_installedscripts.patch</Patch>
            <Patch>010_all_icu_CVE-2007-4770.patch</Patch>
            <Patch>sedscript.patch</Patch>
            <Patch>sedscript2.patch</Patch>
            <Patch>sedscript3.patch</Patch>
        </Patches>
    </Source>

    <Package>
        <Name>texlive-core</Name>
        <RuntimeDependencies>
            <Dependency>fontconfig</Dependency>
            <Dependency>teckit</Dependency>
            <Dependency>poppler</Dependency>
            <Dependency>silgraphite</Dependency>
        </RuntimeDependencies>
        <Replaces>
            <Package>tetex</Package>
            <Package>tetex-texmf</Package>
            <Package>tetex-extra</Package>
        </Replaces>
        <Files>
            <Path fileType="config">/etc</Path>
            <Path fileType="executable">/usr/bin</Path>
            <Path fileType="header">/usr/include</Path>
            <Path fileType="library">/usr/lib</Path>
            <Path fileType="localedata">/usr/share/locale</Path>
            <Path fileType="man">/usr/share/man</Path>
            <Path fileType="doc">/usr/share/doc</Path>
            <Path fileType="data">/usr/share</Path>
            <Path fileType="data">/var/cache/fonts</Path>
        </Files>
        <AdditionalFiles>
            <AdditionalFile owner="root" permission="0644" target="/etc/env.d/98texlive">98texlive</AdditionalFile>
            AdditionalFile owner="root" permission="0644" target="/etc/texmf/texmf.d/00header.cnf">00header.cnf</AdditionalFile>
            <AdditionalFile owner="root" permission="0644" target="/etc/texmf/texmf.d/05searchpaths.cnf">05searchpaths.cnf</AdditionalFile>
            <AdditionalFile owner="root" permission="0644" target="/etc/texmf/texmf.d/10standardpaths.cnf">10standardpaths.cnf</AdditionalFile>
            <AdditionalFile owner="root" permission="0644" target="/etc/texmf/texmf.d/15options.cnf">15options.cnf</AdditionalFile>
            <AdditionalFile owner="root" permission="0644" target="/etc/texmf/texmf.d/20sizes.cnf">20sizes.cnf</AdditionalFile>
            <AdditionalFile owner="root" permission="0755" target="/usr/bin/texmf-update">texmf-update2009</AdditionalFile>
        </AdditionalFiles>
        <Provides>
            <COMAR script="package.py">System.Package</COMAR>
            <COMAR script="pakhandler.py">System.PackageHandler</COMAR>
         </Provides>
        </Package>

        <History>
            <Update release="4">
                <Date>2010-02-25</Date>
                <Version>0.0_20091107</Version>
                <Comment>Enable font generation to users.</Comment>
                <Name>Semen Cirit</Name>
                <Email>scirit@pardus.org.tr</Email>
            </Update>
            <Update release="3">
                <Date>2010-02-15</Date>
                <Version>0.0_20080816</Version>
                <Comment>Enable font generation to users.</Comment>
                <Name>Semen Cirit</Name>
                <Email>scirit@pardus.org.tr</Email>
            </Update>
        </History>
    </PISI>

Different pspec.xml File Tags
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. **<Source>:** This main tag is needed in order to give information about the source of the package.
    #. **<Name>:** The name of the package is added here. It must follow the :ref:`package-naming`. This should be match with the <Name> part of <Package> tag.
    #. **<Homepage>:** The project page of the package is added here.
    #. **<Packager>:** The packager name is added <Name>, and email is added to <Email> part.
    #. **<ExcludeArch>:** When a package could not be compiled for a specific architecture it should be added to pspec.xml file with this tag.
    #. **<License>:** The pacakge license type is added here. See :ref:`licensing-guidelines`.
    #. **<Icon>:** If a package has a gui part, the icon name should be added this part.
    #. **<IsA>:** This tag is used in order to give the types of the software which the the package includes. One then more IsA type can be used, if it is relevant.
        Different IsA types used for Pardus packages:

        * app
        * app:console
        * app:gui
        * app:web
        * library
        * service
        * data
        * data:doc
        * data:font
        * kernel
        * driver
        * locale
        * locale:aa
        * locale:af
        * locale:am
        * locale:an
        * locale:ar
        * locale:as
        * locale:ast
        * locale:az
        * locale:be
        * locale:ber
        * locale:bg
        * locale:bn
        * locale:bn_IN
        * locale:bo
        * locale:br
        * locale:bs
        * locale:byn
        * locale:ca
        * locale:ca@valencia
        * locale:crh
        * locale:cs
        * locale:csb
        * locale:cy
        * locale:da
        * locale:de
        * locale:dz
        * locale:el
        * locale:en
        * locale:en_CA
        * locale:en_GB
        * locale:eo
        * locale:es
        * locale:et
        * locale:eu
        * locale:fa
        * locale:fi
        * locale:fil
        * locale:fo
        * locale:fr
        * locale:fur
    #. **<Summary>:** The summary part of the package is added here. See `link <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#summary-and-description>`_.
    #. **<Description>:** The description of the package is added here. See `link <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#summary-and-description>`_.
    #. **<Archive>:** The package source code link, archive type and SHA-1 hashes. See `link <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#taking-sha-1-hash>`_.

        **sha1sum:** This attribute is for sha1sum value

        **type:** This attribute is for archive type.  These are the different archive types used for Pardus:

        * targz
        * tarbz2
        * tarlzma
        * tar
        * zip
        * gzip
        * binary

        The download link includes between <Archive> tag and the mirrors can also be used. See `usage <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#giving-mirrors>`_.

    #. **<BuildDependencies>:** This part is used in order to list packages which is required for building (compiling) the package. These dependencies can not be automatically find. So you should try to compile the pacakge in a proper system and you need to include everything needed to build the program. The packages for development environment are not needed to add as a build dependency. You can see the list of packages that will be ignored from `here <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#dependencies-excepted>`_. You need to add all dependencies in a different <Dependency> tag.  You can also specify minimum versions or releases of the package. See `link <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#strict-dependencies>`_ for details.
    #. **<Patches>:** The list of patches added here. Each patch should be added with <Patch> tag and added in the order that they applied.

    The level parameter is needed in order to apply the patch properly. It specifies depth differences of the patch and the file that the patch will be applied.
#. **<Package>:**  This main tag is needed in order to give package information when it runs on the system.

    #. **<Name>:** The name of the package is added here. It must follow the :ref:`package-naming`. This should be match with the <Name> part of <Source> tag.
    #. **<BuildType>** One more than packages can be created from same source, if one of these packages needs a special architecture to build, it should be added with <BuildType> tag. This value can be "32bit" or "64bit".
    #. **<BuildDependencies>** One more than packages can be created from same source, if one of these packages needs a special dependency to build, it should be added with <BuildDependencies> tag.
    #. **<RuntimeDependencies>:** This part is used in order to list packages which is required when the program runs. In order to find runtime dependencies please `see <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#runtime-dependencies>`_. You need to add all dependencies in a different <Dependency> tag. You can also specify minimum versions or releases of the package. See `link <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#strict-dependencies>`_ for details.
    #. **<AnyDependency>:** This part is used when the package can have more than one dependency for a specific work. See `link <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#any-dependency>`_.
    #. **<Conflicts>:** This part is used for the packages that conflict with the prapared package. See `link <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#conflicting-packages>`_

    #. **<Replaces>:** The packages that will be replaced with this package, will be added to this part. See `link <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#renaming-replacing-existing-packages>`_

    #. **<Files>:** This part is needed to specify the paths of different file types in the system. All file paths will be used with <Path fileType=""> tag.

       These are the different file types used for Pardus:

       * **config:** This is used for the configuration files and those  are placed under "/etc" path.
       * **executable:** This is used for the executable files and those are placed under "/usr/bin" path.
       * **header:** This is used for header files and those are placed under "/usr/include" path.
       * **library:** This is used for library files and those are placed under "/usr/lib" path.See `link <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#pre-built-binaries-or-libraries-not-allowed>`_.
       * **localedata:**" This is used for localisation files and those are placed under "/usr/share/locale" path.
       * **man:** This is used for manual files and those are placed under /usr/share/man path.
       * **doc:** This is used for documentation files and those are placed under "/usr/share/doc" path. See `link <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#documentation>`_.
       * **data:** This is used for shared data files and those are placed under "/usr/share" path.
       * **info:**  This is used for information files and those are placed under "/user/share/info" path.

    #. **<AdditionalFiles>:** This is used for files that does not exist in the source code and that will directly be installed to the system with the package. So we should give the file path, permission, group and owner for this file.

        **target:** This attribute is used to specify the file path and name

        **permission:** This attribute is used for giving `file permissions <http://en.wikipedia.org/wiki/Filesystem_permissions>`_.

        **owner:** This attribute is used to specify file owner.

        **group:** This attribute is used to specify file group. The "groups" command will list the groups of the current owner.

        Each file should be added like the below format:
        ::

            <AdditionalFile owner="mpd" group="audio" permission="0640" target="/etc/mpd.conf">mpd.conf</AdditionalFile>

        The files is included under files directory of the pisi package.

    #. **<Provides>:** This part is used for COMAR scripts. There ara two types of scripts used. And these files should be appeared in this part. See `link <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#package-setup-post-install-post-and-pre-remove-cleanup-and-post-cleanup>`_

#. **<History>:**  This main tag is needed in order to give information about packaging change history.

        #. **<Update>:** This part is unclude some other sub tags. It also  consists some attributes:

            **release:** The release number of the change should be gived here.

            **type:** The type of the change should be gived there. There are two types used for Pardus. For critical changes "critical", for security changes "security" value are used.
        #. **<Date>:** This part is used for adding the time that the change done. The format should be "YYYY-MM-DD"
        #. **<Version>:** The version of the package should be written there. See `link <http://developer.pardus.org.tr/guides/packaging/binary_package_naming_guidelines.html#version-number>`_
        #. **<Comment>:** The description of the change should be added here. See `link <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#history-comments>`_
        #. **<Requires>:** There are three type actions can be applied for the package.
            - reverseDependencyUpdate: This action should be used, when the package are installed, the packages that are dependent to this package should be updated::

                <Action package="module-fglrx-userspace">reverseDependencyUpdate</Action>
                <Action>reverseDependencyUpdate</Action>
            - systemRestart: This action should be used, when the package are installed, system needs restart::

                <Action package="module-pae-nvidia-current">systemRestart</Action>
                <Action>systemRestart</Action>
            - serviceRestart: This action should be used, when the package are installed, a specific service needs to restart::

                <Action package="dhcp">serviceRestart</Action>
                <Action>systemRestart</Action>

        #. **<Name>:** The name of the package maintainer that make the change should be added here.
        #. **<Email>:** The email of the package maintainer that make the change should be added here.

Creating translations.xml
-------------------------

The translations.xml is included in the pisi package source and it is needed for
the translations of summary and descriptions. All of the packages should include
this file.

**This is an empty translations.xml file:**

::

    <PISI>
        <Source>
            <Name></Name>
            <Summary xml:lang=""></Summary>
            <Description xml:lang=""></Description>
        </Source>
    </PISI>

**This is an example translations.xml file:**

::

    <PISI>
        <Source>
            <Name>texlive-core</Name>
            <Summary xml:lang="tr">TeX Live Dağıtımının Ana Parçası</Summary>
            <Description xml:lang="tr">texlive-core Tex Live dağıtımının ana parçasıdır.</Description>
            <Description xml:lang="fr">texlive-core est la partie essentielle de TeXLive.</Description>
        </Source>
    </PISI>

Different translations.xml File Tags
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. **<Name>:** The name of the package should be added here.
#. **<Summary>:** The translation of the summary should be added there. The language type should be gived as a value of "xml:lang" attribute.
#. **<Description>:**  The translation of the description should be added there. The language type should be gived as a value of "xml:lang" attribute.

See `link <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#summary-and-description>`_.

