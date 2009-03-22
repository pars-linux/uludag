PROJECT_NAME=history-manager
INSTALL_DIR=/usr/kde/4/share/apps/$(PROJECT_NAME)

all: build
build:
	pykde4uic -o src/ui_mainwindow.py ui/mainwindow.ui
	python fix-pykdeuic src/ui_mainwindow.py
	pyrcc4 resources/data.qrc -o src/data_rc.py
clean:
	-rm */*.pyc src/ui_mainwindow.py src/data_rc.py

export DESTDIR := $(R)
install: uninstall
	mkdir -p $(R)$(INSTALL_DIR)
	install -m 0755 src/main.py $(R)$(INSTALL_DIR)/$(PROJECT_NAME).py
	ln -s $(R)$(INSTALL_DIR)/$(PROJECT_NAME).py $(R)$(INSTALL_DIR)/$(PROJECT_NAME)
	install -m 0644 src/about.py $(R)$(INSTALL_DIR)
	install -m 0644 src/mainwindow.py $(R)$(INSTALL_DIR)
	install -m 0644 src/interface.py $(R)$(INSTALL_DIR)
	install -m 0644 src/listitem.py $(R)$(INSTALL_DIR)
	install -m 0644 src/utility.py $(R)$(INSTALL_DIR)
	install -m 0644 src/ui_mainwindow.py $(R)$(INSTALL_DIR)
	install -m 0644 src/data_rc.py $(R)$(INSTALL_DIR)
	cp -r resources/help $(R)$(INSTALL_DIR)
uninstall:
	rm -rf $(R)$(INSTALL_DIR)
	rm -f $(R)/usr/kde/4/share/kde4/services/settings-history-manager.desktop
