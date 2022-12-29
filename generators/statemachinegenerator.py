
def state_name(name : str) -> str:
    return 'state_'+ name[0].lower() + name[1:]

def class_name(name : str) -> str:
    return ''.join([name[0].upper() + name[1:]])


class StateMachineGenerator:

    def __init__(self,name):
        self.name = name
        self.states = []

    def add_state(self,name):
        self.states.append(name)

    def gen(self) -> str:
        template = ""
        #imports
        template += "from statemachine.statemachine import StateMachine\n"
        template += "from statemachine.state import State\n"
        template += "\n"

        template += f"class {class_name(self.name)}:\n"
        template += "\n"
        for state in self.states:
            template += f'\t{state_name(state)} = State("{state}")\n'

        return template
