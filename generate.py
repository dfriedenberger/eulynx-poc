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

# helper
def gen_id(o):
    return hashlib.md5(str(o).encode('utf-8')).hexdigest()

def to_path(o):
    return o.lower().replace(' ','-')


model = parse_args();

graph = Graph()
graph.parse(model)

issues = {}

wrapper = SparQLWrapper(graph)

for subsystem in wrapper.get_instances_of_type(MBA.Subsystem):
    # use implemented Docker-File / DockerCompose-file
    # generate Konfiguration
    depends = []
    for interface in wrapper.get_out_references(subsystem,MBA.has):
        name = wrapper.get_single_object_property(interface,MBA.name)
        # use implemented java/python libraries 
        # generate message classes 
        issue = {
            "id" : gen_id(interface),
            "type" : "Story",
            "title" : f"Create Library and Configuration for Interface {interface}",
            "project" : name,
            "assets" : [],

        }
        depends.append(issue['id'])
        issues[issue['id']] = issue

    # Issue for SubSystem
    name = wrapper.get_single_object_property(subsystem,MBA.name)
    issue = {
        "id" : gen_id(subsystem),
        "type" : "Story",
        "title" : f"Create Project for Subsystem {subsystem}",
        "project" : name,      
        "assets" : ["Dockerfile"],
        "depends" : depends
    }
    issues[issue['id']] = issue

# generate ReadMe for the whole Projekt

output_file = os.path.splitext(model)[0]+".issueJson"
with open(output_file, 'w') as f:
    json.dump(issues,f, indent=4)



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

        #TODO create project 
        print("Implement Project",issue['project'])
        project_path = f"tmp/{to_path(issue['project'])}"
        if not os.path.exists(project_path):
            os.mkdir(project_path)

        for asset in issue['assets']:
            # Implement
            if asset not in self.asset_templates:
                raise Exception(f"Generator for {asset} not implemented")
            
            #TODO create asset 
            print("Create Asset",asset)
            asset_template = self.asset_templates[asset]
            src_file = asset_template['template_path']
            dst_file = os.path.join(project_path,asset_template['filename'])
            shutil.copyfile(src_file,dst_file)


        self.implemented.add(issueId)

    def implement(self):
        for issueId in self.issues.keys():
            self._implement_issue(issueId)

asset_templates = {
    "Dockerfile" : {
        "filename" : "Dockerfile",
        "template_path" : "template/python/Dockerfile"
    }
}
Implementation(issues,asset_templates).implement()
  
       
