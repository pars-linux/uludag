# Translation #
## For translators: ##
If you do first translation in your language, enter the po/ directory and create your .po file. Example:
    $ cd po
    $ msginit -l tr

Please don't forget to set CHARSET in your .po file. I prefer Poedit for translating .po files.

## For developers: ##
(I'm thinking to write a puding-dev script for developers.)
To update main translation file:
    $ cd po
    $ intltool-update -p

For Qt translation file:
    $ cd $(PUDING)/qt4
    $ pylupdate4 /usr/lib/python*/site-packages/puding/qt*.py src/*.py -ts messages.ts

