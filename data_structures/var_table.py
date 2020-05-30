# Variable table class
# Victor Hugo Oyervides Covarrubias - A01382836
# Obed Gonzalez Morneo - A01382900

#Vartable data structure used to store the variables

class Vartable:
    #Declaration of atributes
    def __init__(self):
        self.table = []

    #Method to add new variable
    def newVariable(self, name, varType, vAddr, dims):
        e = None
        #Check if we dont already have a variable with that name
        for i in self.table:
            if i["name"] == name:
                e = "Variable " + str(name) + " already exists" 
        #Insert the new function
        self.table.append({
            'name' :    name, #Name of the variable
            'type' :    varType, #Type of the variable
            'vAddr' :   vAddr, #Virtual Address for the variable
            'dims' :    dims #TODO List of dimensions
        })
        return e

    #method to get the number of variables
    def size(self):
        return len(self.table)

    #Method to display the var table (used for DEBUGING)
    def display_vars(self):
        print("Name \t Type \t Addres")
        for i in self.table:
            print(str(i["name"]) + '\t' +
                str(i["type"]) + '\t' +
                str(i["vAddr"]) + '\t')

    def get_type(self, name):
        e = None
        for var in self.table:
            if(var['name'] == name):
                return var['type'], e
        e = "Variable " + str(name) + " not declared"
        return None, e

    def get_vaddr(self, name):
        e = None
        for var in self.table:
            if(var['name'] == name):
                return var['vAddr'], e
        e = "Variable " + str(name) + " not declared"
        return None, e

    def get_dims(self, name):
        e = None
        for var in self.table:
            if(var['name'] == name):
                return var['dims'], e
        e = "Variable " + str(name) + " not declared"
        return None, e

    def get_variable(self, vaddr):
        e = None
        for var in self.table:
            if(var['vAddr'] == vaddr):
                return var, e
        e = "Variable " + str(vaddr) + ' not declared'
        return None, e