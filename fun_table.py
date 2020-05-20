# Function Table Class
# Victor Hugo Oyervides Covarrubias - A01382836
# Obed Gonzalez Morneo - A01382900

#Function table data structure used to store the functions

class Funtable:
    #Declaration of atributes
    def __init__(self):
        self.table = [] #Table to store the functions
    
    #Methods
    def newFunction(self, name, returnType, quadrupleAddress, number_param, number_variables, param):
        e = None
        #Check if the function does not exists already
        for i in self.table:
            if i["name"] == name:
                e = "Function " + str(name) + " already declared"
        newFun = {
            'name' : name, #Name of the function
            'returnType' : returnType, #The type of return (void, int, char, etc.)
            'quadrupleAddress': quadrupleAddress, #The quadruple address where the function starts
            'numberParam' : number_param, #The number of parameters that the function recives
            'numberVariables' : number_variables, #The number of local variables that the function declarates
            'parameters' : param #List of parameters types that the function have in order (ex: int, char, int)
        }
        self.table.append(newFun)
        return e
    
    #Method to check if a function exists
    def exists(self, name):
        #Check if the function exists
        for i in self.table:
            if i['name'] == name:
                return True
        return False


    #Method to display fun table (Used for DEBUGING)
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
            
    #Verify parameters
    def verify_parameters(self, name, parameters):
        #For to check the parameters
        e = None
        function = None
        for i in self.table:
            if i['name'] == name:
                function = i
                break
        if not function == parameters:
            e = "Parameter mismatch"
        return e
            
    def get_function(self, name):
        #for to search for the function
        e = None
        for i in self.table:
            if i['name'] == name:
                return i, e
        e = "Function not found"
        return None, e