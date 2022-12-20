from rdflib import Graph, RDF, URIRef
from ontology.graphwrapper import GraphWrapper
from ontology.namespace import MBA


# Create Rdf-Model
graph = Graph()
wrapper = GraphWrapper(graph)

# Subsystems
rdf_interlocking = wrapper.add_named_instance(MBA.Subsystem,"Electronic Interlocking")
rdf_p = wrapper.add_named_instance(MBA.Subsystem,"Point")
rdf_ls = wrapper.add_named_instance(MBA.Subsystem,"Light Signal")
rdf_tds = wrapper.add_named_instance(MBA.Subsystem,"Train Detection System")
rdf_io = wrapper.add_named_instance(MBA.Subsystem,"Generic IO")
rdf_mdm = wrapper.add_named_instance(MBA.Subsystem,"Maintenance and Data Management")

# Interface
rdf_sci_ls = wrapper.add_named_instance(MBA.Interface,"SCI-LS")
wrapper.add_reference(MBA.has,rdf_interlocking,rdf_sci_ls)
wrapper.add_reference(MBA.has,rdf_ls,rdf_sci_ls)
#TODO add Message

rdf_sci_tds = wrapper.add_named_instance(MBA.Interface,"SCI-TDS")
wrapper.add_reference(MBA.has,rdf_interlocking,rdf_sci_tds)
wrapper.add_reference(MBA.has,rdf_tds,rdf_sci_tds)

rdf_sci_p_pdi = wrapper.add_named_instance(MBA.Message,"SCI-P.PDI")
wrapper.add_url_property(MBA.has,rdf_sci_p_pdi,"file://SCI-XX-PDI-Telegram-Structure.protobuf")

#rdf_sci_p_telegram = wrapper.add_sequence("SCI-XX-PDI-Telegram-Structure")
#rdf_sci_p_protocol_type = wrapper.add_named_instance(MBA.Property,"Specific Protocol Type")
#rdf_sci_p_message_type = wrapper.add_named_instance(MBA.Property,"Message Type")
#wrapper.add_reference(URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#_1'),rdf_sci_p_telegram,rdf_sci_p_protocol_type)
#wrapper.add_reference(URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#_2'),rdf_sci_p_telegram,rdf_sci_p_message_type)


rdf_sci_p = wrapper.add_named_instance(MBA.Interface,"SCI-P")
wrapper.add_reference(MBA.has,rdf_interlocking,rdf_sci_p)
wrapper.add_reference(MBA.has,rdf_p,rdf_sci_p)
wrapper.add_reference(MBA.has,rdf_sci_p,rdf_sci_p_pdi)






rdf_sci_io = wrapper.add_named_instance(MBA.Interface,"SCI-IO")
wrapper.add_reference(MBA.has,rdf_interlocking,rdf_sci_io)
wrapper.add_reference(MBA.has,rdf_io,rdf_sci_io)

rdf_sdi_ils = wrapper.add_named_instance(MBA.Interface,"SDI-ILS")
wrapper.add_reference(MBA.has,rdf_interlocking,rdf_sdi_ils)
wrapper.add_reference(MBA.has,rdf_mdm,rdf_sdi_ils)

rdf_smi_ils = wrapper.add_named_instance(MBA.Interface,"SMI-ILS")
wrapper.add_reference(MBA.has,rdf_interlocking,rdf_smi_ils)
wrapper.add_reference(MBA.has,rdf_mdm,rdf_smi_ils)




graph.serialize(destination=f"eulynx.ttl",format='turtle')