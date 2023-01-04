

from statemachine.statemachine import StateMachine
from statemachine.state import State


def test_state_machine():

    state_init = State("Init")
    state_close = State("Close")

    #Conditions
    def always_true():
        return True

    #Transitions
    def nop():
        pass


    sm = StateMachine(state_init, {
        state_init : [(always_true , nop, state_close)]
    })


    sm.nextState()

    assert sm.state == state_close
