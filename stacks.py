# Stacks class
# Victor Hugo Oyervides Covarrubias - A01382836
# Obed Gonzalez Morneo - A01382900

#This class is used to handle all the stack operations used during the semantics
#Operator Stack, Operand Stack, Type Stack, jump_stack, Migajitas and quadruples

from quadruples import Quadruples

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
        self.quadruples = Quadruples() 
        self.result_counter = 0

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
        if self.operator_stack[-1] == '$':
            self.operator_stack.pop()
            return True
        else:
            return False

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

    #Method to get a new temporal value name
    def get_result_var(self):
        result = 't' + str(self.result_counter)
        self.result_counter += 1
        return result

    #The name of this method is really obvious but will it generates a new quadruple when we reach certain neuralgic point
    def generate_quadruple(self):
        r_operand = self.operand_stack.pop()
        l_operand = self.operand_stack.pop()
        operator = self.operator_stack.pop()
        result = self.get_result_var()
        self.operand_stack.append(result)
        self.quadruples.add_quadruple(operator,l_operand,r_operand,result)

    #This does the same as the previus method but formats the quadruple for asignation ( = NEW_VALUE NULL RESULT)
    def generate_asignation(self):
        r_operand = self.operand_stack.pop()
        result = self.operand_stack.pop()
        operator = self.operator_stack.pop()
        self.operand_stack.append(result)
        self.quadruples.add_quadruple(operator,r_operand, None, result)
    
    #Method to generate a Goto quadruple
    def generate_jump(self, jumpType):
        variable = None
        jumpTo = None
        if len(self.migajitas[jumpType]) > 0:
            jumpTo = self.migajitas[jumpType].pop()
        else:
            self.jump_stack[jumpType].append(len(self.quadruples.quadruples))
        if jumpType != 'GOTO':
            variable = self.operand_stack.pop()
        self.quadruples.add_quadruple(jumpType, variable, None, jumpTo)
    
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