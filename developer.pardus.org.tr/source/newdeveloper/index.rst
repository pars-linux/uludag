.. _newdeveloper-index:

##############################
New developer's guide
##############################

In this document we'll try to explain the requirements to be a Pardus developer/contributor. Although we are talking about Pardus in particular, the cited requirements in this document should apply to nearly all open source projects.

Please feel free to browse the web pages of `Pardus <http://www.pardus.org.tr/eng>`_ for other information not included in this document.

Who is a developer?
====================

To put it roughly, it is not wrong to say that the project should fulfill two types of mission. As it is the case for any distribution, gathering the software and preparing the infrastructure to enable this task and sustaining it, as well as developing new tools and technologies to form the soul of the distribution are among the required tasks.

When referring to developer, we describe not only those who write programs but also those who fulfill any single task. We are aware that work has to be done in many areas such as documentation, bug triaging, visual materials, translations etc. besides programming to implement a software project. We need all of them for Pardus as well.

How do I start?
================

First of all it's a good idea to keep up with the ongoing discussions. The most effective way of achieving this is to observe for a while and see how people work. It might be useful to join the `e-mail lists <http://lists.pardus.org.tr>`_ and follow the discussions, the ongoing events, the bug reports, the solutions proposed to the bug reports and examine the documents published.

By considering the outlined methods you may continue to help the development process. You can add your comments and proposals for solutions to the `bug reports <http://bugs.pardus.org.tr>`_ by testing the sofware or you can report the new bugs you've just found. You can contribute to develop innovative technologies and add new features or you can support a step of the process which you think is not working correctly or fast enough.

During the development process, you should always be in *communication* with other developers and contributors. As it's true for all tasks performed by more than one person, we always need to have knowledge of each other.

The process of development is completely transparent to the public, and open to any contributor who demonstrates the necessary skills and commitment to the project.

Communication
==============

Email discussion among Pardus developers takes place on the `pardus-devel mailing list <http://liste.pardus.org.tr/mailman/listinfo/pardus-devel>`_, which is moderated (except Pardus developers having an SVN account).

The ``#pardus-devel`` channel on FreeNode IRC network is home to many Pardus developers for real-time communication.

********************
Areas to contribute
********************

In this section, we'll briefly cover the different areas to contribute.

Software development
=====================

You can contribute your knowledge and labour on developing new softwares for Pardus or improving already written ones. For achieving this purpose, you should be familiar with different Pardus technologies like COMAR, PiSi, Mudur, Kaptan to understand how things work in Pardus Linux.

Packaging
==========

If you're interested in preparing PiSi packages, but don't have much experience yet, you can read the :ref:`pisi-packaging-guide` to get involved in the packaging process.

Localization
=============

Pardus officially supports 11 languages: Turkish, English, Dutch, French, German, Spanish, Catalan, Italian, Swedish, Polish and Brazilian Portuguese.

The goal of the localization team is to bring everything around Pardus closer to local communities (countries and languages). Usually this involves doing translations of Pardus tools, websites and documentations and improving their quality.

A collaborative meeting point for Pardus translators is the ``pardus-translators`` `e-mail list <http://lists.pardus.org.tr/mailman/listinfo/pardus-translators>`_.

More information and statistics can be found in Pardus translation project's `website <http://www.pardus.org.tr/eng/projects/translation/>`_.

Bug reporting and triaging
===========================

Pardus bug reports are tracked in bugzilla. You can examine bugs to determine whether or not they have enough information and feedback to be worked on and assign a priority/component/product to them as soon as possible.

To know that the very same bug exists in other distributions might help us to produce a proper solution. If the problem is solved -or never existed- in another distribution, reaching a solution will be faster by examining the work that the particular distribution did for that software.

A detailed bug triaging documentation will be available as soon as possible to guide you through the mechanisms and the workflows commonly used in bugzilla and bug triaging approaches.

In order to help triaging bugs, you have to be able to find them. You can find about new bug reports by subscribing to the bugzilla `e-mail list <http://lists.pardus.org.tr/mailman/listinfo/bugzilla>`_.

Our bug tracking system can be reached via http://bugs.pardus.org.tr. Just create an account and you'll be immediately able to report new bugs and write comments to the existing bug reports. You don't need an account for browsing current bug reports.

Documentation
==============

You can support the documentation of the ongoing projects and different development content. Along with the end user documents, you can also prepare *HOWTO* documents for the users/contributors/developers that have newly joined the project.

The `wiki <http://pardus-wiki.org>`_ for Pardus is a nice place to start helping for the documentation.

You can also enrich the content of this `developer web page <http://developer.pardus.org.tr>`_. Currently, only people with an SVN account have write permissions to the content.

About this document
====================

:Author: Ozan Çağlayan
:Date: |today|


.. toctree::
   :maxdepth: 2
