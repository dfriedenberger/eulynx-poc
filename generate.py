from rdflib import Graph
from ontology.sparql_queries import SparQLWrapper
from ontology.namespace import MBA
import argparse
import hashlib
import os
import json
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
    "pingrequest.py" : {
        "filename" : "pingrequest.py",
        "template_path" : "template/python/pingrequest.py"
    },  
    "pongresponse.py" : {
        "filename" : "pongresponse.py",
        "template_path" : "template/python/pongresponse.py"
    } 
}

for subsystem in wrapper.get_instances_of_type(MBA.Subsystem):
    name = wrapper.get_single_object_property(subsystem,MBA.name)
    path = create_project(name)
    create_asset("Dockerfile",path)
    create_asset("requirements.txt",path)
    create_asset("pingrequest.py",path)
    create_asset("pongresponse.py",path)

    for provide_interface in wrapper.get_out_references(subsystem,MBA.provides):
        interface_name = wrapper.get_single_object_property(provide_interface,MBA.name)
        create_asset("handler.py",path)
        
        # generate messages in target language , import tech. Library
        for message in wrapper.get_out_references(provide_interface,MBA.has):
            message_name = wrapper.get_single_object_property(message,MBA.name)
            print("Message",message_name)
        
    for require_interface in wrapper.get_out_references(subsystem,MBA.requires):
        interface_name = wrapper.get_single_object_property(require_interface,MBA.name)
        create_asset("caller.py",path)
        
        # generate messages in target language , import tech. Library
        for message in wrapper.get_out_references(require_interface,MBA.has):
            message_name = wrapper.get_single_object_property(message,MBA.name)
            print("Message",message_name)


#global      
path = create_project("base")
create_asset("docker-compose.yml",path)
 

 


# Implementation
class Implementation:
    def __init__(self,issues,asset_templates):
        self.issues = issues
        self.implemented = set()
        self.asset_templates = asset_templates

    def _implement_issue(self,issueId):

        if issueId in self.implemented:
            return

        # Depends
        issue = issues[issueId]
        if 'depends' in issue:
            for dependId in issue['depends']:
                self._implement_issue(dependId)

      

        for asset in issue['assets']:
            # Implement
            if asset not in self.asset_templates:
                raise Exception(f"Generator for {asset} not implemented")
            
          


        self.implemented.add(issueId)

    def implement(self):
        for issueId in self.issues.keys():
            self._implement_issue(issueId)


Implementation(issues,asset_templates).implement()
  
       
