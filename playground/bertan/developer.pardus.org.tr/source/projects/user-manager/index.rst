.. _user-manager-index:

User Manager
~~~~~~~~~~~~

:Author: Beyza Ermiş

User Manager is a Kde application for managing users, groups and policies.
It uses COMAR as configuration backend.

To run User Manager you may follow either Pardus Menu > Applications > System > User Manager
or the System Configuration section


Features
----------
* New users or groups could be added.
* Existing users or groups could be removed.
* Authorization scopes of existing groups and users could be modified. 

Source Code
-----------
You can `browse <http://svn.pardus.org.tr/uludag/trunk/kde/user-manager/manager/>`_ source code from WebSVN_.

Or you can get the current version from Pardus SVN using following command::

$ svn co http://svn.pardus.org.tr/uludag/trunk/kde/user-manager/manager

Then you can install user-manager from the source code by typing:

    ./setup build
    sudo ./setup install

Requirements
------------

* PyQT
* PyKDE
* PolicyKit


Bugs
----

* `Normal Priority Bug Reports <http://bugs.pardus.org.tr/buglist.cgi?bug_severity=normal&classification=Pardus%20Teknolojileri%20%2F%20Pardus%20Technologies&query_format=advanced&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&product=Kullan%C4%B1c%C4%B1%20Y%C3%B6neticisi%20%2F%20User%20Manager>`_
* `Wish Reports <http://bugs.pardus.org.tr/buglist.cgi?bug_severity=low&classification=Pardus%20Teknolojileri%20%2F%20Pardus%20Technologies&query_format=advanced&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&product=Kullan%C4%B1c%C4%B1%20Y%C3%B6neticisi%20%2F%20User%20Manager>`_
* `Feature Requests <http://bugs.pardus.org.tr/buglist.cgi?bug_severity=newfeature&classification=Pardus%20Teknolojileri%20%2F%20Pardus%20Technologies&query_format=advanced&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&product=Kullan%C4%B1c%C4%B1%20Y%C3%B6neticisi%20%2F%20User%20Manager>`_

Tasks
-----

* `Open tasks <http://proje.pardus.org.tr:50030/projects/user-manager/issues?set_filter=1&tracker_id=4>`_

Developed by
------------

*Gökmen Göksel <gokmen_at_pardus.org.tr>

*Bahadır Kandemir <bahadir_at_pardus.org.tr>

License
-------

User Manager is distributed under the terms of the `GNU General Public License (GPL), Version 2 <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>`_.

.. _Pisi: http://developer.pardus.org.tr/pisi
.. _Python: http://www.python.org
.. _WebSVN: http://websvn.pardus.org.tr/uludag/trunk/kde/user-manager/
