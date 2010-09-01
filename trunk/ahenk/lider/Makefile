all:
	pyuic4 formmain.ui > ui_formmain.py
	pyuic4 connection.ui > ui_connection.py
	pyuic4 computer.ui > ui_computer.py
	pyuic4 folder.ui > ui_folder.py
	pyrcc4 data.qrc > data_rc.py
	pyuic4 plugins/plugin_summary/summary.ui > plugins/plugin_summary/ui_summary.py
	pyrcc4 plugins/plugin_summary/summary.qrc > plugins/plugin_summary/summary_rc.py
	pyuic4 plugins/plugin_software/software.ui > plugins/plugin_software/ui_software.py
	pyrcc4 plugins/plugin_software/software.qrc > plugins/plugin_software/software_rc.py

clean:
	find . -name "*.pyc" | xargs rm -rf
	find . -name "ui_*.py" | xargs rm -rf
	find . -name "*_rc.py" | xargs rm -rf
