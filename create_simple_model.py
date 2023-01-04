from rdflib import Graph, RDF, URIRef
from ontology.graphwrapper import GraphWrapper
from ontology.namespace import MBA
from ontology.sparql_queries import SparQLWrapper

import yaml


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


# Enrichment
with open("aspects.yaml", "r") as f:
    try:
        print(yaml.safe_load(f))
    except yaml.YAMLError as exc:
        print(exc)


sparQLWrapper = SparQLWrapper(graph)

## Add Projects, add dependencies, UML Package structure, Komponenten-Diagramm

## if 'architecture-pattern' == 'distibuted'
for subsystem in sparQLWrapper.get_instances_of_type(MBA.Subsystem):
    subsystem_name = sparQLWrapper.get_single_object_property(subsystem,MBA.name)

    ## package "" Project
    rdf_p = wrapper.add_named_instance(MBA.Package,subsystem_name);
    
    wrapper.add_reference(MBA.creates,rdf_p,subsystem)
    
    ## add assets

    ## Component for each state machine
    rdf_c_sm_lib = None
    for reference in sparQLWrapper.get_out_references(subsystem,MBA.has):
        type = sparQLWrapper.get_single_object_property(reference,RDF.type)
        name = sparQLWrapper.get_single_object_property(reference,MBA.name)
        if type == MBA.StateMachine:
            ## Component statemachine Library <<lib>>
            if not rdf_c_sm_lib:
                rdf_c_sm_lib = wrapper.add_named_instance(MBA.Component,"StateMachine",unique_name=subsystem_name+"StateMachine");
                wrapper.add_str_property(MBA.pattern,rdf_c_sm_lib,"lib")
                wrapper.add_str_property(MBA.project_ref,rdf_c_sm_lib,"templates/python/statemachine")
                wrapper.add_str_property(MBA.target_path,rdf_c_sm_lib,"statemachine")
                wrapper.add_reference(MBA.contains,rdf_p,rdf_c_sm_lib)

            #add component
            rdf_c = wrapper.add_named_instance(MBA.Component,name+"StateMachine",unique_name=subsystem_name+name);
            wrapper.add_str_property(MBA.pattern,rdf_c,"state machine")
            wrapper.add_str_property(MBA.target_path,rdf_c,"statemachine")

            wrapper.add_reference(MBA.contains,rdf_p,rdf_c)
            wrapper.add_reference(MBA.use,rdf_c,rdf_c_sm_lib)

            wrapper.add_reference(MBA.creates,rdf_c,reference)

        else:
            raise ValueError(f"Unknown type {type}")

        

    ## encode/decode Library
    ## messages + struct info
    message_structs = set()
    rdf_c_msg_lib = None

    for prop in [MBA.provides , MBA.requires]:
        for interface in sparQLWrapper.get_out_references(subsystem,prop):
            interface_name = sparQLWrapper.get_single_object_property(interface,MBA.name)
            ## encode/decode library (once)
            if not rdf_c_msg_lib:
                rdf_c_msg_lib = wrapper.add_named_instance(MBA.Component,"Message",unique_name=subsystem_name+"Message");
                wrapper.add_str_property(MBA.pattern,rdf_c_msg_lib,"lib")
                wrapper.add_str_property(MBA.project_ref,rdf_c_msg_lib,"templates/python/message")
                wrapper.add_str_property(MBA.target_path,rdf_c_msg_lib,"message")
                wrapper.add_reference(MBA.contains,rdf_p,rdf_c_msg_lib)


            # generate messages in target language , import tech. Library
            for message in sparQLWrapper.get_out_references(interface,MBA.has):
                #for message_struct in sparQLWrapper.get_out_references(message,MBA.structure):
                name = sparQLWrapper.get_single_object_property(message,MBA.name)

                ## Message Struct 
                #add component (only once)
                if message in message_structs: continue
                message_structs.add(message)

                rdf_c = wrapper.add_named_instance(MBA.Component,name,unique_name=subsystem_name+name);
                wrapper.add_str_property(MBA.pattern,rdf_c,"message")
                wrapper.add_str_property(MBA.target_path,rdf_c,"message")

                wrapper.add_reference(MBA.contains,rdf_p,rdf_c)
                wrapper.add_reference(MBA.use,rdf_c,rdf_c_msg_lib)

                wrapper.add_reference(MBA.creates,rdf_c,message)

       
   



    ## Component "Main"
    ## Haupt-Programm muss implementiert werden
    ## requirements.txt
   
    ## Dockerfile

## Add SUMO Modul

## Add Infrastruktur
### docker daemon oder aws cluster oder marvis


## Add Deployment
## Pipelines


graph.serialize(destination=f"simple-rich.ttl",format='turtle')

