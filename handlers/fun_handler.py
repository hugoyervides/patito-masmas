# Function table Handler
# Victor Hugo Oyervides Covarrubias - A01382836
# Obed Gonzalez Morneo - A01382900

#Class used to handle the function table and its operations

from data_structures import Funtable #Import the funtable datasctructure

class Funhandler:
    #Atribute declaration
    def __init__(self):
        self.funcTable = Funtable()
        self.current_function = {}
        self.called_function = []
        self.param_counter = 0

    #Method to check a function name inside the function table
    def check_function(self, name):
        e = None
        if not self.funcTable.exists(name):
            e = "Function " + str(name) + ' does not exist!'
        return e  

    #Method to change current scoped function
    def updateFunction(self, key, value):
        self.current_function[key] = value
    
    #Method to update the function quadruple address
    def update_fun_address(self, address):
        self.current_function["quadrupleAddress"] = address

    #Method to insert type to function table
    def insert_type(self, current_type):
        self.current_function['parameters'].append(current_type)
    
    def insert_number_param(self):
        self.current_function["numberParam"] = len(self.current_function['parameters'])

    def insert_number_variables(self, number_variables):
        self.current_function['numberVariables'] =  number_variables - len(self.current_function['parameters'])

    #Method to flush current function
    def flushFunctionTable(self):
        self.current_function = {}

    #Method to insert the current function into the table
    def insertToFunTable(self):
        return self.funcTable.newFunction(
                    self.current_function["name"],
                    self.current_function["varType"],
                    self.current_function["quadrupleAddress"],
                    self.current_function["numberParam"],
                    self.current_function["numberVariables"],
                    self.current_function["parameters"])
        
    def load_called_function(self, name):
        e = None
        self.param_counter = 0
        function, e = self.funcTable.get_function(name)
        if e:
            return None, e
        self.called_function.append(function)
        return self.called_function[-1], e

    def check_param_counter(self):
        e = None
        if len(self.called_function[-1]['parameters']) != self.param_counter:
            e = "Parameter missmatch for function " + str(self.called_function[-1]['name'])
        return e

    def check_param_type(self, param_type):
        e = None
        #Check the parameters
        if len(self.called_function[-1]['parameters']) <= self.param_counter:
            e = "Parameter missmatch for function " + str(self.called_function[-1]['name'])
        elif param_type == self.called_function[-1]['parameters'][self.param_counter]:
            self.param_counter += 1
        else:
            e = "Parameter " + str(self.param_counter) + ' missmatch for function ' + str(self.called_function[-1]["name"])
        return e
        