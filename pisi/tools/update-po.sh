find pisi -iname '*.py' | grep -v pisi/cli/commands.py >exclude
echo tools/pygettext.py >>exclude
python tools/pygettext.py -D -X exclude -o po/pisi.pot pisi pisi-cli tools
msgmerge -U po/tr.po po/pisi.pot
rm exclude
