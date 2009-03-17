PROJECT_NAME=history-manager
INSTALL_DIR=/usr/kde/4/share/apps/$(PROJECT_NAME)

all: build
build:
	pykde4uic -o src/ui_mainwindow.py ui/mainwindow.ui
	python fix-pykdeuic src/ui_mainwindow.py
	pyrcc4 resources/data.qrc -o src/data_rc.py
clean:
	-rm */*.pyc src/ui_mainwindow.py src/data_rc.py
install: uninstall
	mkdir -p $(INSTALL_DIR)
	install -m 0755 src/main.py $(INSTALL_DIR)/$(PROJECT_NAME).py
	ln -s $(INSTALL_DIR)/$(PROJECT_NAME).py $(INSTALL_DIR)/$(PROJECT_NAME)
	install -m 0644 src/about.py $(INSTALL_DIR)
	install -m 0644 src/mainwindow.py $(INSTALL_DIR)
	install -m 0644 src/interface.py $(INSTALL_DIR)
	install -m 0644 src/listitem.py $(INSTALL_DIR)
	install -m 0644 src/utility.py $(INSTALL_DIR)
	install -m 0644 src/ui_mainwindow.py $(INSTALL_DIR)
	install -m 0644 src/data_rc.py $(INSTALL_DIR)
	cp -r resources/help $(INSTALL_DIR)
	install -m 0644 resources/settings-history-manager.desktop /usr/kde/4/share/kde4/services
uninstall:
	rm -rf $(INSTALL_DIR)
	rm -f /usr/kde/4/share/kde4/services/settings-history-manager.desktop
