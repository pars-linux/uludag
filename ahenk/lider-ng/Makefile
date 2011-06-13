all:
	pyrcc4 lider/data.qrc > lider/data_rc.py
	
	pyuic4 lider/main.ui -o lider/ui_main.py
	
	pyuic4 lider/connection.ui > lider/ui_connection.py
	
	pyuic4 lider/plugins/plugin_firewall/firewall.ui > lider/plugins/plugin_firewall/ui_firewall.py
	pyrcc4 lider/plugins/plugin_firewall/firewall.qrc > lider/plugins/plugin_firewall/firewall_rc.py
	
clean:
	find . -name "*.pyc" | xargs rm -rf
	find . -name "ui_*.py" | xargs rm -rf
	find . -name "*_rc.py" | xargs rm -rf
