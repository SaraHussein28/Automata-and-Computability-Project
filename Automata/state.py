import Utils.constants as constant

class State:
    name = ""
    transitions = []
    isInitial = False
    isFinal = False

    def __init__(self, name, isInitial, isFinal, transitions):
        self.name = name
        self.isInitial = isInitial
        self.isFinal = isFinal
        self.transitions = transitions
    
    def __str__(self):
        string = self.name 
        return string



