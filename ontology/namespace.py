from rdflib.term import URIRef
from rdflib.namespace import DefinedNamespace, Namespace

class MBA(DefinedNamespace):

    """
    Microservice Batch Architecture Definition Language (XSD) 
    Datatypes
    """
    URL = "https://frittenburger.de/2022/11/EULYNX"
    _NS = Namespace(URL+"/Schema#")

    # http://www.w3.org/2000/01/rdf-schema#Class

    #IPO model
    Subsystem: URIRef
    Interface: URIRef
    Message: URIRef
    Property: URIRef

    #StateMachine
    StateMachine: URIRef
    State: URIRef
    Transition: URIRef

    # C3 Level
    Package: URIRef
    Component: URIRef

    # http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
    name: URIRef #All Objects have names
    datatype: URIRef


    # general relations
    has: URIRef
    structure: URIRef



    ## interface relations
    provides: URIRef
    requires: URIRef
   
    ## statemachine properties
    guard: URIRef
    init: URIRef
    final: URIRef

    ## statemachine relations
    source: URIRef
    target: URIRef

    # C3 Level relations
    contains: URIRef
    creates: URIRef
    use: URIRef

    # C3 Level properties
    pattern: URIRef

    # C3 Level / Library properties
    target_path: URIRef
    project_ref: URIRef


