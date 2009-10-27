#!/bin/sh

./hav.py register grub Boot.Loader scripts/Boot_Loader.py

./hav.py register module_init_tools Boot.Modules scripts/Boot_Modules.py

./hav.py register wireless_tools Net.Link scripts/Net_Link_w.py

./hav.py register net_tools Net.Link scripts/Net_Link_n.py

./hav.py register ppp Net.Link scripts/Net_Link_p.py

./hav.py register baselayout Net.Stack scripts/Net_Stack.py

./hav.py register baselayout User.Manager scripts/User_Manager.py

./hav.py register util_linux Time.Clock scripts/Time_Clock.py
