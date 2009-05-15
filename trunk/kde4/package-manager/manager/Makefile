
PROJECT_NAME=package-manager
INSTALL_DIR=/usr/kde/4/share/apps/$(PROJECT_NAME)

all: build
build:
	pykde4uic -o ui_mainwidget.py mainwidget.ui
	pykde4uic -o ui_mainwindow.py mainwindow.ui
	pykde4uic -o ui_progressdialog.py progressdialog.ui
	pyrcc4 data.qrc -o data_rc.py
clean:
	rm *.pyc ui_mainwidget.py ui_mainwindow.py ui_progressdialog.py data_rc.py
install: uninstall
	mkdir -p $(INSTALL_DIR)
	install -m 0755 main.py $(INSTALL_DIR)/$(PROJECT_NAME)
	ln -s $(INSTALL_DIR)/$(PROJECT_NAME) $(INSTALL_DIR)/$(PROJECT_NAME).py
	install -m 0644 about.py $(INSTALL_DIR)
	install -m 0644 data_rc.py $(INSTALL_DIR)
	install -m 0644 grouplist.py $(INSTALL_DIR)
	install -m 0644 mainwidget.py $(INSTALL_DIR)
	install -m 0644 mainwindow.py $(INSTALL_DIR)
	install -m 0644 packagedelegate.py $(INSTALL_DIR)
	install -m 0644 packagemodel.py $(INSTALL_DIR)
	install -m 0644 packageproxy.py $(INSTALL_DIR)
	install -m 0644 packageview.py $(INSTALL_DIR)
	install -m 0644 pmutils.py $(INSTALL_DIR)
	install -m 0644 rowanimator.py $(INSTALL_DIR)
	install -m 0644 statemanager.py $(INSTALL_DIR)
	install -m 0644 ui_mainwidget.py $(INSTALL_DIR)
	install -m 0644 ui_mainwindow.py $(INSTALL_DIR)
uninstall:
	rm -rf $(INSTALL_DIR)
