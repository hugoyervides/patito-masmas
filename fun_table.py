# Function Table Class
# Victor Hugo Oyervides Covarrubias - A01382836
# Obed Gonzalez Morneo - A01382900
class Funtable:
    def __init__(self):
        self.table = []
    
    #Methods
    def newFunction(self, name, returnType, quadrupleAddress, number_param, number_variables, param):
        #Check if the function does not exists already
        for i in self.table:
            if i["name"] == name:
                return False
        newFun = {
            'name' : name,
            'returnType' : returnType,
            'quadrupleAddress': quadrupleAddress,
            'numberParam' : number_param,
            'numberVariables' : number_variables,
            'parameters' : param
        }
        self.table.append(newFun)
        return True
    
    #Method to check if a function exists
    def exists(self, name):
        #Check if the function exists
        for i in self.table:
            if i['name'] == name:
                return True
        return False


    #Method to display fun table
    def display_fun_table(self):
        print("FUNCTION TABLE")
        print("Name \t Type \t Addr \t #Par \t #Var \t Parameters")
        for i in self.table:
            print( str(i['name']) + '\t' + 
                    str(i['returnType']) + '\t' +
                    str(i['quadrupleAddress']) + '\t' +
                    str(i['numberParam']) + '\t' +
                    str(i['numberVariables']) + '\t', end='')
            for k in i['parameters']:
                print(str(k) + ' ,' , end = '')
            print()