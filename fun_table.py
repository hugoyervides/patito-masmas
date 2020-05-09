# Function Table Class
# Victor Hugo Oyervides Covarrubias - A01382836
# Obed Gonzalez Morneo - A01382900
from var_table import Vartable

class Funtable:
    def __init__(self):
        self.table = []
    
    #Methods
    def newFunction(self, name, returnType, varTable):
        #Check if the function does not exists already
        for i in self.table:
            if i["name"] == name:
                return False
        newFun = {
            'name' : name,
            'returnType' : returnType,
            'varTable' : varTable
        }
        self.table.append(newFun)
        return True