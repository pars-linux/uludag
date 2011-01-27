.. _generating-nightly-builds:

:Author: Semen Cirit

:Last Modificaiton Date: |today|

:Version: 0.1

Generating Nightly Builds
==========================

Nightly builds are the daily test releases of pardus. In order to automatically
generate these nightly builds and upload them to ftp servers the following steps
are performed:

#. Check out nightly_ script from `core source code repository`_:
    ::

        svn co http://svn.pardus.org.tr/uludag/trunk/scripts/nightly/

#. Add the script to /etc/crontab and start nightly script as a cron job:
    ::

        15 3  * * * root    /root/nightly/build.sh > /root/nightly/build-all.log 2>&1


.. _nigtly: http://svn.pardus.org.tr/uludag/trunk/scripts/nightly/
.. _core source code repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#core-projects-source-repository
