all:
	pyuic4 lider/formmain.ui > lider/ui_formmain.py
	pyuic4 lider/connection.ui > lider/ui_connection.py
	pyuic4 lider/computer.ui > lider/ui_computer.py
	pyuic4 lider/folder.ui > lider/ui_folder.py
	pyrcc4 lider/data.qrc > lider/data_rc.py
	
	pyuic4 plugins/plugin_authentication/authentication.ui > plugins/plugin_authentication/ui_authentication.py
	pyrcc4 plugins/plugin_authentication/authentication.qrc > plugins/plugin_authentication/authentication_rc.py
	
	pyuic4 plugins/plugin_services/services.ui > plugins/plugin_services/ui_services.py
	pyrcc4 plugins/plugin_services/services.qrc > plugins/plugin_services/services_rc.py
	
	pyuic4 plugins/plugin_software/software.ui > plugins/plugin_software/ui_software.py
	pyrcc4 plugins/plugin_software/software.qrc > plugins/plugin_software/software_rc.py
	pyuic4 plugins/plugin_software/repository.ui > plugins/plugin_software/ui_repository.py
	
	pyuic4 plugins/plugin_summary/summary.ui > plugins/plugin_summary/ui_summary.py
	pyrcc4 plugins/plugin_summary/summary.qrc > plugins/plugin_summary/summary_rc.py
	
	pyuic4 plugins/plugin_web/web.ui > plugins/plugin_web/ui_web.py
	pyrcc4 plugins/plugin_web/web.qrc > plugins/plugin_web/web_rc.py

clean:
	find . -name "*.pyc" | xargs rm -rf
	find . -name "ui_*.py" | xargs rm -rf
	find . -name "*_rc.py" | xargs rm -rf
