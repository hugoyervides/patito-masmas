# Variable table class
# Victor Hugo Oyervides Covarrubias - A01382836
# Obed Gonzalez Morneo - A01382900
class Vartable:
    def __init__(self):
        self.table = []

    #Method to add new variable
    def newVariable(self, name, varType):
        #Check if we dont already have a variable with that name
        for i in self.table:
            if i["name"] == name:
                return False
        #Insert the new function
        self.table.append({
            'name' : name,
            'type' : varType
        })