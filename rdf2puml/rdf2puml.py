from rdflib import URIRef, Graph

from .pumlmodel import PumlModel
from ontology.sparql_queries import SparQLWrapper
from ontology.namespace import MBA


def rdf2puml(graph : Graph) -> PumlModel:

    puml = PumlModel("Architecture")
    wrapper = SparQLWrapper(graph)

    for instance in wrapper.get_instances():
        names = wrapper.get_object_properties(instance,MBA.name)
       
        type = wrapper.get_type(instance).split("#")[1]
        puml.create_node(instance,"/".join(names),type,["EULYNX"])

    for (n1,n2) in wrapper.get_references():
        puml.create_relation(n1,n2)

    puml.finish()
    return puml 
