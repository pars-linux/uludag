.. _preparing-buildfarm:

Preparing Buildfarm
===================

:Author: Semen Cirit, Fatih Aşıcı

:Last Modificaiton Date: |today|

:Version: 0.1

Buildfarm is an automated package building tool for Pardus packages. When it is
installed and start to work it send warning mails to contributors for start and
end time of compiling and compile errors.

Preparing Buildfarm From Scratch
--------------------------------

At first a new devel source repository should be created.

At the beginning of a new release after bootstrapping, a developer release is
prepared and this release is installed to the related server.

The other procedures are the same with `Installing and Starting Buildfarm`_.

Preparing Buildfarm for an Existing Release
-------------------------------------------


#. The existed system is installed to the relevant server.
#. All packages in the repository must be installed, therefore it should be listed first:
    ::

        pisi la -U <repository-name> --no-color | sed "s/.*//" > <package-list-file>
#. Control the <package-list-file> in order to remove problematic packages (obsolete, breaks the pisi working etc. )
#. Ignore all file and package conflicts and install the pacakges
    ::

        pisi it --ignore-file-conflicts --ignore-package-conflicts `cat <package-list-file>`
#. Delete all repositories added from the system
    ::

        pisi dr <repository-name>
#. Controll disk usage and if the cache is full, delete pisi cache:
    ::

        df -h
        rm -rf /var/cache/pisi/packages/

Installing and Starting Buildfarm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Check out the buildfarm_ code from `core project source repository`_
    ::

        svn co http://svn.pardus.org.tr/uludag/trunk/scripts/buildfarm/
#. Install buildfarm
    ::

        cd buildfarm
        ./setup.py install
#. There are three files that should be edditted:
    #. /etc/buildfarm/buildfarm.conf

        The followings should be editted according to buildfarm repository that will be created:
        ::

            Release=
            SubRepository=
            Architecture=

        The other part can remain the same if there is not any changes on mailer system or other directories.
    #. /etc/buildfarm/auth.conf

        The followings should be editted according to mailer daemon:
        ::

            username=
            password=
    #. /etc/pisi/pisi.conf

         The followings should be editted to these values:
         ::

            build_host=buildfarm.pardus.org.tr
            build_helper=ccache
            compressionlevel=9
            enableSandbox=True (for testing farm)
            enableSandbox=False (for devel farm)
            generateDebug=True
            jobs=-j25 (this is an example for 24 core server)
            autoclean=True
#. Change the ccache limit to maximum.
    ::

        ccache -s
        ccahche -M 10
#. Start rsync and edit /etc/rsyncd.conf in order to enable sync repositories to packages.pardus.org.tr
#. Start services rsync, openssh, vixie_cron, rsyslog and apache services, stop the others
#. Add under /var/www/localhost/htdocs and redirect the prepared index.html in order to mask the internal ip addresses.
#. Symlink log messages under /var/log/buildfarm directory with /var/www/localhost/htdocs/logs in order to access logs outside of the farm.
    ::

        ln -s /var/log/buildfarm/<directories> /var/www/localhost/htdocs/logs
#. Symlink repository directories with /var/www/localhost/htdocs/<repository-directory> in order to sync it with http://packages.pardus.org.tr
    ::

        ln -s ~/pardus/<pardus-release-name>/<repository-name>/<architecture-name> /var/www/localhost/htdocs/pardus/<pardus-release-name>/<repository-name>/<architecture-name>
        ln -s ~/pardus/<pardus-release-name>/<repository-name>/<architecture-name-debug> /var/www/localhost/htdocs/pardus/<pardus-release-name>/<repository-name>/<architecture-name-debug>

#. Check out the related svn  source repository
    ::

        buildfarm-init

#. If the it is a buildfarm for an existing release, the existed packages from a relevant repository is copied to /var/db/buildfarm/packages/<pardus-release-name>/<repository-name>/<architecture-name>.
    Old packages can be removed.

#. Start buildfarm
    ::

        cd /var/lib/buildfarm/<pardus-release-name>/<repository-name>/<architecture-name>
        buildfarm-up
        vi waitqueue (edit if necessary)
        vi workqueue (edit if necessary)
        buildfarm

.. _bootstrapping: http://developer.pardus.org.tr/guides/releasing/bootstrapping.html
.. _core project source repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#core-projects-source-repository
.. _buildfarm: http://svn.pardus.org.tr/uludag/trunk/buildfarm/
