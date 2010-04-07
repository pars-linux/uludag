=============================
Translation Quick Start Guide
=============================

Quick start guide to providing translations on Pardus
-----------------------------------------------------

#. Subscribing to the Mailing List

 * Visit http://lists.pardus.org.tr/mailman/listinfo/pardus-translators and 
   subscribe to this mailing list.

 * Wait for the confirmation email which contains a link to confirm your 
   subscription. Click the link to confirm your subscription.

#. Introducing Yourself

 * Post a short self introduction to the pardus-translators mailing list.
   Please remember to include your Transifex user name and your language.
   With this information, language coordinator can identify you for
   language team joining approval.

#. Create a Bugzilla account

 * Visit http://bugs.pardus.org.tr to create a Bugzilla account. This is
   useful for translators since there could be a bug in a translation file's
   source (POT) and you should file a bug in order to warn the project maintainer.

#. Welcome

 * You are now a fully recognized member of Pardus community, capable of
   submitting contributions, submitting bugs and following the discussions of our groups.

#. Obtaining and Translating Projects

 Now that you have prepared a directory structure, you can download a file to
 translate. You may need to communicate with other translators in your language
 team to avoid conflict. If you are not sure, please contact your language coordinator.

 1. Visit your language page such as http://translate.pardus.org.tr/transifex/languages/l/pl/,
    and select a target release. The interface will redirect you to a page for
    that release, such as http://translate.pardus.org.tr/transifex/projects/p/pardus/r/corporate2/l/pl/.

 2. Scroll down the page to find the table of all projects available for that
    release. Use the arrow download icon labeled Download pl.po or similar next
    to each project to download the po file.

 3. Since the file name to commit follows the name convention of lang.po, change
    the name of the downloaded file.

 4. Now the file is ready for translation. Translate the po file for your language
    in a po editor such as Lokalize.

 5. Check the integrity of your file before you commit it.

    ``msgfmt -c --statistics pl.po``

#. Committing Projects

 Once you finish translation work, commit the file using the same interface.

 1. Go back to your language page such as
    http://translate.pardus.org.tr/transifex/languages/l/pl/, and select a
    target release. The interface will redirect you to a page for that release,
    such as http://translate.pardus.org.tr/transifex/projects/p/pardus/r/corporate2/l/pl/.

 2. Login

  At the bottom of the page, select Sign in to visit the Sign in page.
  Authenticate with your Transifex user name and password.

 3. Submit

 Use the pencil icon labeled Send a translation for this language next to each
 project, then click the browse button to locate your translated file.

 Select the Send to commit your translated file.

 Interface displays the message File submitted successfully. If you receive an
 error or some other success message, please post it to the pardus-translators
 mailing list so it can be addressed. 

#. Adding New .po File

 If there is no po file for your language, please do the following steps:

 * Download the pot file and copy it as your own language's **po** file.

 * Once you finish the translation, click on the Add a new translation button
   at project page.

 * Type your new file name in the field marked or enter it here:, replacing
   the file name with your locale:

   ``po/<your_lang>.po``

#. Proofreading

To proofread your translation as part of the software, follow these steps:

 1. Change directory to the package you want to proofread. For example,

   cd ~/myproject

 2. Convert the .po file to a .mo file using msgfmt with -o option:

   msgfmt -o myproject..mo pl.po

 3. As a root user, overwrite the existing .mo file in
    /usr/share/locale/lang/LC_MESSAGES/.

   First, back up the existing file:

   su -

   cp /usr/share/locale/pl/LC_MESSAGES/myproject.mo myproject.mo.bak

   Now move the file converted for proofreading.

   mv myproject.mo /usr/share/locale/pl/LC_MESSAGES/

   Exit root user.

   exit

 4. Proofread the package with the translated strings as part of the application:

   LANG=pl_PL.UTF-8 myproject

    The application related to the translated package runs with the translated
    strings.
