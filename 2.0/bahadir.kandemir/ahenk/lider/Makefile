all:
	pyuic4 lider/formmain.ui > lider/ui_formmain.py
	pyuic4 lider/connection.ui > lider/ui_connection.py
	pyuic4 lider/computer.ui > lider/ui_computer.py
	pyuic4 lider/search.ui > lider/ui_search.py
	pyuic4 lider/folder.ui > lider/ui_folder.py
	pyuic4 lider/user.ui > lider/ui_user.py
	pyrcc4 lider/data.qrc > lider/data_rc.py
	
	pyuic4 lider/widgets/list_item/list_item.ui > lider/widgets/list_item/ui_list_item.py
	
	pyuic4 lider/plugins/plugin_authentication/authentication.ui > lider/plugins/plugin_authentication/ui_authentication.py
	pyrcc4 lider/plugins/plugin_authentication/authentication.qrc > lider/plugins/plugin_authentication/authentication_rc.py
	
	pyuic4 lider/plugins/plugin_firewall/firewall.ui > lider/plugins/plugin_firewall/ui_firewall.py
	pyrcc4 lider/plugins/plugin_firewall/firewall.qrc > lider/plugins/plugin_firewall/firewall_rc.py
	
	pyuic4 lider/plugins/plugin_services/services.ui > lider/plugins/plugin_services/ui_services.py
	pyrcc4 lider/plugins/plugin_services/services.qrc > lider/plugins/plugin_services/services_rc.py
	
	pyuic4 lider/plugins/plugin_software/software.ui > lider/plugins/plugin_software/ui_software.py
	pyrcc4 lider/plugins/plugin_software/software.qrc > lider/plugins/plugin_software/software_rc.py
	pyuic4 lider/plugins/plugin_software/repository.ui > lider/plugins/plugin_software/ui_repository.py
	
	pyuic4 lider/plugins/plugin_summary/summary.ui > lider/plugins/plugin_summary/ui_summary.py
	pyrcc4 lider/plugins/plugin_summary/summary.qrc > lider/plugins/plugin_summary/summary_rc.py
	
	pyuic4 lider/plugins/plugin_web/web.ui > lider/plugins/plugin_web/ui_web.py
	pyrcc4 lider/plugins/plugin_web/web.qrc > lider/plugins/plugin_web/web_rc.py

clean:
	find . -name "*.pyc" | xargs rm -rf
	find . -name "ui_*.py" | xargs rm -rf
	find . -name "*_rc.py" | xargs rm -rf
