.. _orphaned packages:

Orphaned and Retired Packages
=============================

**Last Modified Date:** |today|

:Author: Semen Cirit

:Version: template

Pardus knows that life changes, also your availability may change. When
package maintainers are not able to deal with their packages more than one
month, they should warn other developers about this situation and orphan or
retire their packages, that they could not maintain during this period.
If they think that the packages are still useful for Pardus, they should
orphan them. Then other maintainers that are interested in maintaining it,
can take ownership of this package.

Orphaning Process
-----------------

#. Announce on devel_ and gelistirici_ which package you want to orphan.
#. Run takeover_ script for the package(s) you want to orphan.

Before running script, write the below settings for orphaning the package::

    NAME="Pardus"
    EMAIL="admins@pardus.org.tr"


Retiring Process
----------------

#. Announce on devel_ and gelistirici_ which package you want to retire and take
   an approval from an experienced developer.
#. If the upstream does not exist any more, these packages should be removed
   from the active Pardus repositories. These packages should be obsoleted_ in
   distribution.xml file of active repositories.
#. If the package name will change or replaced by another package, `package
   replace procedure`_ is applied.


Takeover Process
----------------

#. Control why the package was orphaned on announced mail.
#. Announce on devel_ and gelistirici_ which packages you would like to become
   the owner of.
#. If you think that the component of the package is wrong, please also announce
   its new component and take an approval from an experienced developer.
#. Run takeover_ script for the package(s) you want to takeover.
    Write your name and email address for the below parts::

   	NAME="developer name"
           EMAIL="developer mail address"
#. Take all open bugs of the related packages on `Pardus bugzilla`_



Inactivity on Packages During Long Time
---------------------------------------

The package update time is mostly related to the upstream of the package, but
all package updates and bug status related to a subcomponent followed by
subcomponent supervisor. If a subcomponent supervisor claims that a package
left uninterested and its bugs are not triaged by its maintainer for a long
time of period, he starts the `contributor availability`_ process.

Also during a release cycle (approximately one year), if there is not any commit for
packages from the package maintainer and for the new release time, they have not
merged also to new release repositories by the package maintainer, these packages
listed on gelistirici_ and devel_ list and package maintainers mail are added to CC.
The developers that have not respond for two weeks the `contributor retirement`_ 
process starts.

List of Orphaned Packages
-------------------------

#. `2011 orphaned packages`_
#. `Corporate2 orphaned packages`_

.. _Corporate2 orphaned packages: http://packages.pardus.org.tr/info/corporate2/devel/packager/Pardus.html
.. _2011 orphaned packages: http://packages.pardus.org.tr/info/2011/devel/packager/Pardus.html
.. _devel: http://liste.pardus.org.tr/mailman/listinfo/pardus-devel
.. _gelistirici: http://liste.pardus.org.tr/mailman/listinfo/gelistirici
.. _takeover: http://svn.pardus.org.tr/uludag/trunk/scripts/takeover
.. _obsoleted: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#renaming-replacing-existing-packages
.. _package replace procedure: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#renaming-replacing-existing-packages
.. _Pardus bugzilla: http://bugs.pardus.org.tr/
.. _component: http://developer.pardus.org.tr/guides/packaging/package_components.html
.. _orphaned: http://developer.pardus.org.tr/guides/packaging/orphan_packages.html#orphaning-process
.. _contributor availability: http://developer.pardus.org.tr/guides/newcontributor/contributor_availability#component-or-related-supervisor-part
.. _contributor retirement: http://developer.pardus.org.tr/guides/newcontributor/contributor_availability#steps-to-retire-a-contributor

.. script sayfası yazılınca takeover linki yerine koy
.. orphaned packages liste linkini yeni packages sitesi yapılınca değiştir.
