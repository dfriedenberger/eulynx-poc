from rdflib import Graph, RDF, URIRef
from ontology.graphwrapper import GraphWrapper
from ontology.namespace import MBA


# Create Rdf-Model
graph = Graph()
wrapper = GraphWrapper(graph)

# Subsystems
rdf_server = wrapper.add_named_instance(MBA.Subsystem,"Server")
rdf_client = wrapper.add_named_instance(MBA.Subsystem,"Client")


# Interface
rdf_i = wrapper.add_named_instance(MBA.Interface,"Echo")
wrapper.add_reference(MBA.provides,rdf_server,rdf_i)
wrapper.add_reference(MBA.requires,rdf_client,rdf_i)


#Message
rdf_msg_req = wrapper.add_named_instance(MBA.Message,"Ping")
wrapper.add_url_property(MBA.has,rdf_msg_req,"file://PingRequest-Structure.protobuf")
wrapper.add_reference(MBA.has,rdf_i,rdf_msg_req)

rdf_msg_res = wrapper.add_named_instance(MBA.Message,"Pong")
wrapper.add_url_property(MBA.has,rdf_msg_res,"file://PongResponse-Structure.protobuf")
wrapper.add_reference(MBA.has,rdf_i,rdf_msg_res)


graph.serialize(destination=f"simple.ttl",format='turtle')