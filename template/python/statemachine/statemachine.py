class StateMachine:

    def __init__(self, initialState, transitionTable):
        self.state = initialState
        self.transitionTable = transitionTable

    def nextState(self):

        print(f"State {self.state}")
        for condition, transition , nextState in self.transitionTable.get(self.state):
     
            if not condition(): continue

            transition()
            self.state = nextState
            return self.state

        raise ValueError("No Condition fulfilled")