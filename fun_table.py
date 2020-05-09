# Function Table Class
# Victor Hugo Oyervides Covarrubias - A01382836
# Obed Gonzalez Morneo - A01382900
import var_table

class Funtable:
    def __init__(self):
        self.table = []
    
    #Methods
    def newFunction(self, name, returnType, varTable):
        newFun = {
            'name' : name,
            'returnType' : returnType,
            'varTable' : varTable
        }
        self.table.append(newFun)