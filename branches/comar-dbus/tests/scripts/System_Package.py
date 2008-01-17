#!/usr/bin/python
# -*- coding: utf-8 -*-

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    notify("System.Package", "Installed", script())
    return True

def preRemove():
    notify("System.Package", "Removed", script())
    return True
