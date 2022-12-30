from rdflib import Graph, RDF, URIRef
from ontology.graphwrapper import GraphWrapper
from ontology.namespace import MBA



def create_server_state_machine():
    rdf_state_machine = wrapper.add_named_instance(MBA.StateMachine,"Server")

    rdf_state_init = wrapper.add_named_instance(MBA.State,"Init",unique_name="ServerInit")
    rdf_state_idle = wrapper.add_named_instance(MBA.State,"Idle",unique_name="ServerIdle")
    rdf_state_accepted = wrapper.add_named_instance(MBA.State,"Accepted",unique_name="ServerAccepted")
    wrapper.add_str_property(MBA.init,rdf_state_init,"true")

    wrapper.add_reference(MBA.has,rdf_state_machine,rdf_state_init)
    wrapper.add_reference(MBA.has,rdf_state_machine,rdf_state_idle)
    wrapper.add_reference(MBA.has,rdf_state_machine,rdf_state_accepted)

    rdf_transition_initialize = wrapper.add_named_instance(MBA.Transition,"Initialize",unique_name="ServerInitialize")
    wrapper.add_reference(MBA.source,rdf_transition_initialize,rdf_state_init)
    wrapper.add_reference(MBA.target,rdf_transition_initialize,rdf_state_idle)
    wrapper.add_str_property(MBA.guard,rdf_transition_initialize,"true")

    rdf_transition_accept = wrapper.add_named_instance(MBA.Transition,"Accept",unique_name="ServerAccept")
    wrapper.add_reference(MBA.source,rdf_transition_accept,rdf_state_idle)
    wrapper.add_reference(MBA.target,rdf_transition_accept,rdf_state_accepted)
    wrapper.add_str_property(MBA.guard,rdf_transition_accept,"true")


    rdf_transition_nop = wrapper.add_named_instance(MBA.Transition,"Timeout",unique_name="ServerTimeout")
    wrapper.add_reference(MBA.source,rdf_transition_nop,rdf_state_accepted)
    wrapper.add_reference(MBA.target,rdf_transition_nop,rdf_state_idle)
    wrapper.add_str_property(MBA.guard,rdf_transition_nop,"timeout")

    rdf_transition_handle_connection = wrapper.add_named_instance(MBA.Transition,"handle Connection",unique_name="ServerHandleConnection")
    wrapper.add_reference(MBA.source,rdf_transition_handle_connection,rdf_state_accepted)
    wrapper.add_reference(MBA.target,rdf_transition_handle_connection,rdf_state_idle)
    wrapper.add_str_property(MBA.guard,rdf_transition_handle_connection,"new connection")

    return rdf_state_machine


def create_connection_state_machine():
    rdf_state_machine = wrapper.add_named_instance(MBA.StateMachine,"Connection")

    rdf_state_init = wrapper.add_named_instance(MBA.State,"Init",unique_name="ConnectionInit")
    rdf_state_idle = wrapper.add_named_instance(MBA.State,"Idle",unique_name="ConnectionIdle")
    rdf_state_handle_recv_data = wrapper.add_named_instance(MBA.State,"HandleRecvData",unique_name="ConnectionHandleRecvData")
    rdf_state_closed = wrapper.add_named_instance(MBA.State,"Closed",unique_name="ConnectionClosed")
    wrapper.add_str_property(MBA.init,rdf_state_init,"true")
    wrapper.add_str_property(MBA.final,rdf_state_closed,"true")

    wrapper.add_reference(MBA.has,rdf_state_machine,rdf_state_init)
    wrapper.add_reference(MBA.has,rdf_state_machine,rdf_state_idle)
    wrapper.add_reference(MBA.has,rdf_state_machine,rdf_state_handle_recv_data)
    wrapper.add_reference(MBA.has,rdf_state_machine,rdf_state_closed)

    rdf_transition_initialize = wrapper.add_named_instance(MBA.Transition,"Initialize",unique_name="ConnectionInitialize")
    wrapper.add_reference(MBA.source,rdf_transition_initialize,rdf_state_init)
    wrapper.add_reference(MBA.target,rdf_transition_initialize,rdf_state_idle)
    wrapper.add_str_property(MBA.guard,rdf_transition_initialize,"true")

    rdf_transition_close = wrapper.add_named_instance(MBA.Transition,"Close",unique_name="ConnectionClose")
    wrapper.add_reference(MBA.source,rdf_transition_close,rdf_state_idle)
    wrapper.add_reference(MBA.target,rdf_transition_close,rdf_state_closed)
    wrapper.add_str_property(MBA.guard,rdf_transition_close,"error")

    rdf_transition_send = wrapper.add_named_instance(MBA.Transition,"Send",unique_name="ConnectionSend")
    wrapper.add_reference(MBA.source,rdf_transition_send,rdf_state_idle)
    wrapper.add_reference(MBA.target,rdf_transition_send,rdf_state_idle)
    wrapper.add_str_property(MBA.guard,rdf_transition_send,"send_data")

    rdf_transition_recv = wrapper.add_named_instance(MBA.Transition,"Recv",unique_name="ConnectionRecv")
    wrapper.add_reference(MBA.source,rdf_transition_recv,rdf_state_idle)
    wrapper.add_reference(MBA.target,rdf_transition_recv,rdf_state_handle_recv_data)
    wrapper.add_str_property(MBA.guard,rdf_transition_recv,"no_error")
    wrapper.add_str_property(MBA.guard,rdf_transition_recv,"no_send_data")


    rdf_transition_handle_callback = wrapper.add_named_instance(MBA.Transition,"Handle Callback",unique_name="ConnectionHandleCallback")
    wrapper.add_reference(MBA.source,rdf_transition_handle_callback,rdf_state_handle_recv_data)
    wrapper.add_reference(MBA.target,rdf_transition_handle_callback,rdf_state_idle)
    wrapper.add_str_property(MBA.guard,rdf_transition_handle_callback,"recv_data")

    rdf_transition_timeout = wrapper.add_named_instance(MBA.Transition,"Timeout",unique_name="ConnectionTimeout")
    wrapper.add_reference(MBA.source,rdf_transition_timeout,rdf_state_handle_recv_data)
    wrapper.add_reference(MBA.target,rdf_transition_timeout,rdf_state_idle)
    wrapper.add_str_property(MBA.guard,rdf_transition_timeout,"timeout")


    return rdf_state_machine

