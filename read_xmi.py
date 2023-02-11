
import argparse
import xml.etree.ElementTree as ET
from ontology.namespace import MBA
from rdflib import Graph, RDF, URIRef
from ontology.graphwrapper import GraphWrapper


def map_states(type,name):
    if type == "uml:State":
        return MBA.State
    if type == "uml:FinalState":
        return MBA.FinalState
    if type == "uml:Pseudostate":
        if name.startswith("Initial"):
            return MBA.InitialState
        if name.startswith("Junction"):
            return MBA.Junction

    raise ValueError(f"Unknown Type {type}:{name}")

class StateMachineCreator:
    def __init__(self,name):
        self.name = name
        self.states = {}
        self.transitions = []

    def add_state(self,type,name,id):
        self.states[id] = type , name 

    def add_transition(self,source,target):
        self.transitions.append([source,target])

    def create(self,wrapper):
        
        rdf_state_machine = wrapper.add_named_instance(MBA.StateMachine,self.name)
        
        rdf_states = {}
        for id, (type , name)  in self.states.items():
            print("State",name,type)
            rdf_type = map_states(type,name)
            rdf_state = wrapper.add_named_instance(rdf_type,name,unique_name=f"{self.name}{name}")
            wrapper.add_reference(MBA.has,rdf_state_machine,rdf_state)

            
            #wrapper.add_str_property(MBA.init,rdf_state,"true")
            rdf_states[id] = rdf_state

        for source, target in self.transitions:
            print("Transition",self.states[source],"=>",self.states[target])
            name = self.states[source][1]+"-"+self.states[target][1]
            rdf_transition = wrapper.add_named_instance(MBA.Transition,name,unique_name=f"{self.name}{name}")
            wrapper.add_reference(MBA.source,rdf_transition,rdf_states[source])
            wrapper.add_reference(MBA.target,rdf_transition,rdf_states[target])
            #wrapper.add_str_property(MBA.guard,rdf_transition_initialize,"true")


    

    
   

    

    




def parse_args():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Script for transform model to code.')
    parser.add_argument("--xmi", required=True,
                        metavar="INPUT", help="model")
    parser.add_argument("--model", required=True,
                        metavar="INPUT", help="model")
    args = parser.parse_args()

    return args.xmi , args.model

xmi_type = "{http://www.omg.org/spec/XMI/20110701}type"
xmi_id = "{http://www.omg.org/spec/XMI/20110701}id"
def get_xmi_type(elem):
    if xmi_type in elem.attrib: 
        return elem.attrib[xmi_type] 
    return None 
def get_xmi_id(elem):
    if xmi_id in elem.attrib: 
        return elem.attrib[xmi_id] 
    return None 

def dump(elem):
    print("dump",elem.tag,get_xmi_type(elem))
    for e in elem:
        print(e.tag,get_xmi_type(e))

def parse_constraint(constraint):
    print("","",get_xmi_type(constraint),"=>",constraint.attrib['constrainedElement']) 
    for e in constraint:
        t = get_xmi_type(e)
        if e.tag == "specification" and t == "uml:OpaqueExpression":
            print("","","","Expression",e.attrib['body'])
        else:
            print("","","unknown Tag",e.tag,t)

def parse_state(sm,state):
    print("",get_xmi_type(state),state.attrib['name'],"id",get_xmi_id(state))
    sm.add_state(get_xmi_type(state),state.attrib['name'],get_xmi_id(state))
    for e in state:
        t = get_xmi_type(e)
        if e.tag == "region":
            parse_region(sm,e)
        elif e.tag == "ownedComment":
            print("","","Comment",e.attrib['body'])
        elif e.tag == "ownedRule" and t == "uml:Constraint":
            parse_constraint(e)
        elif e.tag == "entry" and t == "uml:Activity":
            print("","","Activity",e.attrib['name']) 
        else:
            print("","","unknown Tag",e.tag,t)

def parse_transition(sm,transition):
    print("",get_xmi_type(transition),transition.attrib['source'],"=>",transition.attrib['target'])
    sm.add_transition(transition.attrib['source'],transition.attrib['target'])

    for e in transition:
        t = get_xmi_type(e)
        if e.tag == "ownedComment":
            print("","","Comment",e.attrib['body'])
        elif e.tag == "trigger" and t == "uml:Trigger":
            print("","","Trigger","Event:",e.attrib['event'])
        elif e.tag == "effect" and t == "uml:OpaqueBehavior":
            print("","","Effect",e.attrib['body']) 
        elif e.tag == "ownedRule" and t == "uml:Constraint":
            parse_constraint(e)
        else:
            print("","","unknown Tag",e.tag,t)


def parse_region(sm,region):
    for e in region:
        t = get_xmi_type(e)
        if e.tag == "subvertex" and t == "uml:State":
            parse_state(sm,e)
        elif e.tag == "subvertex" and t == "uml:Pseudostate":
            parse_state(sm,e)
        elif e.tag == "subvertex" and t == "uml:FinalState":
            parse_state(sm,e)
        elif e.tag == "transition" and t == "uml:Transition":
            parse_transition(sm,e)
        else:
            print("Unknown region element",e.tag,get_xmi_type(e))


def parse_state_machine(state_machine,wrapper):
    print("StateMachine", state_machine.attrib['name'])
    sm = StateMachineCreator(state_machine.attrib['name'])
    for e in state_machine:
        if e.tag == 'region':
            parse_region(sm,e)
    sm.create(wrapper)

xmi_file , model = parse_args()


# XML-Datei lesen
tree = ET.parse(xmi_file)
root = tree.getroot()

# 

graph = Graph()
wrapper = GraphWrapper(graph)


for elem in root.iter("ownedBehavior"):

    t = get_xmi_type(elem) 
    if t == "uml:StateMachine":
        parse_state_machine(elem,wrapper)
    elif t == "uml:OpaqueBehavior":
        pass # ignore for the moment
    else:
        print("Unknown ownedBehavior type=",t)
   

graph.serialize(destination=model,format='turtle')
