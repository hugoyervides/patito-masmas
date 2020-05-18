# Variable table class
# Victor Hugo Oyervides Covarrubias - A01382836
# Obed Gonzalez Morneo - A01382900
class Vartable:
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
            'name' : name,
            'type' : varType,
            'vAddr' : vAddr,
            'dims' : dims
        })
        return True

    #method to get the number of variables
    def size(self):
        return len(self.table)

    #Method to display the var table
    def display_vars(self):
        print("Name \t Type \t Addres")
        for i in self.table:
            print(str(i["name"]) + '\t' +
                str(i["type"]) + '\t' +
                str(i["vAddr"]) + '\t')