
def state_name(name : str) -> str:
    return 'state_'+ name[0].lower() + name[1:]

def class_name(name : str) -> str:
    return ''.join([name[0].upper() + name[1:]])

def guard_func_name(guard : str) -> str:
    return 'is_'+guard.lower().replace(" ","_")

def transition_func_name(transition : str) -> str:
    return transition.lower().replace(" ","_")


class StateMachineGenerator:

    def __init__(self,name):
        self.name = name
        self.states = []
        self.initial_state = None
        self.final_states = []

        self.transitions = []
        self.guards = []
        self.config_map = {}


    def add_state(self,name):
        self.states.append(name)

    def set_initial_state(self,name):
        self.initial_state = name

    def add_final_state(self,name):
        self.final_states.append(name)

    def add_transition(self,transition_name,source_state_name,target_state_name,guard):

        if source_state_name not in self.config_map:
            self.config_map[source_state_name] = []

        self.config_map[source_state_name].append([transition_name,source_state_name,target_state_name,guard])

        if transition_name not in self.transitions:
            self.transitions.append(transition_name)

        if guard not in self.guards:
            self.guards.append(guard)
       
    def gen(self) -> str:
        template = ""
        #imports
        template += "from .statemachine import StateMachine\n"
        template += "from .state import State\n"
        template += "\n"

        template += f"class {class_name(self.name)}:\n"
        template += "\n"
        for state in self.states:
            template += f'\t{state_name(state)} = State("{state}")\n'
        template += f'\n'

    	#generate functions hubs
        # Conditions/Guards
        template += f'\t# Conditions/Guards\n'
        for guard in self.guards:
            template += f'\tdef {guard_func_name(guard)}(self):\n'
            template += f'\t\traise NotImplementedError("{guard_func_name(guard)} not implemented yet")\n'
            template += f'\n'

        # Transitions
        template += f'\t# Transitions\n'
        for transition in self.transitions:
            template += f'\tdef {transition_func_name(transition)}(self):\n'
            template += f'\t\traise NotImplementedError("{transition_func_name(transition)} not implemented yet")\n'
            template += f'\n'

    	# generate run function
        template += '\tdef run(self):\n'
        template += '\n'
        template += f'\t\tsm = StateMachine(self.{state_name(self.initial_state)}, [\n'
        l = len(self.final_states)
        for i in range(l):
            final_state = self.final_states[i]
            template += f'\t\t\t\tself.{state_name(final_state)},\n'
        template += f'\t\t\t] , {{\n'



        source_states = list(self.config_map.keys())
        li = len(source_states)
        for i in range(li):
            source_state = source_states[i]
            template += f'\t\t\tself.{state_name(source_state)}\t: [\n'
            transitions = self.config_map[source_state]
            lj = len(transitions)
            for j in range(lj):
                transition,_,target_state,guard = transitions[j]
                template += f'\t\t\t\t(self.{guard_func_name(guard)},self.{transition_func_name(transition)},self.{state_name(target_state)}),\n'            
            template += f'\t\t\t],\n'

        template += f'\t\t}})\n'
        template += f'\n'

        template += f'\t\twhile sm.nextState():\n'  
        template += f'\t\t\tpass\n'
        return template
