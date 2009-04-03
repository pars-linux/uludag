PROJECT_NAME=network-manager
INSTALL_DIR=/usr/kde/4/share/apps/$(PROJECT_NAME)

all: build
build:
	pykde4uic -o uimain.py ui.ui
	pykde4uic -o uiitem.py ui.item.ui
	pykde4uic -o uisettings.py settings.ui
	pykde4uic -o uidevices.py devices.ui
	python fix-pykdeuic uimain.py
	pyrcc4 data.qrc -o data_rc.py
clean:
	-rm *.pyc uimain.py uiitem.py uisettings.py uidevices.py data_rc.py
install: uninstall
	mkdir -p $(INSTALL_DIR)
	install -m 0755 main.py $(INSTALL_DIR)/$(PROJECT_NAME)
	ln -s $(INSTALL_DIR)/$(PROJECT_NAME) $(INSTALL_DIR)/$(PROJECT_NAME).py
	install -m 0644 about.py $(INSTALL_DIR)
	install -m 0644 uimain.py $(INSTALL_DIR)
	install -m 0644 uiitem.py $(INSTALL_DIR)
	install -m 0644 data_rc.py $(INSTALL_DIR)
	install -m 0644 faces.py $(INSTALL_DIR)
	install -m 0644 uisettings.py $(INSTALL_DIR)
	install -m 0644 uidevices.py $(INSTALL_DIR)
	install -m 0644 nettools.py $(INSTALL_DIR)
	# install -m 0644 settings-service-manager.desktop /usr/kde/4/share/kde4/services
uninstall:
	rm -rf $(INSTALL_DIR)
	# rm -f /usr/kde/4/share/kde4/services/settings-service-manager.desktop
