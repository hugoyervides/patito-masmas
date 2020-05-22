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
        #Check if we dont already have a variable with that name
        for i in self.table:
            if i["name"] == name:
                return False
        #Insert the new function
        self.table.append({
            'name' :    name, #Name of the variable
            'type' :    varType, #Type of the variable
            'vAddr' :   vAddr, #TODO Virtual Address for the variable
            'dims' :    dims #TODO List of dimensions
        })
        return True

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
        for var in self.table:
            if(var['name'] == name):
                return var['type']
            
        return None


    def get_mem(self, name):
        for var in self.table:
            if(var['name'] == name):
                return var['vAddr']
            
        return None