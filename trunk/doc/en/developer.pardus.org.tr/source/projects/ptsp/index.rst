.. _ptsp-index:

PTSP
~~~~

:Author: Metin Akdere

**PTSP** is an abbreviation for Pardus Terminal Server Project which aims to boot thin clients over the network without needing any extra hardware or software on the client-side. It helps you to reduce your maintainence and administration costs in such environments where you need same type of workspace.

Although some other variations of terminal server projects exist out there in the community, the main reason of creating **PTSP** is to ease the management of the packages which are used to create rootfs. For instance LTSP_ is another distribution that is used on the thin-client machines. It has its own packaging system with a Perl_ based management tool. The created rootfs by ltsp admin tool is not Pardus. Updating the packages,
and keeping up with the distribution is not an easy task. The management and configuration scripts are hacky. With Pisi_, Mudur_, Coolplug_, Zorg_ and COMAR_ tools Pardus has all the infrastructure to create an automatically bootable rootfs with its own packages.

F (Pardus Terminal Server Projecteaturel
--------

Source Code
-----------

You can `browse <http://websvn.pardus.org.tr/uludag/trunk/ptsp/>`_
source code from WebSVN_.

Or you can get the current version from Pardus SVN using following commands::

$ svn co https://svn.pardus.org.tr/uludag/trunk/ptsp


Requirements
------------


Bugs
----

Developed by
------------

* Faik Uygur <faik_at_pardus.org.tr>
    First Developer

License
-------

Package Manager is distributed under the terms of the `GNU General Public License (GPL), Version 2 <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>`_.

.. _COMAR: https://svn.pardus.org.tr/uludag/trunk/comar/
.. _Coolplug: https://svn.pardus.org.tr/uludag/trunk/coolplug/
.. _LTSP: http://www.ltsp.org/
.. _Mudur: https://svn.pardus.org.tr/uludag/trunk/mudur/
.. _Pisi: http://developer.pardus.org.tr/pisi/
.. _Python: http://www.python.org/
.. _WebSVN: http://websvn.pardus.org.tr/uludag/trunk/ptsp/
.. _Zorg: https://svn.pardus.org.tr/uludag/trunk/zorg/
