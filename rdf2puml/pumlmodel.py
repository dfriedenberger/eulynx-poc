from .group import Group

def create_unique_id(o):
    s = str(o).split('#')[-1]
    return s.replace("/","_").replace("-","_").replace(":","_")



class PumlModel:

    def __init__(self,title):
        self.puml = []
        self.nodes = Group(None)
        self.components = Group(None)
        self.relations = []
        self.component_uses = []
        self.puml.append("@startuml")
        self.puml.append("!include c4/C4.puml")
        self.puml.append("!include nano/nanoservices.puml")
        self.puml.append(f"title {title}")
        self.puml.append("LAYOUT_TOP_DOWN")

        self.cache = set()

    def create_node(self,node,name,type,group):
        id = create_unique_id(node)
        if id in self.cache: #already created
            return

        #T = "Unknown"
        #if type in ["Process","Message","Interface","Service"]:
        #    
        T = type

        puml_obj = f'{T}({id}, "{name}","{type}")'

        self.nodes.append(group,puml_obj)
        self.cache.add(id)

    def create_relation(self,node1,node2,name = " "):
        id1 = create_unique_id(node1)
        id2 = create_unique_id(node2)
        puml_rel = f'Rel_D({id1}, {id2},"{name}")'
        self.relations.append(puml_rel)

    # state machines
    def create_state(self,state):
        self.puml.append(f"state {state}")

    def create_transition(self,source_state,target_state,description):
        self.puml.append(f"{source_state} --> {target_state} : {description}")

    def create_initial_state(self,state):
        self.puml.append(f"[*] --> {state}")

    def create_final_state(self,state):
        self.puml.append(f"{state} --> [*]")


    def create_component(self,id,name,package,pattern):

        component_obj = f'\tcomponent {id} <<{pattern}>> [{name}\n'
        # component_obj += f'\t\t  \n' Add Multiline description
        component_obj += '\t]'
        self.components.append([package],component_obj)

    def create_component_use(self,id,used_id):
        puml_use = f'[{id}] --> [{used_id}] : use'
        self.component_uses.append(puml_use)
  


    def finish(self):

        self.puml.extend(self.nodes.to_puml_package())
        self.puml.extend(self.relations)
        self.puml.extend(self.components.to_puml_package())
        self.puml.extend(self.component_uses)
        self.puml.append("@enduml")
        return self.puml

    def serialize(self,filename):
        textfile = open(filename, "w")
        for element in self.puml:
            textfile.write(element + "\n")
        textfile.close()


