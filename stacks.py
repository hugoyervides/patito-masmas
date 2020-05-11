# Stacks class
# Victor Hugo Oyervides Covarrubias - A01382836
# Obed Gonzalez Morneo - A01382900
from quadruples import Quadruples
from var_table import Vartable
from fun_table import Funtable

class Stacks:
    def __init__(self):
        self.operatorStack = []
        self.operandStack = [] 
        self.jumpStack = {
            'GOTOF' : [],
            'GOTO' : []
        } 
        self.migajitas = {
            'GOTOF' : [],
            'GOTO' : []
        }
        self.funcTable = Funtable()
        self.quadruples = Quadruples() 
        self.resultCounter = 0
        self.var_table = Vartable()
        self.current_function = {}

    #Method to register a new oeprator into our stackl
    def register_operator(self, operator):
        self.operatorStack.append(operator)

    #Method to register a new operand into our stack
    def register_operand(self, variable):
        self.operandStack.append(variable)

    #Method to register a new $ into the operator stack
    #Used to separate the operators of a expresion inside a () )
    def register_separator(self):
        self.operatorStack.append('$')

    #Method to eliminate the $ if it exists in top of the operator stack
    #When we are done evaluating our expresion inside the () )
    def pop_separator(self):
        if self.operatorStack[-1] == '$':
            self.operatorStack.pop()
            return True
        else:
            return False

    #Method to get the top of the operators (Used to for neuralgic points)
    def top_operators(self):
        if len(self.operatorStack) > 0 and self.operandStack[-1] != '$':
            return self.operatorStack[-1]
        else:
            return None

    #Method to get the top operand (Currently not used but may be helpful in the future >:D )
    def top_operand(self):
        if len(self.operandStack) > 0:
            return self.operandStack[-1]
        else:
            return None

    #Method to get a new temporal value name
    def get_result_var(self):
        result = 't' + str(self.resultCounter)
        self.resultCounter += 1
        return result

    #The name of this method is really obvious but will it generates a new quadruple when we reach certain neuralgic point
    def generate_quadruple(self):
        r_operand = self.operandStack.pop()
        l_operand = self.operandStack.pop()
        operator = self.operatorStack.pop()
        result = self.get_result_var()
        self.operandStack.append(result)
        self.quadruples.add_quadruple(operator,l_operand,r_operand,result)

    #This does the same as the previus method but formats the quadruple for asignation ( = NEW_VALUE NULL RESULT)
    def generate_asignation(self):
        r_operand = self.operandStack.pop()
        result = self.operandStack.pop()
        operator = self.operatorStack.pop()
        self.operandStack.append(result)
        self.quadruples.add_quadruple(operator,r_operand, None, result)
    
    #Method to generate a Goto quadruple
    def generate_jump(self, jumpType):
        variable = None
        jumpTo = None
        if len(self.migajitas[jumpType]) > 0:
            jumpTo = self.migajitas[jumpType].pop()
        else:
            self.jumpStack[jumpType].append(len(self.quadruples.quadruples))
        if jumpType != 'GOTO':
            variable = self.operandStack.pop()
        self.quadruples.add_quadruple(jumpType, variable, None, jumpTo)
    
    #Method to complete a goto
    def complete_jump(self, jumpType):
        address = self.jumpStack[jumpType].pop()
        jumpAddress = len(self.quadruples.quadruples)
        jumpType = self.quadruples.quadruples[address]["operator"]
        jumpVariable = self.quadruples.quadruples[address]["l_operand"]
        self.quadruples.update_quadruple(address, jumpType, jumpVariable, None, jumpAddress)
    
    #Method to leve migajita de pan
    def new_migajita(self, jumpType):
        self.migajitas[jumpType].append(len(self.quadruples.quadruples))

    #Method to change current scoped function
    def updateFunction(self, key, value):
        self.current_function[key] = value
    
    #Method to update the function quadruple address
    def update_fun_address(self):
        self.current_function["quadrupleAddress"] = len(self.quadruples.quadruples)

    #Method to flush current function
    def flushFunctionTable(self):
        self.current_function = {}

    #Method to insert the current function into the table
    def insertToFunTable(self):
        self.funcTable.newFunction(self.current_function["name"],
                                    self.current_function["varType"],
                                    self.current_function["quadrupleAddress"])

    #Method to add the end function to que quadruples
    def add_fun_quadruple(self):
        self.quadruples.add_quadruple('EBDOROC', None, None, None)
        
    #Method to flush current var table
    def flush_var_table(self):
        self.var_table = Vartable()
    