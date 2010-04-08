=====================================================
Quick start guide to providing translations on Pardus
=====================================================

#. Subscribing to the Mailing List

   - Pardus uses Transifex to help translators keep track of translation
     projects. Please register yourself to Transifex at
     http://translate.pardus.org.tr.

   - Visit http://lists.pardus.org.tr/mailman/listinfo/pardus-translators and
     subscribe to this mailing list.

   - It is better to subscribe to development mailing list in order to keep
     syncronized with other developers. Use the link below:
     http://lists.pardus.org.tr/mailman/listinfo/pardus-devel.

   - Wait for the confirmation emails from you've just registered and
     subscribed services. These e-mails contains a link to confirm your
     subscription, click the link to confirm your subscription.

#. Introducing Yourself

   - Post a short self introduction to the pardus-translators mailing list.
     Please remember to include your Transifex user name and your language.
     With this information, language coordinator can identify you for language
     team joining approval.

#. Create a Bugzilla account

   * Visit http://bugs.pardus.org.tr to create a Bugzilla account. This is
     useful for translators since there could be a bug in a translation file's
     source (POT) and you should file a bug in order to warn the project
     maintainer. This is not mandatory of course.

   * You are now a fully recognized member of Pardus community, capable of
     submitting contributions, submitting bugs and following the discussions of
     our groups.

#. Obtaining and Translating Projects

   You may need to communicate with other translators in your language team to
   avoid conflict. If you are not sure, please contact your language
   coordinator.

   #. Visit your language page such as
      http://translate.pardus.org.tr/transifex/languages/l/pl/, and select a
      target release. The interface will redirect you to a page for that
      release, such as
      http://translate.pardus.org.tr/transifex/projects/p/pardus/r/corporate2/l/pl/.

   #. Scroll down the page to find the table of all projects available for that
      release.

      ..  image:: dl.png

      Use the marked icon or similar next to each project to download the po
      file.

   #. Before starting to translate any translation file, please make sure that
      none of the translators are working on the file you choose. Transifex eases
      this kind of conflicts with an icon indicating that a translator is working
      on the file. See the marked icon below:

      ..  image:: locked.png

   #. If noone is working on the file, as indicated by the icon, you can
      safely translate the file. First step is to lock the file by clicking the
      lock button. This way, you tell that you are working on the file and going
      to unlock it when the translation is done and commited.

   #. Now you are aware of the workflow and begin translating. Translate the po file for your
      language in a po editor such as Lokalize, or use Transifex' online po
      editor. Just click the icon below and start translating.

      .. image:: edit.png

   #. Check the integrity of your file before you commit it.

      ``msgfmt -c --statistics pl.po``

#. Committing Projects

   Once you finish translation work, commit the file using the same interface.

   Use the upload icon labeled Send a translation for this language next to
   each project, then click the browse button to locate your translated
   file.

   .. image:: ul.png

   Select the Send to commit your translated file.

   Interface displays the message File submitted successfully. If you
   receive an error or some other message except success, please post it to the
   pardus-translators mailing list so it can be addressed.

#. Adding New Translation File

   If there is no po file for your language, please do the following steps:

   * Download the pot file and copy it as your own language's **po** file.

      .. image:: dl-pot.png

   * Once you finish the translation, click on the Add a new translation button
     at project page.

      .. image:: add-new.png

   * Type your new file name in the field marked or enter it here:, replacing
     the file name with your locale:

       **po/your_lang.po**

      .. image:: add-new2.png

