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

    #Method to flush current var table when we change the function
    def flush_var_table(self, var_type):
        if var_type == 'local':
            self.local_var_table = Vartable()

        elif var_type == 'global':
            self.global_var_table = Vartable()

    #Method to set the variable type that we are currenntly feeding into the vartable
    def set_var_type(self, var_type):
        self.current_type = var_type

    def get_var_type(self, value):
        if(self.context != "global"):
            return self.local_var_table.get_type(value)

    
    #Method to insert a new variable to the var table
    def insert_variable(self, variable):
        #Check if we are in global or local context
        if self.context == "global":
            return self.global_var_table.newVariable(variable, self.current_type, None, None)

        elif self.context == "local":
            return self.local_var_table.newVariable(variable, self.current_type, None, None)

    #Used for DEBUGING ONLY!
    def display_var_table(self, var_type):
        if var_type == "local":
            self.local_var_table.display_vars()

        elif var_type == "global":
            print("Displaying global Var table")
            self.global_var_table.display_vars()
            
    #Method to change the context of the var table
    def change_context(self, new_context):
        self.context = new_context # global or local
    