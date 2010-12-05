all:
	pyrcc4 lider/data.qrc > lider/data_rc.py
	
	pyuic4 lider/main.ui > lider/ui_main.py
	
	pyuic4 lider/screens/connection/bookmarks/connection.ui > lider/screens/connection/bookmarks/ui_connection.py
	
	pyuic4 lider/screens/misc/logs/logs.ui > lider/screens/misc/logs/ui_logs.py
	pyuic4 lider/screens/misc/help/help.ui > lider/screens/misc/help/ui_help.py
	pyuic4 lider/screens/misc/about/about.ui > lider/screens/misc/about/ui_about.py
	
	pyuic4 lider/screens/network/tree/tree.ui > lider/screens/network/tree/ui_tree.py
	pyuic4 lider/screens/network/tree/minitree.ui > lider/screens/network/tree/ui_minitree.py
	
	pyuic4 lider/screens/network/search/search.ui > lider/screens/network/search/ui_search.py
	pyuic4 lider/screens/network/search/minisearch.ui > lider/screens/network/search/ui_minisearch.py
	
	pyuic4 lider/screens/node/software/software.ui > lider/screens/node/software/ui_software.py
	pyuic4 lider/screens/node/authentication/authentication.ui > lider/screens/node/authentication/ui_authentication.py
	
	pyuic4 lider/widgets/list_item/list_item.ui > lider/widgets/list_item/ui_list_item.py

clean:
	find . -name "*.pyc" | xargs rm -rf
	find . -name "ui_*.py" | xargs rm -rf
	find . -name "*_rc.py" | xargs rm -rf
