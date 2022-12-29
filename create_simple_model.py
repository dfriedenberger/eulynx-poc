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



#Telegam Parts
rdf_telegram_type = wrapper.add_named_instance(MBA.Property,"TelegramType")
wrapper.add_str_property(MBA.datatype,rdf_telegram_type,"uint8")
rdf_telegram_msg_len = wrapper.add_named_instance(MBA.Property,"MessageLength")
wrapper.add_str_property(MBA.datatype,rdf_telegram_msg_len,"uint16")
rdf_telegram_msg = wrapper.add_named_instance(MBA.Property,"Message")
wrapper.add_str_property(MBA.datatype,rdf_telegram_msg,"string")

rdf_pingpong_telegram = wrapper.add_sequence("PingPong-Telegram-Structure")
wrapper.add_reference(URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#_1'),rdf_pingpong_telegram,rdf_telegram_type)
wrapper.add_reference(URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#_2'),rdf_pingpong_telegram,rdf_telegram_msg_len)
wrapper.add_reference(URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#_3'),rdf_pingpong_telegram,rdf_telegram_msg)

#Message
rdf_msg_req = wrapper.add_named_instance(MBA.Message,"Ping")
wrapper.add_reference(MBA.structure,rdf_msg_req,rdf_pingpong_telegram)
wrapper.add_reference(MBA.has,rdf_i,rdf_msg_req)

rdf_msg_res = wrapper.add_named_instance(MBA.Message,"Pong")
wrapper.add_reference(MBA.structure,rdf_msg_res,rdf_pingpong_telegram)
wrapper.add_reference(MBA.has,rdf_i,rdf_msg_res)

# State Machines
## Server
rdf_state_init = wrapper.add_named_instance(MBA.State,"Init")
rdf_state_idle = wrapper.add_named_instance(MBA.State,"Idle")
rdf_state_accepted = wrapper.add_named_instance(MBA.State,"Accepted")
wrapper.add_str_property(MBA.init,rdf_state_init,"true")

rdf_state_machine = wrapper.add_named_instance(MBA.StateMachine,"Server")
wrapper.add_reference(MBA.has,rdf_state_machine,rdf_state_init)
wrapper.add_reference(MBA.has,rdf_state_machine,rdf_state_idle)
wrapper.add_reference(MBA.has,rdf_state_machine,rdf_state_accepted)

rdf_transition_initialize = wrapper.add_named_instance(MBA.Transition,"Initialize")
wrapper.add_reference(MBA.source,rdf_transition_initialize,rdf_state_init)
wrapper.add_reference(MBA.target,rdf_transition_initialize,rdf_state_idle)
wrapper.add_str_property(MBA.guard,rdf_transition_initialize,"true")

rdf_transition_accept = wrapper.add_named_instance(MBA.Transition,"Accept")
wrapper.add_reference(MBA.source,rdf_transition_accept,rdf_state_idle)
wrapper.add_reference(MBA.target,rdf_transition_accept,rdf_state_accepted)
wrapper.add_str_property(MBA.guard,rdf_transition_accept,"true")



rdf_transition_nop = wrapper.add_named_instance(MBA.Transition,"Timeout")
wrapper.add_reference(MBA.source,rdf_transition_nop,rdf_state_accepted)
wrapper.add_reference(MBA.target,rdf_transition_nop,rdf_state_idle)
wrapper.add_str_property(MBA.guard,rdf_transition_nop,"has timeout")

rdf_transition_handle_connection = wrapper.add_named_instance(MBA.Transition,"handle Connection")
wrapper.add_reference(MBA.source,rdf_transition_handle_connection,rdf_state_accepted)
wrapper.add_reference(MBA.target,rdf_transition_handle_connection,rdf_state_idle)
wrapper.add_str_property(MBA.guard,rdf_transition_handle_connection,"has connection")

wrapper.add_reference(MBA.has,rdf_server,rdf_state_machine)


graph.serialize(destination=f"simple.ttl",format='turtle')