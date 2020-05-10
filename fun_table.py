# Function Table Class
# Victor Hugo Oyervides Covarrubias - A01382836
# Obed Gonzalez Morneo - A01382900
class Funtable:
    def __init__(self):
        self.table = []
    
    #Methods
    def newFunction(self, name, returnType, quadrupleAddress):
        #Check if the function does not exists already
        for i in self.table:
            if i["name"] == name:
                return False
        newFun = {
            'name' : name,
            'returnType' : returnType,
            'quadrupleAddress': quadrupleAddress
        }
        self.table.append(newFun)
        return True
    
    #Method to display fun table
    def display_fun_table(self):
        print("FUNCTIOON TABLE")
        print("FunName \t FunType \t QuadAddr")
        for i in self.table:
            print( str(i['name']) + '\t' +
                    str(i['returnType']) + '\t' +
                    str(i['quadrupleAddress']) + '\t')