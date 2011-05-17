
build:
	pyuic4 ui/ui_main.ui -o ui/ui_main.py
	pyuic4 ui/ui_mainscreen.ui -o ui/ui_mainscreen.py
	pyuic4 ui/ui_screen_1.ui -o ui/ui_screen_1.py
	pyuic4 ui/ui_screen_2.ui -o ui/ui_screen_2.py
	pyuic4 ui/ui_screen_3.ui -o ui/ui_screen_3.py

install:
	mkdir -p /usr/share/um/ui
	cp ui/*.py /usr/share/um/ui
	cp *.py /usr/share/um/
	rm -f /usr/bin/upgrade-manager
	ln -s /usr/share/um/main.py /usr/bin/upgrade-manager
	chmod +x /usr/share/um/main.py

uninstall:
	rm -rf /usr/share/um
	rm /usr/bin/upgrade-manager

clean:
	find -name *.pyc | xargs rm -rf
	rm -vf ui/ui_*.py

