#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os
import re
import sys

releases = []
tasks = []
projectName = ""

projectre = re.compile('== (.*) ==$')
mainre = re.compile('\* (.*) \((.*)\)$')
subre = re.compile('  \* (.*) \((.*)\)$')
datere = re.compile('\> (.*)\t(.*)')

calendarTemplate = """
      <h1>Calendar</h1>

      <table cellspacing="0">
        <tr class="head">
          <th>Release</th>
          <th>Date</th>
        </tr>

        %s

      </table>
"""

statusTemplate = """
      <h1>Status</h1>
      <div style="margin:8px"></div>
      <div class="milestone">
        <div class="prog-border">
          <div class="prog-bar" style="width: %(totalCompleted)s%%;"></div>
        </div>
        <span class="prog-percent">%%%(totalCompleted)s</span>
        <dl>
          <dt>Tasks Finished:</dt>
          <dd><a href="">%(tasksFinished)s</a></dd>
          <dt>Task Inprogress:</dt>
          <dd><a href="">%(tasksInProgress)s</a></dd>
          <dt>Deadline:</dt>
          <dd><a href="">%(deadline)s</a></dd>
        </dl>
      </div>
"""

htmlTemplate = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
  <head>
    <title>%(projectName)s Tasks</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <link rel="stylesheet" href="tasks.css" type="text/css" />
    </head>

    <body>

      <h1 style="font-size:30px">%(projectName)s</h1>

       %(calendar)s

       %(status)s

      <h1>Tasks</h1>
      <div style="width:688px" class="tasks">
        <ul>
           %(tasks)s
        </ul>
      </div>
    </body>
</html>
"""

releaseTemplate = """
        <tr>
          <td>%s</td>
          <td>%s</td>
        </tr>
"""

taskTemplate = """
          <li>
            <div class="bar">
              <span class="text"><strong>%(task)s</strong> (<a href="">%(owner)s</a>)</span>
              <span class="percent">%%%(percent)s</span>
              <div>
                <div style="width:%(width)s%%"></div>
              </div>
            </div>
            <ul>
               %(subTasks)s
            </ul>
          </li>
"""

subTaskTemplate = """
              <li>%s</li>
"""

class Task:
    def __init__(self):
        self.summary = None
        self.owner = None
        self.subTasks = []
        self.completed = 0
        self.percent = 0

def getReleases():
    relhtml = ""
    for r in releases:
        relhtml += releaseTemplate % (r[0], r[1]) + "\n"
    return relhtml

def getTaskAndStatus():
    taskshtml = ""
    totalPercent = 0
    tasksFinished = 0
    for t in tasks:
        totalPercent += t.percent
        subshtml = ""
        for s in t.subTasks:
            if s[1] == "+":
                subshtml += "<font style='color:green'>" + subTaskTemplate % s[0] + "</font>\n"
            elif s[1] == "-":
                subshtml += "<font style='color:red'>" + subTaskTemplate % s[0] + "</font>\n"
            elif s[1] == "X":
                subshtml += "<font style='color:orange'>" + subTaskTemplate % s[0] + "</font>\n"
            else:
                subshtml += "<font style='color:darkblue'>" + subTaskTemplate % s[0] + "</font>\n"

        if t.percent >= 10:
            taskshtml += taskTemplate % {"task":t.summary,"owner":t.owner,"width":t.percent,"percent":t.percent,"subTasks":subshtml} + "\n"
        else:
            taskshtml += taskTemplate % {"task":t.summary,"owner":t.owner,"width":t.percent,"percent":"%d&nbsp&nbsp"%t.percent,"subTasks":subshtml} + "\n"

        if t.percent == 100:
            tasksFinished += 1

    return taskshtml, totalPercent / len(tasks), tasksFinished

def generateWiki(projectName, tasksFile):
    f = open(tasksFile+".wiki", "w")
    for t in tasks:
        f.write("* '''%s''' (%s)\n" % (t.summary, t.owner))
        for s in t.subTasks:
            if s[1] == "+":
                f.write("** {{Done|%s}}\n" % s[0])
            elif s[1] == "-":
                f.write("** {{todo|%s}}\n" % s[0])
            elif s[1] == "X":
                f.write("** {{onhold|%s}}\n" % s[0])
            else:
                percent = int(s[1][1:])
                # we have inprogress{25,50,75,100}.jpegs
                if percent % 25:
                    percent = ((percent / 25) + 1) * 25
                f.write("** {{Inprogress|%s|%s}}\n" % (percent, s[0]))
        f.write("<br>\n")
    f.close()

""" This function needs major rewrite """
def generateHtml(projectName, tasksFile):
    f = open(tasksFile+".html", "w")
    calendar = calendarTemplate % getReleases()
    taskshtml, percent, tasksFinished = getTaskAndStatus()
    tasksInProgress = len(tasks) - tasksFinished
    deadline = "What?"

    status = statusTemplate % {"totalCompleted":percent,
                            "tasksFinished":tasksFinished,
                            "tasksInProgress":tasksInProgress,
                            "deadline":deadline}

    if releases:
        deadline = releases[0][1]
    else:
        calendar = ""
        status = ""

    f.write(htmlTemplate % {"projectName": projectName,"calendar":calendar, "status": status, "tasks":taskshtml})
    f.close()

def parseTasksAndGenerateHtml(tasksFile):
    global projectName

    currentTask = None
    for line in open(tasksFile, "r").readlines():
        if line.startswith(">"):
            m = datere.match(line)
            if m:
                releases.append((m.group(1).strip(), m.group(2)))

        if line.startswith("*"):
            if currentTask != None:
                if currentTask.subTasks:
                    currentTask.percent = currentTask.completed / len(currentTask.subTasks)
                tasks.append(currentTask)

            currentTask = Task()
            m = mainre.match(line)
            if m:
                currentTask.summary = m.group(1)
                currentTask.owner = m.group(2)

        if line.startswith("  *"):
            m = subre.match(line)
            if m:
                currentTask.subTasks.append((m.group(1), m.group(2)))
                if m.group(2) == "+":
                    currentTask.completed += 100
                elif m.group(2)[0] == "/":
                    currentTask.completed += int(m.group(2)[1:])

        if line.startswith("=="):
            m = projectre.match(line)
            if m:
                projectName = m.group(1)

    if currentTask.subTasks:
        currentTask.percent = currentTask.completed / len(currentTask.subTasks)
    tasks.append(currentTask)

    generateHtml(projectName, tasksFile)
    generateWiki(projectName, tasksFile)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: parsetasks.py tasksfile"
        print '       ex: parsetasks.py pardus-2009'
        sys.exit(1)
    parseTasksAndGenerateHtml(sys.argv[1])
