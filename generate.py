from rdflib import Graph, RDF

from ontology.sparql_queries import SparQLWrapper
from ontology.namespace import MBA
from generators.messagegenerator import MessageGenerator
from generators.statemachinegenerator import StateMachineGenerator

import argparse
import os
import shutil

def parse_args():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Script for transform model to code.')
    parser.add_argument("--model", required=True,
                        metavar="INPUT",
                        help="model")
    args = parser.parse_args()

    return args.model

# Helper
def to_path(o):
    return o.lower().replace(' ','-')

def create_project(name):
    #TODO create project 
    project_path = f"tmp/{to_path(name)}"
    print(f"Implement Project {name} in path {project_path}")
    if not os.path.exists(project_path):
        os.mkdir(project_path)
    return project_path

def create_asset(asset,project_path):
    #TODO create asset 
    asset_template = asset_templates[asset]
    src_file = asset_template['template_path']
    dst_file = os.path.join(project_path,asset_template['filename'])
    print(f"Create Asset {asset} in path {project_path}")
    shutil.copyfile(src_file,dst_file)
    return dst_file


def create_message_asset(wrapper,message,project_path):
    message_name = wrapper.get_single_object_property(message,MBA.name)
    print("Message",message_name)
    message_generator = MessageGenerator(message_name)

    for telegramm_structure in wrapper.get_out_references(message,MBA.structure):
        print("struct",telegramm_structure)
        for property in wrapper.get_sequence(telegramm_structure):
            property_name = wrapper.get_single_object_property(property,MBA.name)
            datatype = wrapper.get_single_object_property(property,MBA.datatype)
            message_generator.add_property(property_name,datatype)

    dst_file = os.path.join(project_path,f"{message_name}.py")
    with open(dst_file, 'w') as f:
        f.write(message_generator.gen())

def create_state_machine_asset(wrapper,state_machine,project_path):
    state_machine_name = wrapper.get_single_object_property(state_machine,MBA.name)
    print("StateMachine",state_machine_name)
    state_machine_generator = StateMachineGenerator(state_machine_name)
    for state in wrapper.get_out_references(state_machine,MBA.has):
        print("state",state)
        state_name = wrapper.get_single_object_property(state,MBA.name)
        state_machine_generator.add_state(state_name)
    
    dst_file = os.path.join(project_path,f"{state_machine_name}.py")
    with open(dst_file, 'w') as f:
        f.write(state_machine_generator.gen())

model = parse_args();

graph = Graph()
graph.parse(model)

issues = {}

wrapper = SparQLWrapper(graph)



asset_templates = {
    "Dockerfile" : {
        "filename" : "Dockerfile",
        "template_path" : "template/python/Dockerfile"
    },
    "requirements.txt" : {
        "filename" : "requirements.txt",
        "template_path" : "template/python/requirements.txt"
    },
    "docker-compose.yml" : {
        "filename" : "docker-compose.yml",
        "template_path" : "template/docker/docker-compose.yml"
    },
    "handler.py" : {
        "filename" : "app.py",
        "template_path" : "template/python/handler.py"
    },
    "caller.py" : {
        "filename" : "app.py",
        "template_path" : "template/python/caller.py"
    },
    "encode.py" : {
        "filename" : "encode.py",
        "template_path" : "template/python/encode.py"
    },  
    "decode.py" : {
        "filename" : "decode.py",
        "template_path" : "template/python/decode.py"
    } 
}

for subsystem in wrapper.get_instances_of_type(MBA.Subsystem):
    name = wrapper.get_single_object_property(subsystem,MBA.name)
    path = create_project(name)
    create_asset("Dockerfile",path)
    create_asset("requirements.txt",path)

    # Lib / Helper
    create_asset("encode.py",path)
    create_asset("decode.py",path)


    for reference in wrapper.get_out_references(subsystem,MBA.has):
        type = wrapper.get_single_object_property(reference,RDF.type)
        if type == MBA.StateMachine:
            create_state_machine_asset(wrapper,reference,path)
        else:
            raise ValueError(f"Unknown type {type}")

    for provide_interface in wrapper.get_out_references(subsystem,MBA.provides):
        interface_name = wrapper.get_single_object_property(provide_interface,MBA.name)
        create_asset("handler.py",path)

        # generate messages in target language , import tech. Library
        for message in wrapper.get_out_references(provide_interface,MBA.has):
            create_message_asset(wrapper,message,path)
          
        
       
    for require_interface in wrapper.get_out_references(subsystem,MBA.requires):
        interface_name = wrapper.get_single_object_property(require_interface,MBA.name)
        create_asset("caller.py",path)
       
        # generate messages in target language , import tech. Library
        for message in wrapper.get_out_references(require_interface,MBA.has):
            create_message_asset(wrapper,message,path)





#global      
path = create_project("base")
create_asset("docker-compose.yml",path)
