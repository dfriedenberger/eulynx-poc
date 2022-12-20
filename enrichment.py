from rdflib import Graph
import yaml

with open("aspects.yaml", "r") as f:
    try:
        print(yaml.safe_load(f))
    except yaml.YAMLError as exc:
        print(exc)

graph = Graph()
graph.parse("eulynx.ttl")

# enrichment

graph.serialize(destination=f"eulynx-rich.ttl",format='turtle')