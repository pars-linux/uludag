Pardus Target Audience and Package Inclusion and Update Vision
==============================================================

The person whom wants to use Pardus probably:

    #. is a volunteer switching to Linux
    #. is familiar with computers but is not necessarily a hacker or developer
    #. is likely to collaborate in some fashion when something's wrong with Pardus, and
    #. wants to use Pardus for daily usage, either using desktop applications or a Web browser

For the Pardus Corporate release we extend this vision to support server and development languages and environments.


Therefore Pardus target audience extends whom also:

    #. maintain and operate computer systems and network
    #. install, support and maintain servers and other computer systems
    #. manage network and database services and deal with their problems
    #. use virtualization technologies for servers
    #. know version control systems
    #. know debugging and development languages and environments
        * Preferential languages that Pardus official repositories support:
            - Python
            - C,C++
            - Java
            - Perl
            - Ruby
            - Bash
            - Php


Daily Usage
-----------

Pardus takes into account below user actions as daily usage.

Basic Experiences
^^^^^^^^^^^^^^^^^

    * Can open/close or adjust monitor
    * Can control that the power cable is plugged in or power supply is worked properly
    * Can use mouse, touch pad or touch screen
    * Can set printer, fax or scanner and use them
    * Can plug in/out peripheral device and equipments
    * Can choose suitable application to work on
    * Can choose necessary hardware for the system
    * Can use data storage devices like floppy disk, CD, DVD, usbdisk, usbmemory etc.
    * Can burn CD/DVD
    * Can use technological applience that communicate with computers (mobile phone, tablet pc, PDA, digital camera, etc.)

Desktop Experiences
^^^^^^^^^^^^^^^^^^^

    * Can use package manager to install/update/remove packages
    * Can use KDE system settings and change appearance and settings (wallpaper, date/time, sound, colour ve resolution, theme, icons etc.)
    * Can manage directory and files:
          - Create new file/directory
          - Copy/paste/cut functionality
          - Remove file/directory
    * Can transfer/move/copy/backup data to different data storage media
    * Know how to quit from an application
    * Know how to archive, compress and decompress files/directories
    * Know help pages and can read these pages when ever need
    * Know how to change disk partitioning
    * Can share file and directories over a network
    * Can use multimedia to listen music or watch video or broadcast. (audio, video, raido/TV etc.)
    * Can make basic changes on images (cut, copy, crop, scale, etc.)

Personal Infromation Management and Office Applications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    * Can use office applications like document writer, presenter, spreadsheet, drawing, etc.
    * Use latex/tex
    * Can use personal information aplications like mail, news reader, address book, calender, scheduler etc.

Network Experince
^^^^^^^^^^^^^^^^^

    * Know how to connect internet
    * Can use web browser and searching engines
    * Can use plugins when needed
    * Can download files over Internet
    * Can use remote desktop
    * Can use file sharing

Package Inclusion and Update Vision
-----------------------------------

Visible behaviour changes will affect user experience, because these changes keep away users from their daily usage and users must spent time to discover what has changed. This outcome is undesirable. Therefore package inclusion and update vision is come to the fruition under this idea.

This vision is rationale for Pardus official repositories.

    * Instead of adding new packages with same functionality, we try to hardenning the functionality of existed packages' daily usage desktop experience
    * All desktop applications have Turkish localization (This is a must due to Pardus Project Vision)
    * Stable repository updates should be consistent and high quality stream of updates.
    * Stable repository should provide a consistent user experience throughout the release lifecycle, and only fix bugs and security issues.
    * Stable releases should not be used for tracking upstream version closely when this is likely to change the user experience beyond fixing bugs and security issues.
    * Close tracking of upstream should be done in the devel repository wherever possible, and we should strive to move our patches upstream.
    * Stable, testing and devel repositories have different approaches to what types of updates are expected. For example, testing should accept some updates which a stable release would not, and devel would accept updates that are not appropriate for either stable or testing repository.
    * All developers should be able to transparently measure or monitor a new updates process to objectively measure its effectiveness, and determine whether the updates process is achieving the aforementioned vision statements.

- For other details about package inclusion please follow `package inclusion requirements`_ and `new package inclusion process`_.
- For other details about package update please follow `package update process`_.

.. _package inclusion requirements: http://developer.pardus.org.tr/guides/packaging/package-review-process.html#package-inclusion-requirements-and-aim-of-review
.. _package update process: http://developer.pardus.org.tr/guides/packaging/package_update_process.html
.. _new package inclusion process: http://developer.pardus.org.tr/guides/newfeature/new_package_requests.html

