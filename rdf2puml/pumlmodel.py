from .nodegroup import NodeGroup

def create_unique_id(o):
    s = str(o).split('#')[-1]
    return s.replace("/","_").replace("-","_").replace(":","_")



class PumlModel:

    def __init__(self,title):
        self.puml = []
        self.nodes = NodeGroup(None)
        self.relations = []
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

    def create_relation(self,node1,node2):
        id1 = create_unique_id(node1)
        id2 = create_unique_id(node2)
        puml_rel = f'Rel_D({id1}, {id2}," ")'
        self.relations.append(puml_rel)

    def finish(self):

        self.puml.extend(self.nodes.to_puml_package())
        self.puml.extend(self.relations)
        self.puml.append("@enduml")
        return self.puml

    def serialize(self,filename):
        textfile = open(filename, "w")
        for element in self.puml:
            textfile.write(element + "\n")
        textfile.close()


