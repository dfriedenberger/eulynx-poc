class StateMachine:

    def __init__(self, initialState, finalStates,transitionTable):
        self.state = initialState
        self.finalStates = finalStates
        self.transitionTable = transitionTable

    def nextState(self):

        #print(f"State {self.state}")
        for condition, transition , nextState in self.transitionTable.get(self.state):

            if not condition(): continue

            transition()
            self.state = nextState

            if self.state in self.finalStates:
                return False # Finish
            return True # Still Running

        print("State",self.state,"len=",len(self.transitionTable.get(self.state)))
        for condition, transition , nextState in self.transitionTable.get(self.state):
            print("Condition",condition.__name__,"=",condition())

        raise ValueError("No Condition fulfilled")