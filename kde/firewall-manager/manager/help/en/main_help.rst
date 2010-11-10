Firewall Manager
----------------

**Firewall Manager** is used for defining port blocking rules over a system's communication with other systems. These rules block or allow a connection attempt. These attempts may be either made by your system or a remote system. You can configure these rules via **Firewall Manager**.


Activating Firewall
-------------------

If the **Firewall Manager** is not activated in your system, you can activate it by clicking the 'Start' button at the top of the window. When a firewall is activated it starts to apply defined rules.  If a process in your system tries to open a blocked port, system will prevent it. Similarly, if a remote system tries to connect a blocked port on your system, your system will prevent it too.


Deactivating Firewall
---------------------

If the **Firewall Manager** is activated in your system, you can deactivate it by clicking the 'Stop' button at the top of the window. Once the firewall is stopped, it does not apply any rules.


Editing Incoming Connection Rules
---------------------------------

These are the rules restrict access to your system from remote systems. **Firewall Manager** blocks every connection attempt by default. In this section, allowed ports are chosen. Once a port is allowed, remote systems can access to your system over this port.
Select the 'Block Incoming Connections' item and click the edit button at the left side of the item. After that, settings window opens and **Firewall Manager** lists some ports if there are any allowed ports added before. You can add and remove ports by clicking the 'Add' and 'Remove' buttons. Now your system will accept connections to related process over these ports. If you want to change the order of the port control, you can do that by clicking the 'Move Up', 'Move Down' buttons. Click 'Ok' button to save and 'Cancel' button to discard.


Editing Outgoing Connection Rules
---------------------------------

These are the rules restrict your system's connections over a port. If a process in your system tries to open a connection with the listed (blocked) ports in this section, it will be blocked.
Select the 'Block Outgoing Connections' item and click the edit button at the left side of the item. Settings window appears and you see the blocked ports list. Configuration are made on this window. In order to add a port, write port number to the text box at the top of the list and click 'Add'. Select a port on the list and click 'Remove' to delete. Use 'Move Up' and 'Move Down' buttons to change cotrol order of the ports. Click 'Ok' button to save and 'Cancel' button to discard.

Using Your Computer As A Gateway
--------------------------------

Connect a computer in your local network to internet over your computer is possible. In this case your computer acts like a gateway.
In order to do gateway settings select the 'Sharing Internet' item and click the edit button at the right side of the item. Settings window opens and displays two lists. You should select related network interfaces from these lists. Select the network interface for your computer's internet connection from the first list. Your computer connects to internet over this interface. Secondly, select the interface for other computer's connection to your computer. Click 'Ok' button to save and 'Cancel' button to discard.