def create_client_state_machine():
    rdf_state_machine = wrapper.add_named_instance(MBA.StateMachine,"Client")

    rdf_state_init = wrapper.add_named_instance(MBA.State,"Init",unique_name="ClientInit")
    rdf_state_idle = wrapper.add_named_instance(MBA.State,"Idle",unique_name="ClientIdle")
    rdf_state_connected = wrapper.add_named_instance(MBA.State,"Connected",unique_name="ClientConnected")
    rdf_state_handle_recv_data = wrapper.add_named_instance(MBA.State,"HandleRecvData",unique_name="ClientHandleRecvData")
    rdf_state_closed = wrapper.add_named_instance(MBA.State,"Closed",unique_name="ClientClosed")
    wrapper.add_str_property(MBA.init,rdf_state_init,"true")

    wrapper.add_reference(MBA.has,rdf_state_machine,rdf_state_init)
    wrapper.add_reference(MBA.has,rdf_state_machine,rdf_state_idle)
    wrapper.add_reference(MBA.has,rdf_state_machine,rdf_state_connected)
    wrapper.add_reference(MBA.has,rdf_state_machine,rdf_state_handle_recv_data)
    wrapper.add_reference(MBA.has,rdf_state_machine,rdf_state_closed)

    rdf_transition_initialize = wrapper.add_named_instance(MBA.Transition,"Initialize",unique_name="ClientInitialize")
    wrapper.add_reference(MBA.source,rdf_transition_initialize,rdf_state_init)
    wrapper.add_reference(MBA.target,rdf_transition_initialize,rdf_state_idle)
    wrapper.add_str_property(MBA.guard,rdf_transition_initialize,"true")

    rdf_transition_connect = wrapper.add_named_instance(MBA.Transition,"Connect",unique_name="ClientConnect")
    wrapper.add_reference(MBA.source,rdf_transition_connect,rdf_state_idle)
    wrapper.add_reference(MBA.target,rdf_transition_connect,rdf_state_connected)
    wrapper.add_str_property(MBA.guard,rdf_transition_connect,"true")


    rdf_transition_close = wrapper.add_named_instance(MBA.Transition,"Close",unique_name="ClientClose")
    wrapper.add_reference(MBA.source,rdf_transition_close,rdf_state_connected)
    wrapper.add_reference(MBA.target,rdf_transition_close,rdf_state_closed)
    wrapper.add_str_property(MBA.guard,rdf_transition_close,"error")

    rdf_transition_send = wrapper.add_named_instance(MBA.Transition,"Send",unique_name="ClientSend")
    wrapper.add_reference(MBA.source,rdf_transition_send,rdf_state_connected)
    wrapper.add_reference(MBA.target,rdf_transition_send,rdf_state_connected)
    wrapper.add_str_property(MBA.guard,rdf_transition_send,"send_data")

    rdf_transition_recv = wrapper.add_named_instance(MBA.Transition,"Recv",unique_name="ClientRecv")
    wrapper.add_reference(MBA.source,rdf_transition_recv,rdf_state_connected)
    wrapper.add_reference(MBA.target,rdf_transition_recv,rdf_state_handle_recv_data)
    wrapper.add_str_property(MBA.guard,rdf_transition_recv,"no_error")
    wrapper.add_str_property(MBA.guard,rdf_transition_recv,"no_send_data")


    rdf_transition_handle_callback = wrapper.add_named_instance(MBA.Transition,"Handle Callback",unique_name="ClientHandleCallback")
    wrapper.add_reference(MBA.source,rdf_transition_handle_callback,rdf_state_handle_recv_data)
    wrapper.add_reference(MBA.target,rdf_transition_handle_callback,rdf_state_connected)
    wrapper.add_str_property(MBA.guard,rdf_transition_handle_callback,"recv_data")

    rdf_transition_timeout = wrapper.add_named_instance(MBA.Transition,"Timeout",unique_name="ClientTimeout")
    wrapper.add_reference(MBA.source,rdf_transition_timeout,rdf_state_handle_recv_data)
    wrapper.add_reference(MBA.target,rdf_transition_timeout,rdf_state_connected)
    wrapper.add_str_property(MBA.guard,rdf_transition_timeout,"timeout")

    rdf_transition_wait = wrapper.add_named_instance(MBA.Transition,"Wait",unique_name="ClientWait")
    wrapper.add_reference(MBA.source,rdf_transition_wait,rdf_state_closed)
    wrapper.add_reference(MBA.target,rdf_transition_wait,rdf_state_init)
    wrapper.add_str_property(MBA.guard,rdf_transition_wait,"true")

    return rdf_state_machine

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
rdf_server_state_machine = create_server_state_machine()
rdf_connection_state_machine = create_connection_state_machine()
rdf_client_state_machine = create_client_state_machine()

wrapper.add_reference(MBA.has,rdf_server,rdf_server_state_machine)
wrapper.add_reference(MBA.has,rdf_server,rdf_connection_state_machine)
wrapper.add_reference(MBA.has,rdf_client,rdf_client_state_machine)


graph.serialize(destination=f"simple.ttl",format='turtle')