#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

import comariface
from dialog import *

_ = lambda x: x

def menuScan(script, device):
    menu = []
    
    dia.showMessage(_("Scanning remotes. This may take a while."))
    
    remotes = link.getRemotes(script, device)
    
    if len(remotes):
        for remote in remotes:
            name, quality, mac = remote.split()
            menu.append(dialogListEntry(name, "%s %s" % (name, mac), quality))
        ret = dia.showList(_("Select remote"), menu)
        if ret == None:
            return
        else:
            return ret.value
    else:
        dia.showMessage(_("No remotes found."))

def menuAuthentication(script, mode, value, methods):
    menu = []
    default = "1"
    
    menu.append(dialogListEntry(_("No Authentication"), "__no__"))
    
    for method in methods.split(";"):
        name, field, label = method.split(",")
        if mode == name:
            default = str(len(menu) + 1)
        menu.append(dialogListEntry(label, name))
    
    while 1:
        ret = dia.showList(_("Select authentication mode"), menu, default)
        if ret == None:
            return
        elif ret.value == "__no__":
            return "", ""
        else:
            auth_method = ret.value
            break
    
    if auth_method == "login":
        username, password = "", ""
        if "\n" in value:
            username, password = value.split("\n")
        menu = []
        menu.append(dialogListEntry(_("Username"), "username", username))
        menu.append(dialogListEntry(_("Password"), "password", password))
        menu.append(dialogListEntry(_("Done"), "done"))
        while 1:
            ret = dia.showList(_("Enter details"), menu)
            if ret == None:
                return
            elif ret.value == "username":
                username = dia.showInputBox(_("Enter username"), username)
                if username:
                    ret.data = username
            elif ret.value == "password":
                password = dia.showInputBox(_("Enter password"), password)
                if password:
                    ret.data = password
            elif ret.value == "done":
                return auth_method, "%s\n%s" % (username, password)
    else:
        ret = dia.showInputBox(_("Enter password"), value)
        if ret == "":
            return
        else:
            return auth_method, ret

def menuConnectionAddress(mode="", address="", mask="", gateway="", methods=[]):
    default = "1"
    if mode == "manual":
        default = "2"
    
    menu = []
    if "auto" in methods:
        menu.append(dialogListEntry(_("Auto get IP from DHCP"), "auto"))
    if "manual" in methods:
        menu.append(dialogListEntry(_("Use a static IP"), "manual"))
    
    while 1:
        ret = dia.showList(_("Dynamic or static IP?"), menu, default)
        if ret == None:
            return
        elif ret.value == "auto":
            return "auto"
        else:
            break
    
    data = {"address": address, "mask": mask, "gateway": gateway}
    menu = []
    menu.append(dialogListEntry(_("Set IP"), "address", data.get("address", "")))
    menu.append(dialogListEntry(_("Set Mask"), "mask", data.get("mask", "")))
    menu.append(dialogListEntry(_("Set Gateway"), "gateway", data.get("gateway", "")))
    menu.append(dialogListEntry(_("Done"), "done"))
    
    while 1:
        ret = dia.showList(_("Enter details."), menu)
        if ret == None:
            return
        elif ret.value == "address":
            data["address"] = dia.showInputBox(_("Enter IP"), data.get("address", ""))
            ret.data = data["address"]
        elif ret.value == "mask":
            data["mask"] = dia.showInputBox(_("Enter mask"), data.get("mask", ""))
            ret.data = data["mask"]
        elif ret.value == "gateway":
            data["gateway"] = dia.showInputBox(_("Enter gateway"), data.get("gateway", ""))
            ret.data = data["gateway"]
        elif ret.value == "done":
            return "manual,%s,%s,%s" % (data["address"], data["mask"], data["gateway"])

