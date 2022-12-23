
def property_name(name : str) -> str:
    return ''.join([name[0].lower() + name[1:]])

def class_name(name : str) -> str:
    return ''.join([name[0].upper() + name[1:]])

def private_property_name(name : str) -> str:
    return f"_{property_name(name)}"


def set_type(datatype,varname):
    return {
        "uint8" : "np.uint8({})",
        "uint16" : "np.uint16({})",
        "string" : "str({})",
    }[datatype].format(varname)

class MessageGenerator:

    def __init__(self,name):
        self.name = name
        self.properties = []

    def add_property(self,name,datatype):
        self.properties.append([name,datatype])

    def gen(self) -> str:
        template = ""
        #imports
        template += "import numpy as np\n"
        template += "\n"

        
        template += f"class {class_name(self.name)}:\n"
        template += "\n"

        # init
        template += "\tdef __init__(self):\n"
        for [name,_] in self.properties:
            template += f"\t\tself.{private_property_name(name)} = None\n"
        template += "\n"

        # property and setter
        for [name,datatype] in self.properties:
            template += "\t@property\n"
            template += f"\tdef {property_name(name)}(self):\n"
            template += f"\t\treturn self.{private_property_name(name)}\n"
            template += "\n"
            template += f"\t@{property_name(name)}.setter\n"
            template += f"\tdef {property_name(name)}(self,value):\n"
            template += f"\t\tself.{private_property_name(name)} = {set_type(datatype,'value')}\n"
            template += "\n"


        return template;

    