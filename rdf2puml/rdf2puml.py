from rdflib import URIRef, Graph

from .pumlmodel import PumlModel
from ontology.sparql_queries import SparQLWrapper
from ontology.namespace import MBA
from typing import List


def get_name(wrapper,instance):
    names = wrapper.get_object_properties(instance,MBA.name)
    return "/".join(names)

def get_type(wrapper,instance):
    return wrapper.get_type(instance).split("#")[1]

def get_id(instance):
    return str(instance).split("#")[1].replace("-","")

def rdf2puml(graph : Graph) -> PumlModel:

    puml = PumlModel("Architecture")
    wrapper = SparQLWrapper(graph)

    for instance in wrapper.get_instances():
        name = get_name(wrapper,instance)
        type = get_type(wrapper,instance)

        puml.create_node(instance,name,type,["EULYNX"])

    for (n1,n2) in wrapper.get_references():
        puml.create_relation(n1,n2)

    puml.finish()
    return puml 

def statemachines2puml(graph : Graph) -> List[PumlModel]:
    puml_models = {}
    wrapper = SparQLWrapper(graph)

    for state_machine in wrapper.get_instances_of_type(MBA.StateMachine):
        state_machine_name = get_name(wrapper,state_machine)
        state_machine_states = set()

        puml = PumlModel(state_machine_name)
        for state in wrapper.get_out_references(state_machine,MBA.has):
            state_machine_states.add(state)
            name = get_name(wrapper,state)
            puml.create_state(name)
            init_properties = wrapper.get_object_properties(state,MBA.init)
            if len(init_properties) > 0:
                puml.create_initial_state(name)
            final_properties = wrapper.get_object_properties(state,MBA.final)
            if len(final_properties) > 0:
                puml.create_final_state(name)


        for transition in wrapper.get_instances_of_type(MBA.Transition): 
            transition_name = get_name(wrapper,transition)
            source_state = wrapper.get_out_references(transition,MBA.source)[0]
            target_state = wrapper.get_out_references(transition,MBA.target)[0]
            guards = wrapper.get_object_properties(transition,MBA.guard)
            guard = " and ".join(guards)

            # Check if states belongs to statemachine
            if source_state in state_machine_states or target_state in state_machine_states:
                source_state_name = get_name(wrapper,source_state)
                target_state_name = get_name(wrapper,target_state)

                puml.create_transition(source_state_name,target_state_name,f"[{guard}] / {transition_name}")
            
        



        puml.finish()
        puml_models[state_machine_name] = puml


    return puml_models

def packages2puml(graph : Graph) -> PumlModel:
    puml = PumlModel("Components")
    wrapper = SparQLWrapper(graph)
    
    for package in wrapper.get_instances_of_type(MBA.Package):
        package_name = get_name(wrapper,package)

        for component in wrapper.get_out_references(package,MBA.contains):
            component_name = get_name(wrapper,component)
            pattern = wrapper.get_single_object_property(component,MBA.pattern)
            puml.create_component(get_id(component),component_name,package_name,pattern)

            #use
            for used_component in wrapper.get_out_references(component,MBA.use):
                puml.create_component_use(get_id(component),get_id(used_component))

    puml.finish()
    return puml 