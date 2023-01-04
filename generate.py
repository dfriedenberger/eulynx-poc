from rdflib import Graph, RDF

from ontology.sparql_queries import SparQLWrapper
from ontology.namespace import MBA
from generators.messagegenerator import MessageGenerator
from generators.statemachinegenerator import StateMachineGenerator
from generators.project import Project

import argparse
import os
import shutil
from distutils.dir_util import copy_tree

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid path")


def parse_args():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Script for transform model to code.')
    parser.add_argument("--model", required=True,
                        metavar="INPUT", help="model")
    parser.add_argument("--path", required=True, type=dir_path,
                        metavar="PATH", help="project folder")
    args = parser.parse_args()

    return args.model , args.path 


def list_files(folder):
    files = []
    for e in os.listdir(folder):

        #Todo Exclude
        if e == "__pycache__": continue

        if os.path.isdir(os.path.join(folder, e)):
            for f in list_files(os.path.join(folder, e)):
                files.append(os.path.join(e,f))
        if os.path.isfile(os.path.join(folder, e)):
            files.append(e)
    return files

def read_content(filename):
    with open(filename) as f:
        return f.read()

def create_message_asset(wrapper,project,component):

    message = wrapper.get_single_out_reference(component,MBA.creates)
    target_path = wrapper.get_single_object_property(component,MBA.target_path)

    message_name = wrapper.get_single_object_property(message,MBA.name)
    print("Message",message_name)
    message_generator = MessageGenerator(message_name)

    for telegramm_structure in wrapper.get_out_references(message,MBA.structure):
        print("struct",telegramm_structure)
        for property in wrapper.get_sequence(telegramm_structure):
            property_name = wrapper.get_single_object_property(property,MBA.name)
            datatype = wrapper.get_single_object_property(property,MBA.datatype)
            message_generator.add_property(property_name,datatype)

    project.create_folder(target_path)
    project.create_file(os.path.join(target_path,f"{message_name}.py"),message_generator.gen())
  
def create_state_machine_asset(wrapper,project,component):

    state_machine = wrapper.get_single_out_reference(component,MBA.creates)
    target_path = wrapper.get_single_object_property(component,MBA.target_path)

    state_machine_name = wrapper.get_single_object_property(state_machine,MBA.name)+"StateMachine"

    print("StateMachine",state_machine_name)

    # TODO code duplicate to rdf2puml
    state_machine_generator = StateMachineGenerator(state_machine_name)
    state_machine_states = set()

    for state in wrapper.get_out_references(state_machine,MBA.has):
        state_machine_states.add(state)
        state_name = wrapper.get_single_object_property(state,MBA.name)
        state_machine_generator.add_state(state_name)
        init_properties = wrapper.get_object_properties(state,MBA.init)
        if len(init_properties) > 0:
            state_machine_generator.set_initial_state(state_name)
        final_properties = wrapper.get_object_properties(state,MBA.final)
        if len(final_properties) > 0:
            state_machine_generator.add_final_state(state_name)

    for transition in wrapper.get_instances_of_type(MBA.Transition): 
        transition_name = wrapper.get_single_object_property(transition,MBA.name)
        source_state = wrapper.get_out_references(transition,MBA.source)[0]
        target_state = wrapper.get_out_references(transition,MBA.target)[0]
        guards = wrapper.get_object_properties(transition,MBA.guard)
        guard = " and ".join(guards)

        # Check if states belongs to state machine
        if source_state in state_machine_states or target_state in state_machine_states:
            source_state_name = wrapper.get_single_object_property(source_state,MBA.name)
            target_state_name = wrapper.get_single_object_property(target_state,MBA.name)
            state_machine_generator.add_transition(transition_name,source_state_name,target_state_name,guard)

    project.create_folder(target_path)
    project.create_file(os.path.join(target_path,f"{state_machine_name}.py"),state_machine_generator.gen())
   
def create_library_asset(wrapper,project,component):

    project_reference = wrapper.get_single_object_property(component,MBA.project_ref)
    target_path = wrapper.get_single_object_property(component,MBA.target_path)

    ## if project_reference is directory
    if not os.path.isdir(project_reference):
        raise ValueError(f"Only template directories are supported. {project_reference} is not readable")
    

    project.create_folder(target_path)
    result = list_files(project_reference)
    for file in result:
        content = read_content(os.path.join(project_reference,file))
        project.create_file(os.path.join(target_path,file),content)
    

component_creator = {
    "state machine" : create_state_machine_asset,
    "message" : create_message_asset,

    "lib" : create_library_asset

}


model , path = parse_args();

graph = Graph()
graph.parse(model)


wrapper = SparQLWrapper(graph)

rootProject = Project("Root",path)

for package in wrapper.get_instances_of_type(MBA.Package):
    package_name = wrapper.get_single_object_property(package,MBA.name)

    project = rootProject.create_project(package_name)
    project.init()

    for component in wrapper.get_out_references(package,MBA.contains):
        pattern = wrapper.get_single_object_property(component,MBA.pattern)
        print("Create",pattern,"in",package_name)

        if pattern not in component_creator:
            raise ValueError(f'Pattern "{pattern}" is unknown')
        component_creator[pattern](wrapper,project,component)


