from rdf2puml.rdf2puml import rdf2puml, statemachines2puml
from rdflib import Graph
import argparse
import os

def parse_args():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Script for transform model to code.')
    parser.add_argument("--model", required=True,
                        metavar="INPUT",
                        help="model")
    args = parser.parse_args()

    return args.model

model = parse_args();

graph = Graph()
graph.parse(model)

puml = rdf2puml(graph)
txt = '\n'.join(puml.puml)

basename = os.path.splitext(model)[0]
output_file = basename+".puml"
with open(output_file, 'w') as f:
    f.write(txt)

for key,puml_sm in statemachines2puml(graph).items():
    txt_sm = '\n'.join(puml_sm.puml)
    output_file_sm = basename+"-sm-"+key.lower()+".puml"
    with open(output_file_sm, 'w') as f:
        f.write(txt_sm)