def menuConnectionCommon(data):
    menu = []
    scriptInfo = link.getScriptInfo(data["script"])
    modes = scriptInfo["modes"].split(",")
    address_methods = []
    
    data["auth_mode"] = None
    data["auth_password"] = ""
    if data["name"]:
        auth_mode = link.getAuthentication(data["script"], data["name"])
        if auth_mode:
            data["auth_mode"] = auth_mode[1]
            if data["auth_mode"] == "login":
                data["auth_password"] = "%s\n%s" % (auth_mode[2], auth_mode[3])
            else:
                data["auth_password"] = auth_mode[2]
    
    menu.append(dialogListEntry(_("Name"), "name", data.get("name", "")))
    
    if "remote" in modes:
        menu.append(dialogListEntry(scriptInfo["remote_name"], "remote", data.get("remote", "")))
    if "net" in modes or "auto" in modes:
        menu.append(dialogListEntry(_("IP Address"), "net_mode", data.get("net_mode", "")))
        if "net" in modes:
            address_methods.append("manual")
        if "auto" in modes:
            address_methods.append("auto")
    if "scan" in modes:
        menu.append(dialogListEntry(_("Scan"), "scan"))
    if "auth" in modes:
        menu.append(dialogListEntry(_("Authentication"), "auth", data.get("auth_mode", "")))
    
    menu.append(dialogListEntry(_("Done"), "done"))
    
    while 1:
        ret = dia.showList(_("Enter connection details"), menu)
        if ret == None:
            return
        elif ret.value == "name":
            data["name"] = dia.showInputBox(_("Name"), data.get("name", ""))
            ret.data = data["name"]
        elif ret.value == "remote":
            data["remote"] = dia.showInputBox(scriptInfo["remote_name"], data.get("remote", ""))
            ret.data = data["remote"]
        elif ret.value == "net_mode":
            address = menuConnectionAddress(data.get("net_mode", ""),
                                            data.get("net_address", ""),
                                            data.get("net_mask", ""),
                                            data.get("net_gateway", ""),
                                            address_methods)
            if not address:
                return
            if address.startswith("manual"):
                data["net_mode"], data["net_address"], data["net_mask"], data["net_gateway"] = address.split(",")
            else:
                data["net_mode"] = "auto"
                data["net_address"], data["net_mask"], data["net_gateway"] = "", "", ""
            ret.data = data["net_mode"]
        elif ret.value == "scan":
            scan = menuScan(data["script"], data["device_id"])
            if scan:
                data["remote"] = scan
                for x in menu:
                    if x.value == "remote":
                        x.data = scan
        elif ret.value == "auth":
            auth = menuAuthentication(data["script"], data.get("auth_mode", ""), data.get("auth_password", ""), scriptInfo["auth_modes"])
            if auth:
                data["auth_mode"], data["auth_password"] = auth
                if data["auth_mode"] == "":
                    ret.data = _("No")
                else:
                    ret.data = data["auth_mode"]
        elif ret.value == "done":
            link.setConnection(script=data["script"],
                               name=data["name"],
                               device=data["device_id"],
                               mode=data.get("net_mode", None),
                               address=data.get("net_address", None),
                               mask=data.get("net_mask", None),
                               gateway=data.get("net_gateway", None),
                               remote=data["remote"],
                               auth_mode=data["auth_mode"],
                               auth_value=data["auth_password"])
            return True
            break

def menuEditConnection(script, name):
    connInfo = link.getConnectionInfo(script, name)
    return menuConnectionCommon(connInfo)

def menuNewConnection():
    menu = []
    for script in link.getScripts():
        if not len(link.getDevices(script)):
            continue
        info = link.getScriptInfo(script)
        menu.append(dialogListEntry(info["name"], script))
    
    if not len(menu):
        dia.showMessage(_("No Net.Link package found."))
        return
    
    while 1:
        ret = dia.showList(_("Select a connection type"), menu)
        if ret == None:
            return
        else:
            break
    
    script = ret.value
    scriptInfo = link.getScriptInfo(script)
    menu = []
    for id, label in link.getDevices(script).iteritems():
        menu.append(dialogListEntry(label, id))
    
    while 1:
        ret = dia.showList(_("Select a device"), menu)
        if ret == None:
            return
        else:
            break
    
    device = ret.value
    
    return menuConnectionCommon({"script": script, "device_id": device, "name": ""})

def menuEditConnections():
    menu = []
    updated = False
    
    for connection in link.getConnections():
        script, name = connection.split(" ", 1)
        menu.append(dialogListEntry(name, connection))
    
    menu.append(dialogListEntry(_("New Connection..."), "__new__"))
    
    while 1:
        ret = dia.showList(_("Select a connection or create new one."), menu)
        if ret == None:
            return
        elif ret.value == "__new__":
            updated = menuNewConnection()
            if updated:
                break
        else:
            script, name = ret.value.split(" ", 1)
            menuEditConnection(script, name)
    
    if updated:
        menuConnections()

def menuViewConnections():
    menu = []
    scripts = {}
    
    for connection in link.getConnections():
        script, name = connection.split(" ", 1)
        state = link.getConnectionInfo(script, name)["state"]
        menu.append(dialogListEntry(name, name, state))
        scripts[name] = script
    
    menu.append(dialogListEntry(_("Back"), "__back__"))
    
    while 1:
        ret = dia.showList(_("Select a connection and press OK to switch state."), menu)
        if ret == None:
            return
        elif ret.value == "__back__":
            return
        else:
            if ret.data.startswith("up"):
                state = "down"
            else:
                state = "up"
            link.setState(ret.value, state)
            ret.data = state

def menuMain():
    menu = [
        dialogListEntry(_("View Connections"), "view_connections"),
        dialogListEntry(_("Edit Connections"), "edit_connections"),
        dialogListEntry(_("Exit"), "exit"),
    ]
    
    while 1:
        ret = dia.showList(_("Select an item"), menu)
        if ret == None:
            return
        elif ret.value == "edit_connections":
            menuEditConnections()
        elif ret.value == "view_connections":
            menuViewConnections()
        elif ret.value == "exit":
            return

def main(args):
    global link, dia
    
    dia = dialog(_("Network Manager"))
    link = comariface.comarLink()
    
    menuMain()
    
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
