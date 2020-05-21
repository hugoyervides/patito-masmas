# Var tables class
# Victor Hugo Oyervides Covarrubias - A01382836
# Obed Gonzalez Morneo - A01382900

#This class is used to manage all the var tables used during the semantics
#We store here the local variables and the global variables


from var_table import Vartable #Include the Vartable datascructure

#Declaration of function
class Vartables:

    #Declaration of the variables that we are going to be using
    def __init__(self):
        self.local_var_table = Vartable() #Used to store the local var table used in functions
        self.global_var_table = Vartable() #Used to store the global var table used in main
        self.context = "global" #Used to define the context (in the main (global) or in the local function)
        self.current_type = "" #Used to define the current type of variables that we are pushing into the tables
        self.global_mem = 1000
        self.local_mem = 8001

    #Method to change the context of the var table
    def change_context(self, new_context):
        self.context = new_context # global or local

    #Method to flush current var table when we change the function
    def flush_var_table(self, var_type):
        if var_type == 'local':
            self.local_var_table = Vartable()

        elif var_type == 'global':
            self.global_var_table = Vartable()

    #Method to set the variable type that we are currenntly feeding into the vartable
    def set_var_type(self, var_type):
        self.current_type = var_type

    #Method to get the current type of variable
    def get_var_type(self, value):
        #Check the context that we are currenlty
        if(self.context == "local"):
            var_type, e = self.local_var_table.get_type(value)
            if var_type == None:
                return self.global_var_table.get_type(value)
            return var_type, e
        return self.global_var_table.get_type(value)

    #Method to get the current type of variable
    def get_var_vaddr(self, value):
        #Check the context that we are currenlty
        if(self.context == "local"):
            var_type, e = self.local_var_table.get_vaddr(value)
            if var_type == None:
                return self.global_var_table.get_vaddr(value)
            return var_type, e
        return self.global_var_table.get_vaddr(value)

    #Method to insert a new variable to the var table
    def insert_variable(self, variable):
        e = None
        #Check if we are in global or local context
        if self.context == "global":
            if(self.global_mem <= 8000):
                self.global_mem += 1
                e = self.global_var_table.newVariable(variable, self.current_type, self.global_mem - 1, None)
            #TODO: error handling for memory
        elif self.context == "local":
            if(self.local_mem <= 15000):
                self.local_mem += 1
                e = self.local_var_table.newVariable(variable, self.current_type, self.local_mem - 1, None)
            #TODO: error handling for memory
        return e

    def insert_function(self, function_name, function_type):
        self.global_mem += 1
        self.global_var_table.newVariable(function_name, function_type, self.global_mem - 1, None)

    #Used for DEBUGING ONLY!
    def display_var_table(self, var_type):
        if var_type == "local":
            self.local_var_table.display_vars()

        elif var_type == "global":
            print("Displaying global Var table")
            self.global_var_table.display_vars()
        
    
#variables globales - 1000 -> 8000
#int - 1000 -> 5000
#float - 5001 -> 6000
#char - 6001 -> 7000
#string - 7001 -> 8000

#variables locales - 8001 -> 15000
#int - 8001 -> 12000
#float - 12001 -> 13000
#char - 13001 -> 14000
#string - 14001 -> 15000