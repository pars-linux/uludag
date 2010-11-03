Firewall Manager
----------------

**Firewall Manager** is used for defining port blocking rules over a system's communication with other systems. These rules block or allow a connection attempt. These attempts may be either made by your system or a remote system. You can configure these rules via **Firewall Manager**.


Activating Firewall
-------------------

If the **Firewall Manager** is not activated in your system, you can activate it by clicking the 'Start Firewall' button at the top of the window. When a firewall is activated it starts to apply defined rules.  If a process in your system tries to open a blocked port, system will prevent it. Similarly, if a remote system tries to connect a blocked port on your system, your system will prevent it too.


Deactivating Firewall
---------------------

If the **Firewall Manager** is activated in your system, you can deactivate it by clicking the 'Stop Firewall' button at the top of the window. Once the firewall is stopped, it does not apply any rules.


Editing Incoming Connection Rules
---------------------------------

These are the rules restrict access to your system from remote systems. **Firewall Manager** blocks every connection attempt by default. In this section, allowed services are chosen. Once a service is allowed, remote systems can access to your system over this service.
Select the 'Incoming Connections' tab. **Firewall Manager** lists some service names. Select a service from the list then your system will accept connections to related process over that service's port. In order to allow a service (in other words a port is used by that service) check the checkbox near the service name. Uncheck the checkbox for removing allowance.

Note: To add an incoming connection rule **Firewall Manager** should be activated. In order to apply changes click the 'Apply' button at the bottom of the window.

Editing Outgoing Connection Rules
---------------------------------

These are the rules restrict your system's connections over a port. If a process in your system tries to open a connection with the listed (blocked) ports in this section, it will be blocked.
Select the 'Outgoing Connections' tab. In order to add a new rule click the '+' button. If you want to define a rule for only one port, write port and click 'Ok' button at the dialog. You also can define rules for port ranges, to do that write port range with '-' character between ports and click 'Ok' button. In order to cancel a rule uncheck the checkbox near the rule in the list.

Note: To add an outgoing connection rule **Firewall Manager** should be activated. In order to apply changes click the 'Apply' button at the bottom of the window.