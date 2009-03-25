PROJECT_NAME=history-manager-kde4
INSTALL_DIR=/usr/kde/4/share/apps/$(PROJECT_NAME)

all: build
build:
	pykde4uic -o src/ui_mainwindow.py ui/mainwindow.ui
	python fix-pykdeuic src/ui_mainwindow.py
	pyrcc4 resources/data.qrc -o src/data_rc.py
clean:
	-rm */*.pyc src/ui_mainwindow.py src/data_rc.py

export DESTDIR := $(DESTDIR)
export VERSION := $(VERSION)
install: uninstall
	mkdir -p $(DESTDIR)$(INSTALL_DIR)
	install -m 0755 src/main.py $(DESTDIR)$(INSTALL_DIR)/$(PROJECT_NAME).py
	ln -s $(DESTDIR)$(INSTALL_DIR)/$(PROJECT_NAME).py $(DESTDIR)$(INSTALL_DIR)/$(PROJECT_NAME)
	install -m 0644 src/about.py $(DESTDIR)$(INSTALL_DIR)
	install -m 0644 src/mainwindow.py $(DESTDIR)$(INSTALL_DIR)
	install -m 0644 src/interface.py $(DESTDIR)$(INSTALL_DIR)
	install -m 0644 src/listitem.py $(DESTDIR)$(INSTALL_DIR)
	install -m 0644 src/utility.py $(DESTDIR)$(INSTALL_DIR)
	install -m 0644 src/ui_mainwindow.py $(DESTDIR)$(INSTALL_DIR)
	install -m 0644 src/data_rc.py $(DESTDIR)$(INSTALL_DIR)
	cp -r resources/help $(DESTDIR)$(INSTALL_DIR)
uninstall:
	rm -rf $(DESTDIR)$(INSTALL_DIR)
	rm -f $(DESTDIR)/usr/kde/4/share/kde4/services/settings-history-manager.desktop

package:
	svn export . $(PROJECT_NAME)-$(VERSION)
	tar -jcf $(PROJECT_NAME)-$(VERSION).tar.bz2 $(PROJECT_NAME)-$(VERSION)
	rm -rf $(PROJECT_NAME)-$(VERSION)
