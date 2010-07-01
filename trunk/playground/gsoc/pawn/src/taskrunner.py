from PyQt4 import QtCore

from logger import getLogger
log = getLogger("TaskRunner")

class Task(QtCore.QThread):
    '''
    Qt-Threaded task.
    '''
    def __init__(self, method = None, description = None, callback = None):
        QtCore.QThread.__init__(self)
        self.method = method
        self.description = description
        self.callback = callback

    def run(self):
        if callable(self.method):
            self.method()
        else:
            log.warning("Non-callable method on %s" % self.description)

    def onFinish(self):
        self.finished = True

        if callable(self.callback):
            self.callback()
        else:
            log.warning("Non-callable callback received on %s" % self.description)

    def isFinished(self):
        return self.finished

class TaskList():
    tasks = []

    def __init__(self, name = None, description = None, tasks = None):
        if tasks: self.tasks = tasks
        if name: self.name = name
        if description: self.description = description

        self.index = 0
        self.finished = False

    def empty(self):
        self.tasks = []

    def isFinished(self):
        return self.finished

    def getPercentage(self):
        return int((self.index * 1.0)/ len(self.tasks) * 100)

    def start(self):
        self.index = 0
        self.finished = False
        self.startNext()

    def done(self):
        self.finished = True

    def startNext(self):
        if self.index == len(self.tasks):
            self.done()
            return

        curTask = self.tasks[self.index]
        self.index += 1

        curTask.start()
        if(curTask.wait()):
            curTask.onFinish()

    def queue_task(self, task):
        if isinstance(task, Task):
            self.tasks.append(task)
