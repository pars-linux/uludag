
class StepWidget():
    heading = ''

    finishStep = False

    def __init__(self):
	pass

    def onEnter(self):
	pass

    def onSubmit(self):
	return True;

    def onRollback(self):
	return True;

    def nextIndex(self): #have to be implemented
	return -1

    def isFinishStep(self):
	return self.finishStep