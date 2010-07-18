from PyQt4 import QtCore

import logger
log = logger.getLogger("TaskRunner")

class Task(QtCore.QThread):
    "Threaded task using QThread class of Qt."
    description, method, callback = None, None, None
    
    def __init__(self, method = None, description = None, callback = None):
        QtCore.QThread.__init__(self)
        self.method = method
        self.description = description
        self.callback = callback

    def run(self):
        if callable(self.method): self.method()
        else: log.warning("Non-callable method on %s" % self.description)

    def onFinish(self):
        self.finished = True

        if callable(self.callback):
            self.callback()
        else:
            log.warning("Non-callable callback received on %s"%self.description)

    def isFinished(self):
        return self.finished

    def __repr__(self):
        return 'Task: %s' % self.description

class TaskList():
    "Execution framework for Task threads."
    tasks = []
    currentTask = None

    def __init__(self, name = None, tasks = None, callback = None):
        self.setTasks(tasks)
        if name: self.name = name
        self.callback = callback
        
        self.finished = False
        self.index = 0

    def setTasks(self, tasks):
        if isinstance(tasks,list): self.tasks = tasks

    def empty(self):
        self.tasks = []

    def isFinished(self):
        return self.finished

    def getPercentage(self):
        try:
            return int((self.index * 1.0)/ (len(self.tasks)) * 100)
        except ZeroDivisionError:
            return 0

    def start(self):
        self.index = 0
        self.finished = False
        self.startNext()

    def done(self):
        self.finished = True
        self.callback()

    def startNext(self):
        if callable(self.callback): self.callback() # on advance signal
        if self.index == len(self.tasks):
            self.done()
            return

        self.currentTask = self.tasks[self.index]
        self.index += 1

        log.info('Starting task: %s' % self.currentTask.description)
        self.currentTask.start()
        if(self.currentTask.wait()):
            self.currentTask.onFinish()

    def queue_task(self, task):
        if isinstance(task, Task):
            self.tasks.append(task)
