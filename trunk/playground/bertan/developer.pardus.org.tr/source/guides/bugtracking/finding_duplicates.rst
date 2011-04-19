.. _finding-duplicates:

Finding Duplicate Bugs
======================

It is very valuable to file specific and reproducible bugs. Therefore please check possible duplicates of the bugs before report it. If you find your bug is reported more than once you can mark one of them as duplicate.

Mostly experienced bugs can be found from:

    * `Mostly frequently reported bugs list <http://bugs.pardus.org.tr/duplicates.cgi>`_.
    * Tracker bugs opened for Pardus Releases.

Use Bugzilla search to find duplicates
--------------------------------------
`Find spesific bug form <http://bugs.pardus.org.tr/query.cgi?format=specific>`_ enables users to search eith keywords.

`Advance search form <http://bugs.pardus.org.tr/query.cgi?format=advanced>`_ looks a little complex. But it is a powerful search interface, you only need to state your search criteria and ignore the other parts of the form. The empty parts do not limit your search, the bugs will be listed only according to your criteira.

For the status part NEW, ASSIGNED and REOPEN are selected by default. These bugs are all not resolved bugs.

You can state a word or a simple phrase. For example: desktop settings, screen etc. If you enter one more than word and they are not perform a phrase, you can change the search criteria to "contains any of the string" or "contains all of the strings".

Please do not state any keyword before clicking the `Keyword link <http://bugs.pardus.org.tr/describekeywords.cgi>`_: Unless you use the keywords in the list, the search won't work. This part only searching by keywords.
There are two types of keyword in Pardus, one of them is for the bugs that needs information, the other is for upstream related bugs.

There exist also a graphical search part at the bottom of the search form.

What to do if a dupliacte is catched?
-------------------------------------

If you are a bug triager or a developer, you can select resolution as "RESOLVED/DUPLICATE" for the bug that has less information and add the bug number of the best information.

If you don't have permission to change bugs, you can give duplicate bug number as a comment, someone else will see and do the relavant operation.


**Last Modified Date:** |today|

:Author: Semen Cirit
