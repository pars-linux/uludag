#!/usr/bin/python
# -*- coding: utf-8 -*-

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    notify("Installed", script())
    return True

def preRemove():
    notify("Removed", script())
    return True
