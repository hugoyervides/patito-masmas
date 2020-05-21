# Stacks class
# Victor Hugo Oyervides Covarrubias - A01382836
# Obed Gonzalez Morneo - A01382900

#This class is used to handle all the stack operations used during the semantics
#Operator Stack, Operand Stack, Type Stack, jump_stack, Migajitas and quadruples

from quadruples import Quadruples
from semantic import cubo_semantico
import parser

class Stacks:
    def __init__(self):
        self.operator_stack = [] #Used to store the operators
        self.operand_stack = []  #Used to store the operands
        self.type_stack = [] #Used to store the type of the operands (Size must match with the operand_stack)
        self.jump_stack = { #Used to save pending jumps if we have a GOTO or GOTOF
            'GOTOF' :   [],
            'GOTO' :    []
        } 
        self.migajitas = { #Used to save where the start address of a loop is 
            'GOTOF' :   [],
            'GOTO' :    []
        }
        self.return_stack = [] #Used for pending return Jumps
        self.quadruples = Quadruples() 
        self.result_counter = 0

    #Method to get an operand with its type
    def pop_operand(self):
        operand = self.operand_stack.pop()
        operand_type = self.type_stack.pop()
        return operand, operand_type

    #Method to register a new oeprator into our stackl
    def register_operator(self, operator):
        self.operator_stack.append(operator)

    #Method to register a new operand into our stack
    def register_operand(self, variable):
        self.operand_stack.append(variable)

    #Method to register a new type into our stack
    def register_type(self, variable):
        self.type_stack.append(variable)

    #Method to register a new $ into the operator stack
    #Used to separate the operators of a expresion inside a () )
    def register_separator(self):
        self.operator_stack.append('$')

    #Method to eliminate the $ if it exists in top of the operator stack
    #When we are done evaluating our expresion inside the () )
    def pop_separator(self):
        e = None
        if self.operator_stack[-1] == '$':
            self.operator_stack.pop()
        else:
            e = "Invalid expresion"
        return e

    #Method to get the top of the operators (Used to for neuralgic points)
    def top_operators(self):
        if len(self.operator_stack) > 0 and self.operand_stack[-1] != '$':
            return self.operator_stack[-1]
        else:
            return None

    #Method to get the top operand (Currently not used but may be helpful in the future >:D )
    def top_operand(self):
        if len(self.operand_stack) > 0:
            return self.operand_stack[-1]
        else:
            return None

    def top_types(self):
        if len(self.type_stack) > 0:
            return self.type_stack[-1]
        else:
            return None

    #Method to get a new temporal value name
    def get_result_var(self):
        result = 't' + str(self.result_counter)
        self.result_counter += 1
        return result

    #The name of this method is really obvious but will it generates a new quadruple when we reach certain neuralgic point
    def generate_quadruple(self):
        e = None
        #Get the right operand and type
        r_operand = self.operand_stack.pop()
        r_type = self.type_stack.pop()
        #Get the left operand and type
        l_operand = self.operand_stack.pop()
        l_type = self.type_stack.pop()
        #Get the operator
        operator = self.operator_stack.pop()
        result = self.get_result_var()
        #Verify with semantics
        type_quad = cubo_semantico[r_type][l_type][operator]
        if(type_quad != 'Error'):
            self.operand_stack.append(result)
            self.type_stack.append(type_quad)
            self.quadruples.add_quadruple(operator,l_operand,r_operand,result)
        else:
            e = "Operation " + str(l_type) + ' ' + str(operator) + ' ' + str(r_type) + " not posible!"
        return e
            

    #This does the same as the previus method but formats the quadruple for asignation ( = NEW_VALUE NULL RESULT)
    def generate_asignation(self):
        e = None
        #Get the right operand and type
        r_operand = self.operand_stack.pop()
        r_type = self.type_stack.pop()
        #get where are we going to save the result and type
        result = self.operand_stack.pop()
        result_type = self.type_stack.pop()
        operator = self.operator_stack.pop()
        #Verify semantics
        type_quad = cubo_semantico[result_type][r_type][operator]
        if(type_quad != 'Error'):
            self.operand_stack.append(result)
            self.type_stack.append(result_type)
            self.quadruples.add_quadruple(operator,r_operand, None, result)
        else:
            e = "Canot asign " + str(r_type) + ' to ' + str(result_type) + '!'
        return e
    
    def generate_param_quadruple(self, param_number):
        #Get the right operand and type
        operand = self.operand_stack.pop()
        #Pop the type (we wont need it)
        self.type_stack.pop()
        #Generate the cuadruple
        self.quadruples.add_quadruple("PARAM", operand, None, "PARAM" + str(param_number))

    def generate_gosub_quadruple(self, function, vaddr):
        self.quadruples.add_quadruple("GOSUB", None, None, function['name'])
        #Check if the function has a return value
        if function['returnType'] != 'void':
            #Add a tep value to store the function return
            self.operand_stack.append(self.get_result_var())
            self.type_stack.append(function['returnType'])
            #Add a equal to store the return value
            self.operand_stack.append(vaddr)
            self.type_stack.append(function['returnType'])
            self.generate_asignation()

    def generate_eka_quadruple(self, function_name):
        self.quadruples.add_quadruple("EKA", None, None, function_name)

    def generate_return_quadruple(self, function_type):
        e = None
        operand = self.operand_stack.pop()
        operand_type = self.type_stack.pop()
        if (operand_type != function_type):
            e = "Function return type missmatch"
        self.quadruples.add_quadruple("RETURN", None, None, operand)
        return e

    #Method to generate a Goto quadruple
    def generate_jump(self, jumpType):
        e = None
        variable = None
        jumpTo = None
        if len(self.migajitas[jumpType]) > 0:
            jumpTo = self.migajitas[jumpType].pop()
        else:
            self.jump_stack[jumpType].append(len(self.quadruples.quadruples))
        if jumpType != 'GOTO':
            variable = self.operand_stack.pop()
            variable_type = self.type_stack.pop()
            if variable_type != 'bool':
                e = "Expresion is not a boolean!"
        self.quadruples.add_quadruple(jumpType, variable, None, jumpTo)
        return e

    #Method to complete a goto
    def complete_jump(self, jumpType):
        address = self.jump_stack[jumpType].pop()
        jumpAddress = len(self.quadruples.quadruples)
        jumpType = self.quadruples.quadruples[address]["operator"]
        jumpVariable = self.quadruples.quadruples[address]["l_operand"]
        self.quadruples.update_quadruple(address, jumpType, jumpVariable, None, jumpAddress)
    
    #Method to leve migajita de pan
    def new_migajita(self, jumpType):
        self.migajitas[jumpType].append(len(self.quadruples.quadruples))

    #Method to add the end function to que quadruples
    def add_fun_quadruple(self):
        self.quadruples.add_quadruple('EBDOROC', None, None, None)

    #Method the get the current quadruple address
    def current_quadruple_address(self):
        return len(self.quadruples.quadruples) - 1 

    #Method to generate a new goto for a return statment
    def generate_return_jump(self):
        self.return_stack.append(len(self.quadruples.quadruples))
        self.quadruples.add_quadruple('GOTO', None, None, None)

    #Method to complete a return goto
    def complete_return_jump(self):
        #Function ends, complete all returns goto in stack
        while len(self.return_stack) > 0:
            address = self.return_stack.pop()
            jumpAddress = len(self.quadruples.quadruples)
            self.quadruples.update_quadruple(address, 'GOTO', None, None, jumpAddress)
